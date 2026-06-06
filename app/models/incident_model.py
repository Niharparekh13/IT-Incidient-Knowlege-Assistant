INCIDENT_STATUSES = ["new", "in_progress", "resolved", "escalated"]


def get_home_summary(db):
    return db.execute(
        """
        SELECT
            (SELECT COUNT(*) FROM knowledge_base) AS knowledge_count,
            (SELECT COUNT(*) FROM incidents) AS incident_count,
            (SELECT COUNT(*) FROM ai_recommendations) AS recommendation_count,
            (SELECT COUNT(*) FROM feedback) AS feedback_count
        """
    ).fetchone()


def get_recent_incidents(db, limit=4):
    return db.execute(
        """
        SELECT i.*, c.name AS category_name
        FROM incidents i
        LEFT JOIN categories c ON c.id = i.category_id
        ORDER BY i.created_at DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()


def create_incident(
    db,
    category_id,
    user_issue,
    matched_kb_id,
    status,
    notes,
):
    cursor = db.execute(
        """
        INSERT INTO incidents (category_id, user_issue, matched_kb_id, status, notes)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            category_id,
            user_issue,
            matched_kb_id,
            status,
            notes,
        ),
    )
    return cursor.lastrowid


def get_incidents(db):
    return db.execute(
        """
        SELECT i.*, c.name AS category_name, kb.title AS matched_title
        FROM incidents i
        LEFT JOIN categories c ON c.id = i.category_id
        LEFT JOIN knowledge_base kb ON kb.id = i.matched_kb_id
        ORDER BY i.created_at DESC
        """
    ).fetchall()


def get_status_counts(db):
    return db.execute(
        """
        SELECT status, COUNT(*) AS total
        FROM incidents
        GROUP BY status
        ORDER BY status
        """
    ).fetchall()


def get_incident_by_id(db, incident_id):
    return db.execute("SELECT * FROM incidents WHERE id = ?", (incident_id,)).fetchone()


def get_incident_detail(db, incident_id):
    return db.execute(
        """
        SELECT i.*, c.name AS category_name, kb.title AS matched_title,
            kb.resolution_steps AS matched_steps
        FROM incidents i
        LEFT JOIN categories c ON c.id = i.category_id
        LEFT JOIN knowledge_base kb ON kb.id = i.matched_kb_id
        WHERE i.id = ?
        """,
        (incident_id,),
    ).fetchone()


def update_incident(
    db,
    incident_id,
    category_id,
    user_issue,
    matched_kb_id,
    status,
    notes,
):
    db.execute(
        """
        UPDATE incidents
        SET category_id = ?, user_issue = ?, matched_kb_id = ?, status = ?, notes = ?
        WHERE id = ?
        """,
        (category_id, user_issue, matched_kb_id, status, notes, incident_id),
    )


def delete_incident(db, incident_id):
    db.execute("DELETE FROM feedback WHERE incident_id = ?", (incident_id,))
    db.execute("DELETE FROM ai_recommendations WHERE incident_id = ?", (incident_id,))
    db.execute("DELETE FROM incidents WHERE id = ?", (incident_id,))


def get_feedback_for_incident(db, incident_id):
    return db.execute(
        """
        SELECT *
        FROM feedback
        WHERE incident_id = ?
        ORDER BY created_at DESC
        """,
        (incident_id,),
    ).fetchall()


def create_feedback(db, incident_id, is_helpful, comments):
    db.execute(
        """
        INSERT INTO feedback (incident_id, is_helpful, comments)
        VALUES (?, ?, ?)
        """,
        (incident_id, is_helpful, comments),
    )
