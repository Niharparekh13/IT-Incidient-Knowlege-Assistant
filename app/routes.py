from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from .db import get_db

bp = Blueprint("main", __name__)
INCIDENT_STATUSES = ["new", "in_progress", "resolved", "escalated"]


@bp.route("/")
def index():
    db = get_db()
    categories = get_categories(db)
    common_solutions = db.execute(
        """
        SELECT kb.*, c.name AS category_name
        FROM knowledge_base kb
        JOIN categories c ON c.id = kb.category_id
        ORDER BY kb.created_at DESC
        LIMIT 6
        """
    ).fetchall()

    return render_template(
        "index.html",
        categories=categories,
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
    matches = find_matches(db, issue, category_id)

    return render_template(
        "results.html",
        issue=issue,
        category_id=category_id,
        categories=categories,
        matches=matches,
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

        if not user_issue:
            flash("Incident details are required.")
            return redirect(url_for("main.new_incident"))

        if status not in INCIDENT_STATUSES:
            status = "new"

        db.execute(
            """
            INSERT INTO incidents (category_id, user_issue, matched_kb_id, status, notes)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                category_id,
                user_issue,
                matched_kb_id,
                status,
                notes or "Created from Week 3 user flow.",
            ),
        )
        db.commit()
        flash("Incident saved.")
        return redirect(url_for("main.incidents"))

    incident_rows = db.execute(
        """
        SELECT i.*, c.name AS category_name, kb.title AS matched_title
        FROM incidents i
        LEFT JOIN categories c ON c.id = i.category_id
        LEFT JOIN knowledge_base kb ON kb.id = i.matched_kb_id
        ORDER BY i.created_at DESC
        """
    ).fetchall()

    return render_template("incidents.html", incidents=incident_rows)


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
            db.execute(
                """
                UPDATE incidents
                SET category_id = ?, user_issue = ?, matched_kb_id = ?, status = ?, notes = ?
                WHERE id = ?
                """,
                (category_id, user_issue, matched_kb_id, status, notes, incident_id),
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
    db.execute("DELETE FROM incidents WHERE id = ?", (incident_id,))
    db.commit()
    flash("Incident deleted.")
    return redirect(url_for("main.incidents"))


@bp.route("/knowledge")
def knowledge():
    db = get_db()
    entries = db.execute(
        """
        SELECT kb.*, c.name AS category_name, COUNT(i.id) AS incident_count
        FROM knowledge_base kb
        JOIN categories c ON c.id = kb.category_id
        LEFT JOIN incidents i ON i.matched_kb_id = kb.id
        GROUP BY kb.id
        ORDER BY c.name, kb.title
        """
    ).fetchall()

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

        db.execute(
            """
            INSERT INTO knowledge_base
                (category_id, title, symptoms, resolution_steps, escalation_required)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                category_id,
                title,
                symptoms,
                resolution_steps,
                escalation_required,
            ),
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
            db.execute(
                """
                UPDATE knowledge_base
                SET category_id = ?, title = ?, symptoms = ?, resolution_steps = ?,
                    escalation_required = ?
                WHERE id = ?
                """,
                (
                    category_id,
                    title,
                    symptoms,
                    resolution_steps,
                    escalation_required,
                    entry_id,
                ),
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
    db.execute("UPDATE incidents SET matched_kb_id = NULL WHERE matched_kb_id = ?", (entry_id,))
    db.execute("DELETE FROM knowledge_base WHERE id = ?", (entry_id,))
    db.commit()
    flash("Knowledge base entry deleted.")
    return redirect(url_for("main.knowledge"))


def get_categories(db):
    return db.execute("SELECT * FROM categories ORDER BY name").fetchall()


def get_knowledge_entries(db):
    return db.execute(
        """
        SELECT kb.*, c.name AS category_name
        FROM knowledge_base kb
        JOIN categories c ON c.id = kb.category_id
        ORDER BY c.name, kb.title
        """
    ).fetchall()


def get_knowledge_or_404(db, entry_id):
    entry = db.execute("SELECT * FROM knowledge_base WHERE id = ?", (entry_id,)).fetchone()
    if entry is None:
        abort(404)
    return entry


def get_incident_or_404(db, incident_id):
    incident = db.execute("SELECT * FROM incidents WHERE id = ?", (incident_id,)).fetchone()
    if incident is None:
        abort(404)
    return incident


def find_matches(db, issue, category_id=None):
    words = [word for word in issue.lower().split() if len(word) > 2]
    like_terms = [f"%{word}%" for word in words] or [f"%{issue.lower()}%"]

    search_parts = []
    params = []

    for term in like_terms:
        search_parts.append(
            "(LOWER(kb.title) LIKE ? OR LOWER(kb.symptoms) LIKE ? OR LOWER(kb.resolution_steps) LIKE ?)"
        )
        params.extend([term, term, term])

    where_clause = f"({' OR '.join(search_parts)})" if search_parts else "1 = 1"

    if category_id:
        where_clause = f"{where_clause} AND kb.category_id = ?"
        params.append(category_id)

    return db.execute(
        f"""
        SELECT kb.*, c.name AS category_name
        FROM knowledge_base kb
        JOIN categories c ON c.id = kb.category_id
        WHERE {where_clause}
        ORDER BY kb.escalation_required DESC, kb.created_at DESC
        LIMIT 8
        """,
        params,
    ).fetchall()
