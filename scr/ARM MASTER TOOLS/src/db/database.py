
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "db" / "mastertool.db"

def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.executescript("""
    PRAGMA foreign_keys = ON;

    CREATE TABLE IF NOT EXISTS employees (
        employee_id INTEGER PRIMARY KEY,
        full_name TEXT NOT NULL,
        position TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS storage_cells (
        cell_id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT NOT NULL UNIQUE,
        is_free INTEGER NOT NULL DEFAULT 1
    );

    CREATE TABLE IF NOT EXISTS tools (
        tool_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        tool_type TEXT NOT NULL,
        diameter REAL,
        material TEXT,
        status TEXT NOT NULL DEFAULT 'IN_STOCK',
        cell_code TEXT,
        issued_to INTEGER,
        issue_date TEXT,
        service_life_minutes INTEGER,
        FOREIGN KEY (issued_to) REFERENCES employees(employee_id)
    );

    CREATE TABLE IF NOT EXISTS operations (
        op_id INTEGER PRIMARY KEY AUTOINCREMENT,
        op_type TEXT NOT NULL,
        tool_id TEXT NOT NULL,
        employee_id INTEGER,
        op_date TEXT NOT NULL,
        comment TEXT,
        FOREIGN KEY (tool_id) REFERENCES tools(tool_id),
        FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
    );
    """)

    conn.commit()
    conn.close()
    print(f"DB created: {DB_PATH}")

if __name__ == "__main__":
    init_db()
