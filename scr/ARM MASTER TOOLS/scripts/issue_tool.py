
import argparse
from src.services.tool_service import issue_tool

parser = argparse.ArgumentParser()
parser.add_argument("--employee", type=int, required=True)
parser.add_argument("--tool", required=True)
args = parser.parse_args()

issue_tool(args.tool, args.employee)
print("OK. Tool issued.")
