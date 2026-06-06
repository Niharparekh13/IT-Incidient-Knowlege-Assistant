from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from ..db import get_db
from ..models.ai_model import (
    get_ai_recommendations,
    get_ai_summary,
    get_feedback_summary,
    get_recommendations_for_incident,
    save_ai_recommendation,
)
from ..models.incident_model import (
    INCIDENT_STATUSES,
    create_feedback,
    create_incident,
    delete_incident as delete_incident_record,
    get_feedback_for_incident,
    get_home_summary,
    get_incident_by_id,
    get_incident_detail,
    get_incidents,
    get_recent_incidents,
    get_status_counts,
    update_incident as update_incident_record,
)
from ..models.knowledge_model import (
    create_knowledge_entry,
    delete_knowledge_entry,
    get_categories,
    get_common_solutions,
    get_knowledge_by_id,
    get_knowledge_entries,
    get_knowledge_entries_with_incident_count,
    update_knowledge_entry,
)
from ..services.ai_agent import (
    build_escalation_message,
    build_general_ai_guidance,
    recommend_solutions,
)

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    db = get_db()
    categories = get_categories(db)
    summary = get_home_summary(db)
    recent_incidents = get_recent_incidents(db)
    common_solutions = get_common_solutions(db)

    return render_template(
        "index.html",
        categories=categories,
        summary=summary,
        recent_incidents=recent_incidents,
        common_solutions=common_solutions,
    )


@bp.route("/search", methods=["POST"])
def search():
    issue = request.form.get("issue", "").strip()
    category_id = request.form.get("category_id") or None

    if not issue:
        flash("Enter an issue before searching.")
        return redirect(url_for("main.index"))

    db = get_db()
    categories = get_categories(db)
    matches = recommend_solutions(db, issue, category_id)
    escalation_message = build_escalation_message(issue, bool(matches))
    general_guidance = None
    if not matches:
        general_guidance = build_general_ai_guidance(issue)

    return render_template(
        "results.html",
        issue=issue,
        category_id=category_id,
        categories=categories,
        matches=matches,
        escalation_message=escalation_message,
        general_guidance=general_guidance,
    )


@bp.route("/incidents", methods=["GET", "POST"])
def incidents():
    db = get_db()

    if request.method == "POST":
        user_issue = request.form.get("issue", "").strip()
        category_id = request.form.get("category_id") or None
        matched_kb_id = request.form.get("matched_kb_id") or None
        status = request.form.get("status") or "new"
        notes = request.form.get("notes", "").strip()
        confidence_score = request.form.get("confidence_score") or None
        recommended_text = request.form.get("recommended_text", "").strip()

        if not user_issue:
            flash("Incident details are required.")
            return redirect(url_for("main.new_incident"))

        if status not in INCIDENT_STATUSES:
            status = "new"

        incident_id = create_incident(
            db,
            category_id,
            user_issue,
            matched_kb_id,
            status,
            notes or "Created from Week 3 user flow.",
        )

        if matched_kb_id or recommended_text:
            save_ai_recommendation(
                db,
                incident_id,
                matched_kb_id,
                confidence_score,
                recommended_text or "AI v1 recommendation created from selected solution.",
            )

        db.commit()
        flash("Incident saved.")
        return redirect(url_for("main.incidents"))

    incident_rows = get_incidents(db)
    status_counts = get_status_counts(db)

    return render_template(
        "incidents.html",
        incidents=incident_rows,
        status_counts=status_counts,
    )


@bp.route("/incidents/<int:incident_id>")
def incident_detail(incident_id):
    db = get_db()
    incident = get_incident_detail_or_404(db, incident_id)
    recommendations = get_recommendations_for_incident(db, incident_id)
    feedback_rows = get_feedback_for_incident(db, incident_id)

    return render_template(
        "incident_detail.html",
        incident=incident,
        recommendations=recommendations,
        feedback_rows=feedback_rows,
    )


@bp.route("/incidents/<int:incident_id>/feedback", methods=["POST"])
def add_feedback(incident_id):
    db = get_db()
    get_incident_or_404(db, incident_id)
    is_helpful = request.form.get("is_helpful")
    comments = request.form.get("comments", "").strip()

    if is_helpful not in {"0", "1"}:
        flash("Choose whether the recommendation was helpful.")
        return redirect(url_for("main.incident_detail", incident_id=incident_id))

    create_feedback(db, incident_id, int(is_helpful), comments)
    db.commit()
    flash("Feedback saved.")
    return redirect(url_for("main.incident_detail", incident_id=incident_id))


@bp.route("/incidents/new")
def new_incident():
    db = get_db()
    return render_template(
        "incident_form.html",
        form_action=url_for("main.incidents"),
        incident=None,
        categories=get_categories(db),
        knowledge_entries=get_knowledge_entries(db),
        statuses=INCIDENT_STATUSES,
        submit_label="Create Incident",
    )


