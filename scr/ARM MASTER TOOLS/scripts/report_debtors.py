
import argparse
from src.services.report_service import report_debtors

parser = argparse.ArgumentParser()
parser.add_argument("--days", type=int, default=3)
args = parser.parse_args()

df = report_debtors(args.days)
if df.empty:
    print("Должников нет.")
else:
    print(df.to_string(index=False))
