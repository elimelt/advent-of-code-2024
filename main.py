from pathlib import Path
import importlib
import sys
from typing import Callable, List

def validate_day(day_arg: str) -> str:
    try:
        day_num = int(day_arg)
        return f"{day_num:02d}"
    except ValueError:
        sys.exit("Error: Day must be an integer")

def load_input(day: str) -> List[str]:
    input_path = Path("src") / f"day{day}" / "input.txt"
    try:
        return input_path.read_text().splitlines()
    except FileNotFoundError:
        sys.exit(f"Error: Input file not found at {input_path}")

def get_solution_functions(day: str) -> tuple[Callable, Callable]:
    try:
        module = importlib.import_module(f"src.day{day}.sol")
        return module.part_one, module.part_two
    except (ImportError, AttributeError) as e:
        sys.exit(f"Error: Failed to load solution module - {e}")

def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("Usage: python script.py <day>")

    day = validate_day(sys.argv[1])
    input_lines = load_input(day)
    part_one, part_two = get_solution_functions(day)

    print(part_one(input_lines))
    print(part_two(input_lines))

if __name__ == "__main__":
    main()