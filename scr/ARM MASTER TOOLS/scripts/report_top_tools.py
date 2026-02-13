
from src.services.report_service import report_top_tools

df = report_top_tools()
print(df.to_string(index=False))
