# expired_orders.py
# Работа с просроченными заказами (JSON + отчеты)

from db_orders import load_orders, save_orders
from datetime import datetime, timedelta
import json
import csv

STORAGE_DAYS = 3  # Срок хранения на ПВЗ

def check_expired_orders():
    """Находит и отмечает просроченные заказы"""
    orders = load_orders()
    today = datetime.now()
    updated = False
    expired_list = []
    
    for order in orders:
        if order['status'] in ['ожидает', 'просрочен']:
            try:
                order_date = datetime.strptime(order['date'], "%Y-%m-%d")
                days_on_shelf = (today - order_date).days
                
                if days_on_shelf >= STORAGE_DAYS and order['status'] != 'просрочен':
                    order['status'] = 'просрочен'
                    order['expired_date'] = today.strftime("%Y-%m-%d")
                    updated = True
                    expired_list.append(order)
                    print(f"⚠️ Заказ {order['id']} просрочен! ({days_on_shelf} дней)")
            except:
                continue
    
    if updated:
        save_orders(orders)
        save_expired_report(expired_list)
    
    return expired_list

def save_expired_report(expired_orders):
    """Сохраняет отчет по просрочкам"""
    # Сохраняем в JSON
    report_data = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "count": len(expired_orders),
        "orders": expired_orders
    }
    
    filename = f"expired_{datetime.now().strftime('%Y%m%d')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)
    
    # Сохраняем в CSV для Excel
    csv_filename = f"expired_{datetime.now().strftime('%Y%m%d')}.csv"
    with open(csv_filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Номер заказа', 'ФИО', 'Телефон', 'Дата приема', 'Ячейка', 'Дней на ПВЗ'])
        
        for order in expired_orders:
            order_date = datetime.strptime(order['date'], "%Y-%m-%d")
            days = (datetime.now() - order_date).days
            writer.writerow([
                order['id'], 
                order['fio'], 
                order['phone'], 
                order['date'], 
                order['cell'],
                days
            ])
    
    print(f"📊 Отчет сохранен: {csv_filename}")

def show_statistics():
    """Показывает статистику по ПВЗ"""
    orders = load_orders()
    total = len(orders)
    waiting = len([o for o in orders if o['status'] == 'ожидает'])
    issued = len([o for o in orders if o['status'] == 'выдан'])
    expired = len([o for o in orders if o['status'] == 'просрочен'])
    
    print("\n📊 СТАТИСТИКА ПВЗ")
    print("=" * 40)
    print(f"📦 Всего заказов: {total}")
    print(f"⏳ Ожидают выдачи: {waiting}")
    print(f"✅ Выдано: {issued}")
    print(f"⚠️ Просрочено: {expired}")
    print(f"📈 Загрузка: {int((waiting+expired)/30*100)}%")
    print("=" * 40)
    
    # Сохраняем статистику
    stats = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "total": total,
        "waiting": waiting,
        "issued": issued,
        "expired": expired
    }
    
    with open("statistics.json", 'a', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False)
        f.write("\n")

def main():
    print("⏰ ПРОВЕРКА ПРОСРОЧЕННЫХ ЗАКАЗОВ")
    print(f"📅 Сегодня: {datetime.now().strftime('%d.%m.%Y')}")
    print(f"⚡ Срок хранения: {STORAGE_DAYS} дня")
    
    # Проверяем просрочки
    expired = check_expired_orders()
    
    if expired:
        print(f"\n⚠️ Найдено просрочек: {len(expired)}")
        
        # Предлагаем сформировать акт возврата
        answer = input("\nСформировать акт возврата? (да/нет): ")
        if answer.lower() == 'да':
            from datetime import datetime
            filename = f"return_act_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("АКТ ВОЗВРАТА ТОВАРА\n")
                f.write("=" * 50 + "\n")
                f.write(f"Дата: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n")
                f.write(f"ПВЗ: Ozon\n")
                f.write("=" * 50 + "\n\n")
                
                for order in expired:
                    f.write(f"Заказ №{order['id']}\n")
                    f.write(f"Клиент: {order['fio']}\n")
                    f.write(f"Ячейка: {order['cell']}\n")
                    f.write(f"Дата приема: {order['date']}\n")
                    f.write("-" * 30 + "\n")
            
            print(f"✅ Акт сохранен: {filename}")
    else:
        print("✅ Просроченных заказов нет")
    
    # Показываем статистику
    show_statistics()

if __name__ == "__main__":
    main()