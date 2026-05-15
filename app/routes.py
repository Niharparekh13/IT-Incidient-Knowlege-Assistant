from flask import Blueprint, flash, redirect, render_template, request, url_for

from .db import get_db

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    db = get_db()
    categories = db.execute("SELECT * FROM categories ORDER BY name").fetchall()
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
    categories = db.execute("SELECT * FROM categories ORDER BY name").fetchall()
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

        if not user_issue:
            flash("Incident details are required.")
            return redirect(url_for("main.index"))

        db.execute(
            """
            INSERT INTO incidents (category_id, user_issue, matched_kb_id, notes)
            VALUES (?, ?, ?, ?)
            """,
            (
                category_id,
                user_issue,
                matched_kb_id,
                "Created from Week 2 search flow.",
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


@bp.route("/knowledge/new", methods=["GET", "POST"])
def new_knowledge():
    db = get_db()
    categories = db.execute("SELECT * FROM categories ORDER BY name").fetchall()

    if request.method == "POST":
        category_id = request.form.get("category_id")
        title = request.form.get("title", "").strip()
        symptoms = request.form.get("symptoms", "").strip()
        resolution_steps = request.form.get("resolution_steps", "").strip()
        escalation_required = 1 if request.form.get("escalation_required") else 0

        if not category_id or not title or not symptoms or not resolution_steps:
            flash("All knowledge base fields are required.")
            return render_template("knowledge_form.html", categories=categories)

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
        return redirect(url_for("main.index"))

    return render_template("knowledge_form.html", categories=categories)


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
