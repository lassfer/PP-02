
import pandas as pd
from datetime import datetime, timedelta
from src.db.database import get_connection

def report_stock():
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT tool_id, name, tool_type, diameter, material, status, cell_code
        FROM tools
        ORDER BY tool_type, name
    """, conn)
    conn.close()
    return df

def report_debtors(days=3):
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT t.tool_id, t.name, t.issue_date, e.full_name, e.position
        FROM tools t
        JOIN employees e ON e.employee_id = t.issued_to
        WHERE t.status='ISSUED'
    """, conn)
    conn.close()

    if df.empty:
        return df

    df["issue_date"] = pd.to_datetime(df["issue_date"])
    border = datetime.now() - timedelta(days=days)
    return df[df["issue_date"] < border].sort_values("issue_date")

def report_top_tools(limit=5):
    conn = get_connection()
    df = pd.read_sql_query(f"""
        SELECT tool_id, COUNT(*) as issue_count
        FROM operations
        WHERE op_type='ISSUE'
        GROUP BY tool_id
        ORDER BY issue_count DESC
        LIMIT {limit}
    """, conn)
    conn.close()
    return df
