-- Database initialization schema for Smart Energy Advisor

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS energy_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    units_consumed REAL NOT NULL,
    rate REAL NOT NULL,
    family_members INTEGER NOT NULL,
    house_type TEXT NOT NULL,
    ac_hours REAL NOT NULL,
    fan_hours REAL NOT NULL,
    tv_hours REAL NOT NULL,
    refrigerator INTEGER NOT NULL DEFAULT 0,
    washing_machine INTEGER NOT NULL DEFAULT 0,
    cooler INTEGER NOT NULL DEFAULT 0,
    other_appliances INTEGER NOT NULL DEFAULT 0,
    recorded_date DATE NOT NULL DEFAULT CURRENT_DATE,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);
