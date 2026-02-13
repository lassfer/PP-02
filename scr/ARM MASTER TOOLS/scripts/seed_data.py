
from src.db.database import get_connection

def seed():
    conn = get_connection()
    cur = conn.cursor()

    employees = [
        (1001, "Иванов И.И.", "Оператор ЧПУ"),
        (1002, "Петров П.П.", "Наладчик"),
        (1003, "Сидоров С.С.", "Мастер цеха"),
    ]
    cur.executemany("INSERT OR IGNORE INTO employees(employee_id, full_name, position) VALUES (?, ?, ?)", employees)

    cells = []
    for rack in ["A", "B"]:
        for row in range(1, 4):
            for shelf in range(1, 4):
                code = f"RACK-{rack}-{row:02d}-{shelf:02d}"
                cells.append((code, 1))

    cur.executemany("INSERT OR IGNORE INTO storage_cells(code, is_free) VALUES (?, ?)", cells)

    tools = [
        ("T-0001", "Фреза концевая", "Фреза", 20.0, "HSS", "IN_STOCK", None, None, None, 500),
        ("T-0002", "Сверло спиральное", "Сверло", 10.0, "HSS", "IN_STOCK", None, None, None, 300),
        ("T-0003", "Резец проходной", "Резец", None, "Твердосплав", "IN_STOCK", None, None, None, 800),
    ]

    # размещаем вручную в первые свободные ячейки
    cur.execute("SELECT code FROM storage_cells WHERE is_free=1 ORDER BY code LIMIT 3")
    free = [x[0] for x in cur.fetchall()]

    for i, tool in enumerate(tools):
        cell = free[i]
        cur.execute("""
            INSERT OR IGNORE INTO tools(tool_id, name, tool_type, diameter, material, status, cell_code, issued_to, issue_date, service_life_minutes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (tool[0], tool[1], tool[2], tool[3], tool[4], "IN_STOCK", cell, None, None, tool[9]))
        cur.execute("UPDATE storage_cells SET is_free=0 WHERE code=?", (cell,))

    conn.commit()
    conn.close()
    print("Seed data inserted.")

if __name__ == "__main__":
    seed()
