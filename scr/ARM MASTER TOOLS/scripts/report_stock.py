
from src.services.report_service import report_stock

df = report_stock()
print(df.to_string(index=False))
