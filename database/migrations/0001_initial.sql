CREATE TABLE IF NOT EXISTS incidents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    requester TEXT NOT NULL,
    area TEXT NOT NULL,
    category TEXT,
    status TEXT NOT NULL DEFAULT 'aberto',
    priority TEXT NOT NULL DEFAULT 'media',
    impact_users INTEGER NOT NULL DEFAULT 1,
    urgency TEXT NOT NULL DEFAULT 'media',
    ai_category TEXT,
    ai_priority TEXT,
    ai_confidence REAL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_incidents_created_at
    ON incidents(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_incidents_status
    ON incidents(status);

CREATE INDEX IF NOT EXISTS idx_incidents_priority
    ON incidents(priority);

CREATE INDEX IF NOT EXISTS idx_incidents_category
    ON incidents(category);