@bp.route("/incidents/<int:incident_id>/edit", methods=["GET", "POST"])
def edit_incident(incident_id):
    db = get_db()
    incident = get_incident_or_404(db, incident_id)

    if request.method == "POST":
        user_issue = request.form.get("issue", "").strip()
        category_id = request.form.get("category_id") or None
        matched_kb_id = request.form.get("matched_kb_id") or None
        status = request.form.get("status") or "new"
        notes = request.form.get("notes", "").strip()

        if not user_issue:
            flash("Incident details are required.")
        elif status not in INCIDENT_STATUSES:
            flash("Choose a valid incident status.")
        else:
            update_incident_record(
                db,
                incident_id,
                category_id,
                user_issue,
                matched_kb_id,
                status,
                notes,
            )
            db.commit()
            flash("Incident updated.")
            return redirect(url_for("main.incidents"))

    return render_template(
        "incident_form.html",
        form_action=url_for("main.edit_incident", incident_id=incident_id),
        incident=incident,
        categories=get_categories(db),
        knowledge_entries=get_knowledge_entries(db),
        statuses=INCIDENT_STATUSES,
        submit_label="Update Incident",
    )


@bp.route("/incidents/<int:incident_id>/delete", methods=["POST"])
def delete_incident(incident_id):
    db = get_db()
    get_incident_or_404(db, incident_id)
    delete_incident_record(db, incident_id)
    db.commit()
    flash("Incident deleted.")
    return redirect(url_for("main.incidents"))


@bp.route("/knowledge")
def knowledge():
    db = get_db()
    entries = get_knowledge_entries_with_incident_count(db)

    return render_template("knowledge.html", entries=entries)


@bp.route("/knowledge/new", methods=["GET", "POST"])
def new_knowledge():
    db = get_db()
    categories = get_categories(db)

    if request.method == "POST":
        category_id = request.form.get("category_id")
        title = request.form.get("title", "").strip()
        symptoms = request.form.get("symptoms", "").strip()
        resolution_steps = request.form.get("resolution_steps", "").strip()
        escalation_required = 1 if request.form.get("escalation_required") else 0

        if not category_id or not title or not symptoms or not resolution_steps:
            flash("All knowledge base fields are required.")
            return render_template(
                "knowledge_form.html",
                form_action=url_for("main.new_knowledge"),
                entry=None,
                categories=categories,
                submit_label="Add Solution",
            )

        create_knowledge_entry(
            db,
            category_id,
            title,
            symptoms,
            resolution_steps,
            escalation_required,
        )
        db.commit()
        flash("Knowledge base entry added.")
        return redirect(url_for("main.knowledge"))

    return render_template(
        "knowledge_form.html",
        form_action=url_for("main.new_knowledge"),
        entry=None,
        categories=categories,
        submit_label="Add Solution",
    )


@bp.route("/knowledge/<int:entry_id>/edit", methods=["GET", "POST"])
def edit_knowledge(entry_id):
    db = get_db()
    entry = get_knowledge_or_404(db, entry_id)
    categories = get_categories(db)

    if request.method == "POST":
        category_id = request.form.get("category_id")
        title = request.form.get("title", "").strip()
        symptoms = request.form.get("symptoms", "").strip()
        resolution_steps = request.form.get("resolution_steps", "").strip()
        escalation_required = 1 if request.form.get("escalation_required") else 0

        if not category_id or not title or not symptoms or not resolution_steps:
            flash("All knowledge base fields are required.")
        else:
            update_knowledge_entry(
                db,
                entry_id,
                category_id,
                title,
                symptoms,
                resolution_steps,
                escalation_required,
            )
            db.commit()
            flash("Knowledge base entry updated.")
            return redirect(url_for("main.knowledge"))

    return render_template(
        "knowledge_form.html",
        form_action=url_for("main.edit_knowledge", entry_id=entry_id),
        entry=entry,
        categories=categories,
        submit_label="Update Solution",
    )


@bp.route("/knowledge/<int:entry_id>/delete", methods=["POST"])
def delete_knowledge(entry_id):
    db = get_db()
    get_knowledge_or_404(db, entry_id)
    delete_knowledge_entry(db, entry_id)
    db.commit()
    flash("Knowledge base entry deleted.")
    return redirect(url_for("main.knowledge"))


@bp.route("/ai")
def ai_dashboard():
    db = get_db()
    summary = get_ai_summary(db)
    recommendations = get_ai_recommendations(db)
    feedback_summary = get_feedback_summary(db)

    return render_template(
        "ai_dashboard.html",
        summary=summary,
        recommendations=recommendations,
        feedback_summary=feedback_summary,
    )


def get_knowledge_or_404(db, entry_id):
    entry = get_knowledge_by_id(db, entry_id)
    if entry is None:
        abort(404)
    return entry


def get_incident_or_404(db, incident_id):
    incident = get_incident_by_id(db, incident_id)
    if incident is None:
        abort(404)
    return incident


def get_incident_detail_or_404(db, incident_id):
    incident = get_incident_detail(db, incident_id)
    if incident is None:
        abort(404)
    return incident
