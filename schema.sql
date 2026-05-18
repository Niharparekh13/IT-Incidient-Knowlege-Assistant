DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS knowledge_base;
DROP TABLE IF EXISTS incidents;
DROP TABLE IF EXISTS ai_recommendations;
DROP TABLE IF EXISTS feedback;

CREATE TABLE categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE knowledge_base (
    solution_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER,
    issue_title TEXT NOT NULL,
    issue_description TEXT NOT NULL,
    troubleshooting_steps TEXT NOT NULL,
    priority_level TEXT,
    keywords TEXT,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

CREATE TABLE incidents (
    incident_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT,
    user_issue TEXT NOT NULL,
    category_id INTEGER,
    status TEXT DEFAULT 'Open',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

CREATE TABLE ai_recommendations (
    recommendation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    incident_id INTEGER,
    solution_id INTEGER,
    confidence_score REAL,
    recommended_text TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (incident_id) REFERENCES incidents(incident_id),
    FOREIGN KEY (solution_id) REFERENCES knowledge_base(solution_id)
);

CREATE TABLE feedback (
    feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
    incident_id INTEGER,
    is_helpful TEXT,
    comments TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (incident_id) REFERENCES incidents(incident_id)
);
