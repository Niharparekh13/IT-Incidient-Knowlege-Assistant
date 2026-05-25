DROP TABLE IF EXISTS ai_recommendations;
DROP TABLE IF EXISTS feedback;
DROP TABLE IF EXISTS incidents;
DROP TABLE IF EXISTS knowledge_base;
DROP TABLE IF EXISTS categories;

CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE knowledge_base (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    symptoms TEXT NOT NULL,
    resolution_steps TEXT NOT NULL,
    escalation_required INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories (id)
);

CREATE TABLE incidents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER,
    user_issue TEXT NOT NULL,
    matched_kb_id INTEGER,
    status TEXT NOT NULL DEFAULT 'new',
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories (id),
    FOREIGN KEY (matched_kb_id) REFERENCES knowledge_base (id)
);

CREATE TABLE ai_recommendations (
    recommendation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    incident_id INTEGER NOT NULL,
    knowledge_base_id INTEGER,
    confidence_score REAL,
    recommended_text TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (incident_id) REFERENCES incidents (id),
    FOREIGN KEY (knowledge_base_id) REFERENCES knowledge_base (id)
);

CREATE TABLE feedback (
    feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
    incident_id INTEGER NOT NULL,
    is_helpful INTEGER,
    comments TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (incident_id) REFERENCES incidents (id)
);
