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

CREATE TABLE IF NOT EXISTS pledges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    donor_name TEXT NOT NULL,
    school_name TEXT NOT NULL,
    pledge_amount REAL NOT NULL,
    pledge_date TEXT DEFAULT CURRENT_TIMESTAMP
);
