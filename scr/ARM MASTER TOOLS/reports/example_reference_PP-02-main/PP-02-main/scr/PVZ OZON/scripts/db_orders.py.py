# db_orders.py
# Работа с JSON файлом для хранения заказов

import json
import os
from datetime import datetime

DB_FILE = "orders.json"

def init_db():
    """Создает файл базы данных, если его нет"""
    if not os.path.exists(DB_FILE):
        # Начальные тестовые данные
        initial_orders = [
            {"id": "12345", "fio": "Иванов Иван", "phone": "79991234567", 
             "date": "2026-02-10", "cell": "A12", "status": "ожидает"},
            {"id": "12346", "fio": "Петров Петр", "phone": "79992345678", 
             "date": "2026-02-11", "cell": "B05", "status": "ожидает"},
            {"id": "12347", "fio": "Сидорова Анна", "phone": "79993456789", 
             "date": "2026-02-09", "cell": "C08", "status": "выдан"},
            {"id": "12348", "fio": "Иванова Мария", "phone": "79994567890", 
             "date": "2026-02-10", "cell": "A15", "status": "ожидает"},
            {"id": "12349", "fio": "Смирнов Алексей", "phone": "79995678901", 
             "date": "2026-02-08", "cell": "B10", "status": "просрочен"},
        ]
        save_orders(initial_orders)
        print(f"✅ Создана база данных: {DB_FILE}")

def load_orders():
    """Загружает заказы из JSON файла"""
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        init_db()
        return load_orders()
    except json.JSONDecodeError:
        print("❌ Ошибка чтения файла. Создаю новый...")
        init_db()
        return load_orders()

def save_orders(orders):
    """Сохраняет заказы в JSON файл"""
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)

def add_order(order):
    """Добавляет новый заказ"""
    orders = load_orders()
    orders.append(order)
    save_orders(orders)
    print(f"✅ Заказ {order['id']} добавлен в базу")

def update_order(order_id, new_data):
    """Обновляет данные заказа"""
    orders = load_orders()
    for order in orders:
        if order['id'] == order_id:
            order.update(new_data)
            save_orders(orders)
            print(f"✅ Заказ {order_id} обновлен")
            return True
    return False

def find_orders(search_term):
    """Ищет заказы по тексту"""
    orders = load_orders()
    results = []
    search_term = search_term.lower()
    
    for order in orders:
        if (search_term in order['id'].lower() or 
            search_term in order['fio'].lower() or
            search_term in order['phone']):
            results.append(order)
    
    return results

# Инициализация при первом запуске
init_db()