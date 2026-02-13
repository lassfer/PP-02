# MasterTool (прототип)

Это простой учебный проект на Python для учета инструмента в инструментально-раздаточной кладовой (ИРК).

## Что умеет
- Создавать SQLite базу данных
- Заполнять тестовыми данными (сотрудники, ячейки хранения, инструмент)
- Выполнять операции: приемка, выдача, возврат, списание
- Формировать простые отчеты (остатки, должники, топ инструментов)
- Экспортировать отчеты в CSV/JSON

## Структура проекта
- `src/` — исходники
- `scripts/` — скрипты запуска (инициализация БД, генерация данных, отчеты)
- `data/db/` — база SQLite
- `exports/` — выгрузки отчетов
- `logs/` — логи работы
- `backup/` — бэкапы БД
- `reports/` — отчеты/документация/референсы

## Быстрый старт
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

pip install -r requirements.txt

python scripts/init_db.py
python scripts/seed_data.py

python scripts/issue_tool.py --employee 1001 --tool T-0001
python scripts/return_tool.py --tool T-0001

python scripts/report_stock.py
python scripts/report_debtors.py --days 3
python scripts/export_reports.py
```
# PP-02
# PP-02
