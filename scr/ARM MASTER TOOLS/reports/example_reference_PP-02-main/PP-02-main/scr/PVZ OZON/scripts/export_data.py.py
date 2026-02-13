# export_data.py
# Экспорт данных в разные форматы

from db_orders import load_orders
from datetime import datetime
import json
import csv

def export_to_json():
    """Экспорт всех заказов в JSON"""
    orders = load_orders()
    filename = f"orders_backup_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Экспорт в JSON: {filename}")
    return filename

def export_to_csv():
    """Экспорт всех заказов в CSV (Excel)"""
    orders = load_orders()
    filename = f"orders_{datetime.now().strftime('%Y%m%d')}.csv"
    
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        if orders:
            writer = csv.DictWriter(f, fieldnames=orders[0].keys())
            writer.writeheader()
            writer.writerows(orders)
    
    print(f"✅ Экспорт в CSV: {filename}")
    return filename

def export_daily_report():
    """Создает ежедневный отчет"""
    orders = load_orders()
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Фильтруем заказы за сегодня
    received_today = [o for o in orders if o['date'] == today]
    issued_today = [o for o in orders if o.get('issue_date') == today]
    
    report = {
        "date": today,
        "received": len(received_today),
        "issued": len(issued_today),
        "total_orders": len(orders),
        "received_list": received_today[:10],  # первые 10
        "issued_list": issued_today[:10]
    }
    
    # Сохраняем отчет
    filename = f"daily_report_{today}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    # Сохраняем в текстовый файл для чтения
    txt_filename = f"daily_report_{today}.txt"
    with open(txt_filename, 'w', encoding='utf-8') as f:
        f.write(f"ОТЧЕТ ПВЗ OZON\n")
        f.write(f"Дата: {today}\n")
        f.write("=" * 50 + "\n")
        f.write(f"📦 Принято заказов: {len(received_today)}\n")
        f.write(f"✅ Выдано заказов: {len(issued_today)}\n")
        f.write(f"📊 Всего в системе: {len(orders)}\n")
        f.write("=" * 50 + "\n")
        
        if received_today:
            f.write("\nПРИНЯТО СЕГОДНЯ:\n")
            for o in received_today[:5]:
                f.write(f"  • {o['id']} - {o['fio']} - яч.{o['cell']}\n")
        
        if issued_today:
            f.write("\nВЫДАНО СЕГОДНЯ:\n")
            for o in issued_today[:5]:
                f.write(f"  • {o['id']} - {o['fio']}\n")
    
    print(f"✅ Отчет сохранен: {txt_filename}")
    return txt_filename

def main():
    print("📊 ЭКСПОРТ ДАННЫХ")
    print("1. Экспорт в JSON (бэкап)")
    print("2. Экспорт в CSV (Excel)")
    print("3. Создать дневной отчет")
    print("4. Все форматы сразу")
    
    choice = input("\nВыберите действие: ")
    
    if choice == '1':
        export_to_json()
    elif choice == '2':
        export_to_csv()
    elif choice == '3':
        export_daily_report()
    elif choice == '4':
        export_to_json()
        export_to_csv()
        export_daily_report()
        print("✅ Все файлы сохранены!")

if __name__ == "__main__":
    main()