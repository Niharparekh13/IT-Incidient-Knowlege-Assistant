def get_categories(db):
    return db.execute("SELECT * FROM categories ORDER BY name").fetchall()


def get_common_solutions(db, limit=6):
    return db.execute(
        """
        SELECT kb.*, c.name AS category_name
        FROM knowledge_base kb
        JOIN categories c ON c.id = kb.category_id
        ORDER BY kb.created_at DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()


def get_knowledge_entries(db):
    return db.execute(
        """
        SELECT kb.*, c.name AS category_name
        FROM knowledge_base kb
        JOIN categories c ON c.id = kb.category_id
        ORDER BY c.name, kb.title
        """
    ).fetchall()


def get_knowledge_entries_with_incident_count(db):
    return db.execute(
        """
        SELECT kb.*, c.name AS category_name, COUNT(i.id) AS incident_count
        FROM knowledge_base kb
        JOIN categories c ON c.id = kb.category_id
        LEFT JOIN incidents i ON i.matched_kb_id = kb.id
        GROUP BY kb.id
        ORDER BY c.name, kb.title
        """
    ).fetchall()


def get_knowledge_by_id(db, entry_id):
    return db.execute("SELECT * FROM knowledge_base WHERE id = ?", (entry_id,)).fetchone()


def create_knowledge_entry(
    db,
    category_id,
    title,
    symptoms,
    resolution_steps,
    escalation_required,
):
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


def update_knowledge_entry(
    db,
    entry_id,
    category_id,
    title,
    symptoms,
    resolution_steps,
    escalation_required,
):
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


def delete_knowledge_entry(db, entry_id):
    db.execute("UPDATE incidents SET matched_kb_id = NULL WHERE matched_kb_id = ?", (entry_id,))
    db.execute(
        "UPDATE ai_recommendations SET knowledge_base_id = NULL WHERE knowledge_base_id = ?",
        (entry_id,),
    )
    db.execute("DELETE FROM knowledge_base WHERE id = ?", (entry_id,))
