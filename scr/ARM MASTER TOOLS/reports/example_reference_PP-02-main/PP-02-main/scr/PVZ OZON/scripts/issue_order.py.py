# issue_order.py
# Выдача заказа с обновлением JSON

from db_orders import load_orders, save_orders, find_orders, update_order
from datetime import datetime
import csv

def issue_order_by_id(order_id):
    """Оформляет выдачу заказа"""
    orders = load_orders()
    
    for order in orders:
        if order['id'] == order_id:
            if order['status'] == 'выдан':
                print("⚠️ Заказ уже был выдан")
                return False
            
            # Обновляем данные заказа
            order['status'] = 'выдан'
            order['issue_date'] = datetime.now().strftime("%Y-%m-%d")
            order['issue_time'] = datetime.now().strftime("%H:%M")
            order['issued_by'] = "Оператор Иванова"
            
            # Сохраняем изменения
            save_orders(orders)
            
            # Записываем в историю выдач
            save_to_issue_history(order)
            
            print(f"✅ Заказ {order_id} выдан")
            print(f"📅 {order['issue_date']} {order['issue_time']}")
            
            # Отправляем СМС (имитация)
            send_sms(order['phone'], order_id)
            
            return True
    
    print("❌ Заказ не найден")
    return False

def save_to_issue_history(order):
    """Сохраняет информацию о выдаче в CSV"""
    filename = "issue_history.csv"
    file_exists = False
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            file_exists = True
    except FileNotFoundError:
        pass
    
    with open(filename, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Дата', 'Время', 'Номер заказа', 'ФИО', 'Телефон', 'Оператор'])
        
        writer.writerow([
            order['issue_date'],
            order['issue_time'],
            order['id'],
            order['fio'],
            order['phone'],
            order['issued_by']
        ])

def send_sms(phone, order_id):
    """Имитация отправки СМС"""
    print(f"📱 СМС отправлено на {phone}")
    print(f"   Ваш заказ №{order_id} получен. Спасибо!")

def show_issued_today():
    """Показывает выданные сегодня заказы"""
    today = datetime.now().strftime("%Y-%m-%d")
    orders = load_orders()
    
    issued_today = [o for o in orders 
                   if o.get('status') == 'выдан' 
                   and o.get('issue_date') == today]
    
    print(f"\n📊 ВЫДАНО СЕГОДНЯ: {len(issued_today)} заказов")
    print("-" * 40)
    for order in issued_today:
        print(f"{order['issue_time']} - №{order['id']} - {order['fio']}")

def main():
    print("📦 ВЫДАЧА ЗАКАЗОВ")
    
    while True:
        print("\n1. Выдать заказ по номеру")
        print("2. Поиск заказа")
        print("3. Выданные сегодня")
        print("4. Выход")
        
        choice = input("\nВыберите действие: ")
        
        if choice == '1':
            order_id = input("Введите номер заказа: ")
            issue_order_by_id(order_id)
        
        elif choice == '2':
            search = input("Поиск (номер/ФИО/телефон): ")
            results = find_orders(search)
            print(f"\nНайдено: {len(results)}")
            for order in results:
                status = "✅" if order['status'] == 'выдан' else "⏳"
                print(f"{status} №{order['id']} - {order['fio']} - {order['status']}")
        
        elif choice == '3':
            show_issued_today()
        
        elif choice == '4':
            break

if __name__ == "__main__":
    main()