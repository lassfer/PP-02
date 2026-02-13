
from datetime import datetime
from src.db.database import get_connection
from src.utils.logger import get_logger

logger = get_logger()

def _now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def find_free_cell(conn):
    cur = conn.cursor()
    cur.execute("SELECT code FROM storage_cells WHERE is_free = 1 ORDER BY code LIMIT 1")
    row = cur.fetchone()
    return row[0] if row else None

def accept_tool(tool_id, name, tool_type, diameter=None, material=None, service_life_minutes=None):
    conn = get_connection()
    cur = conn.cursor()

    free_cell = find_free_cell(conn)
    if not free_cell:
        raise RuntimeError("Нет свободных ячеек хранения!")

    cur.execute("""
        INSERT INTO tools(tool_id, name, tool_type, diameter, material, status, cell_code, service_life_minutes)
        VALUES (?, ?, ?, ?, ?, 'IN_STOCK', ?, ?)
    """, (tool_id, name, tool_type, diameter, material, free_cell, service_life_minutes))

    cur.execute("UPDATE storage_cells SET is_free = 0 WHERE code = ?", (free_cell,))

    cur.execute("""
        INSERT INTO operations(op_type, tool_id, employee_id, op_date, comment)
        VALUES ('ACCEPT', ?, NULL, ?, ?)
    """, (tool_id, _now(), f"Принят и размещен в {free_cell}"))

    conn.commit()
    conn.close()
    logger.info(f"ACCEPT tool={tool_id} cell={free_cell}")
    return free_cell

def issue_tool(tool_id, employee_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT status, cell_code FROM tools WHERE tool_id = ?", (tool_id,))
    row = cur.fetchone()
    if not row:
        raise RuntimeError("Инструмент не найден!")
    status, cell_code = row

    if status != "IN_STOCK":
        raise RuntimeError(f"Инструмент не на складе (status={status})")

    cur.execute("""
        UPDATE tools
        SET status='ISSUED', issued_to=?, issue_date=?, cell_code=NULL
        WHERE tool_id=?
    """, (employee_id, _now(), tool_id))

    if cell_code:
        cur.execute("UPDATE storage_cells SET is_free = 1 WHERE code = ?", (cell_code,))

    cur.execute("""
        INSERT INTO operations(op_type, tool_id, employee_id, op_date, comment)
        VALUES ('ISSUE', ?, ?, ?, 'Выдан')
    """, (tool_id, employee_id, _now()))

    conn.commit()
    conn.close()
    logger.info(f"ISSUE tool={tool_id} employee={employee_id}")

def return_tool(tool_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT status FROM tools WHERE tool_id = ?", (tool_id,))
    row = cur.fetchone()
    if not row:
        raise RuntimeError("Инструмент не найден!")

    if row[0] != "ISSUED":
        raise RuntimeError("Инструмент не числится как выданный!")

    free_cell = find_free_cell(conn)
    if not free_cell:
        raise RuntimeError("Нет свободных ячеек хранения!")

    cur.execute("""
        UPDATE tools
        SET status='IN_STOCK', issued_to=NULL, issue_date=NULL, cell_code=?
        WHERE tool_id=?
    """, (free_cell, tool_id))

    cur.execute("UPDATE storage_cells SET is_free = 0 WHERE code = ?", (free_cell,))

    cur.execute("""
        INSERT INTO operations(op_type, tool_id, employee_id, op_date, comment)
        VALUES ('RETURN', ?, NULL, ?, ?)
    """, (tool_id, _now(), f"Возврат на склад, размещено в {free_cell}"))

    conn.commit()
    conn.close()
    logger.info(f"RETURN tool={tool_id} cell={free_cell}")
    return free_cell

def write_off(tool_id, comment="Списан"):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT status, cell_code FROM tools WHERE tool_id = ?", (tool_id,))
    row = cur.fetchone()
    if not row:
        raise RuntimeError("Инструмент не найден!")

    status, cell_code = row

    cur.execute("""
        UPDATE tools SET status='WRITTEN_OFF', issued_to=NULL, issue_date=NULL, cell_code=NULL
        WHERE tool_id=?
    """, (tool_id,))

    if cell_code:
        cur.execute("UPDATE storage_cells SET is_free = 1 WHERE code = ?", (cell_code,))

    cur.execute("""
        INSERT INTO operations(op_type, tool_id, employee_id, op_date, comment)
        VALUES ('WRITE_OFF', ?, NULL, ?, ?)
    """, (tool_id, _now(), comment))

    conn.commit()
    conn.close()
    logger.info(f"WRITE_OFF tool={tool_id}")
