
import argparse
from src.services.tool_service import accept_tool

parser = argparse.ArgumentParser()
parser.add_argument("--tool", required=True)
parser.add_argument("--name", required=True)
parser.add_argument("--type", required=True)
parser.add_argument("--diameter", type=float, default=None)
parser.add_argument("--material", default=None)
parser.add_argument("--life", type=int, default=None)

args = parser.parse_args()

cell = accept_tool(args.tool, args.name, args.type, args.diameter, args.material, args.life)
print(f"OK. Tool accepted. Cell: {cell}")
