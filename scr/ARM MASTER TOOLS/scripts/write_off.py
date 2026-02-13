
import argparse
from src.services.tool_service import write_off

parser = argparse.ArgumentParser()
parser.add_argument("--tool", required=True)
parser.add_argument("--comment", default="Списан")
args = parser.parse_args()

write_off(args.tool, args.comment)
print("OK. Tool written off.")
