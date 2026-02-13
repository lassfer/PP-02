
from pathlib import Path
from src.services.report_service import report_stock, report_debtors, report_top_tools

EXPORT_DIR = Path(__file__).resolve().parents[1] / "exports"

def export():
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    stock = report_stock()
    debtors = report_debtors(3)
    top = report_top_tools()

    stock.to_csv(EXPORT_DIR / "stock.csv", index=False)
    debtors.to_csv(EXPORT_DIR / "debtors.csv", index=False)
    top.to_csv(EXPORT_DIR / "top_tools.csv", index=False)

    stock.to_json(EXPORT_DIR / "stock.json", orient="records", force_ascii=False, indent=2)
    debtors.to_json(EXPORT_DIR / "debtors.json", orient="records", force_ascii=False, indent=2)
    top.to_json(EXPORT_DIR / "top_tools.json", orient="records", force_ascii=False, indent=2)

    print("Reports exported to exports/")

if __name__ == "__main__":
    export()
