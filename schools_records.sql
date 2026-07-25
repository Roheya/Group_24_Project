CREATE TABLE IF NOT EXISTS schools (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    school_name TEXT UNIQUE NOT NULL,
    population INTEGER,
    girls_affected INTEGER,
    days_missed REAL,
    pad_cost REAL,
    days_lost REAL,
    annual_cost REAL,
    date_added TEXT
);
