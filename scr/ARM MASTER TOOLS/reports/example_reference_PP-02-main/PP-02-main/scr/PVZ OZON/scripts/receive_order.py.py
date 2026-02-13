# receive_order.py
# Приемка новых заказов с сохранением в JSON

from db_orders import load_orders, save_orders, add_order
from datetime import datetime, timedelta
import random

# Все доступные ячейки
CELLS = [f"{row}{i:02d}" for row in ['A','B','C','D'] for i in range(1, 11)]

def get_free_cell():
    """Находит первую свободную ячейку"""
    orders = load_orders()
    occupied_cells = [order['cell'] for order in orders 
                     if order['status'] in ['ожидает', 'просрочен']]
    
    for cell in CELLS:
        if cell not in occupied_cells:
            return cell
    return None

def generate_order_id():
    """Генерирует номер заказа"""
    return str(random.randint(10000, 99999))

def receive_new_order():
    """Принимает новый заказ от курьера"""
    print("\n📦 ПРИЕМКА НОВОГО ЗАКАЗА")
    print("-" * 40)
    
    # Генерируем номер заказа
    order_id = generate_order_id()
    print(f"🔢 Номер заказа: {order_id}")
    
    # Ввод данных клиента
    fio = input("👤 ФИО клиента: ")
    phone = input("📱 Телефон: ")
    
    # Поиск свободной ячейки
    cell = get_free_cell()
    if not cell:
        print("❌ Нет свободных ячеек!")
        return
    
    # Создаем заказ
    new_order = {
        "id": order_id,
        "fio": fio,
        "phone": phone,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "cell": cell,
        "status": "ожидает",
        "received_by": "Оператор Иванова",
        "received_time": datetime.now().strftime("%H:%M")
    }
    
    # Сохраняем в JSON
    add_order(new_order)
    
    print(f"📍 Ячейка: {cell}")
    print("✅ Заказ успешно принят!")
    
    # Сохраняем в CSV отчет
    save_to_csv(new_order)

def save_to_csv(order):
    """Сохраняет информацию о приемке в CSV файл"""
    filename = "received_orders.csv"
    file_exists = False
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            file_exists = True
    except FileNotFoundError:
        pass
    
    with open(filename, 'a', encoding='utf-8') as f:
        if not file_exists:
            f.write("Дата,Номер заказа,ФИО,Телефон,Ячейка,Время приема\n")
        
        f.write(f"{order['date']},{order['id']},{order['fio']},"
                f"{order['phone']},{order['cell']},{order['received_time']}\n")
    
    print(f"📊 Данные сохранены в {filename}")

def main():
    while True:
        print("\n1. Принять новый заказ")
        print("2. Показать все заказы")
        print("3. Выход")
        
        choice = input("\nВыберите действие: ")
        
        if choice == '1':
            receive_new_order()
        elif choice == '2':
            orders = load_orders()
            print(f"\n📋 Всего заказов: {len(orders)}")
            print("-" * 40)
            for order in orders[:5]:  # Показываем первые 5
                print(f"№{order['id']} - {order['fio']} - {order['cell']} - {order['status']}")
        elif choice == '3':
            print("👋 До свидания!")
            break

if __name__ == "__main__":
    main()