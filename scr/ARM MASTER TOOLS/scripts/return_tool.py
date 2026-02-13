
import argparse
from src.services.tool_service import return_tool

parser = argparse.ArgumentParser()
parser.add_argument("--tool", required=True)
args = parser.parse_args()

cell = return_tool(args.tool)
print(f"OK. Tool returned. Cell: {cell}")
