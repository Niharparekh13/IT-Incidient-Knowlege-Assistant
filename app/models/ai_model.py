def save_ai_recommendation(
    db,
    incident_id,
    knowledge_base_id,
    confidence_score,
    recommended_text,
):
    try:
        confidence = float(confidence_score) if confidence_score else None
    except ValueError:
        confidence = None

    db.execute(
        """
        INSERT INTO ai_recommendations
            (incident_id, knowledge_base_id, confidence_score, recommended_text)
        VALUES (?, ?, ?, ?)
        """,
        (incident_id, knowledge_base_id, confidence, recommended_text),
    )


def get_recommendations_for_incident(db, incident_id):
    return db.execute(
        """
        SELECT ar.*, kb.title AS knowledge_title
        FROM ai_recommendations ar
        LEFT JOIN knowledge_base kb ON kb.id = ar.knowledge_base_id
        WHERE ar.incident_id = ?
        ORDER BY ar.created_at DESC
        """,
        (incident_id,),
    ).fetchall()


def get_ai_summary(db):
    return db.execute(
        """
        SELECT
            COUNT(*) AS recommendation_count,
            AVG(confidence_score) AS average_confidence
        FROM ai_recommendations
        """
    ).fetchone()


def get_ai_recommendations(db):
    return db.execute(
        """
        SELECT
            ar.*,
            i.user_issue,
            i.status,
            kb.title AS knowledge_title,
            c.name AS category_name
        FROM ai_recommendations ar
        JOIN incidents i ON i.id = ar.incident_id
        LEFT JOIN knowledge_base kb ON kb.id = ar.knowledge_base_id
        LEFT JOIN categories c ON c.id = i.category_id
        ORDER BY ar.created_at DESC
        """
    ).fetchall()


def get_feedback_summary(db):
    return db.execute(
        """
        SELECT
            COUNT(*) AS feedback_count,
            SUM(CASE WHEN is_helpful = 1 THEN 1 ELSE 0 END) AS helpful_count
        FROM feedback
        """
    ).fetchone()
