import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database', 'database.db')

def get_db_connection():
    """Establish a connection to the SQLite database with row factory enabled."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # Enable foreign keys support
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    """Initialize the database tables if they do not exist."""
    schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database', 'schema.sql')
    with open(schema_path, 'r') as f:
        schema_sql = f.read()
    
    conn = get_db_connection()
    try:
        conn.executescript(schema_sql)
        conn.commit()
    finally:
        conn.close()

def create_user(name, email, password_hash):
    """Insert a new user record into the users table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email.lower().strip(), password_hash)
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None  # Email already exists
    finally:
        conn.close()

def get_user_by_email(email):
    """Retrieve user details by email address."""
    conn = get_db_connection()
    try:
        user = conn.execute(
            "SELECT * FROM users WHERE email = ?",
            (email.lower().strip(),)
        ).fetchone()
        return dict(user) if user else None
    finally:
        conn.close()

def get_user_by_id(user_id):
    """Retrieve user details by unique User ID."""
    conn = get_db_connection()
    try:
        user = conn.execute(
            "SELECT * FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()
        return dict(user) if user else None
    finally:
        conn.close()

def update_user_profile(user_id, name, email):
    """Update name and email in the user's profile database entry."""
    conn = get_db_connection()
    try:
        conn.execute(
            "UPDATE users SET name = ?, email = ? WHERE id = ?",
            (name, email.lower().strip(), user_id)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Email clash
    finally:
        conn.close()

def update_user_password(user_id, password_hash):
    """Update the hashed password of a user."""
    conn = get_db_connection()
    try:
        conn.execute(
            "UPDATE users SET password_hash = ? WHERE id = ?",
            (password_hash, user_id)
        )
        conn.commit()
        return True
    finally:
        conn.close()

def add_energy_usage(user_id, units_consumed, rate, family_members, house_type, 
                     ac_hours, fan_hours, tv_hours, refrigerator, washing_machine, 
                     cooler, other_appliances, recorded_date):
    """Insert a new monthly usage and appliance logging entry into the database."""
    conn = get_db_connection()
    try:
        conn.execute(
            """INSERT INTO energy_usage 
            (user_id, units_consumed, rate, family_members, house_type, ac_hours, fan_hours, tv_hours, 
             refrigerator, washing_machine, cooler, other_appliances, recorded_date) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (user_id, units_consumed, rate, family_members, house_type, ac_hours, fan_hours, tv_hours, 
             int(refrigerator), int(washing_machine), int(cooler), int(other_appliances), recorded_date)
        )
        conn.commit()
        return True
    finally:
        conn.close()

def get_energy_usage_history(user_id):
    """Retrieve historical energy logs for a specific user, sorted by date."""
    conn = get_db_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM energy_usage WHERE user_id = ? ORDER BY recorded_date ASC",
            (user_id,)
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()

def get_latest_energy_usage(user_id):
    """Retrieve the most recent energy log for a user."""
    conn = get_db_connection()
    try:
        row = conn.execute(
            "SELECT * FROM energy_usage WHERE user_id = ? ORDER BY recorded_date DESC LIMIT 1",
            (user_id,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

def delete_all_energy_usage(user_id):
    """Delete all recorded usage data for a user (Reset feature)."""
    conn = get_db_connection()
    try:
        conn.execute("DELETE FROM energy_usage WHERE user_id = ?", (user_id,))
        conn.commit()
        return True
    finally:
        conn.close()
