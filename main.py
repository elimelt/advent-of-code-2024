from pathlib import Path
import importlib
import sys
from typing import Callable, List
import time
import psutil
import cProfile
import pstats
from io import StringIO
from datetime import datetime
from prettytable import PrettyTable


def format_time(seconds: float) -> str:
    if seconds < 0.001:
        return f"{seconds*1000000:.2f}µs"
    elif seconds < 1:
        return f"{seconds*1000:.2f}ms"
    else:
        return f"{seconds:.2f}s"


def format_memory(bytes: int) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if bytes < 1024:
            return f"{bytes:.1f}{unit}"
        bytes /= 1024
    return f"{bytes:.1f}TB"


class Solution:
    def __init__(self, day: str):
        self.day = day
        self.input_lines = self.load_input()
        self.part_one, self.part_two = self.get_solution_functions()

    def load_input(self) -> List[str]:
        input_path = Path("src") / f"day{self.day}" / "input.txt"
        try:
            return input_path.read_text().splitlines()
        except FileNotFoundError:
            sys.exit(f"Error: Input file not found at {input_path}")

    def get_solution_functions(self) -> tuple[Callable, Callable]:
        try:
            module = importlib.import_module(f"src.day{self.day}.sol")
            return module.part_one, module.part_two
        except (ImportError, AttributeError) as e:
            sys.exit(f"Error: Failed to load solution module - {e}")

    def run_with_profiling(self, func: Callable, part: int) -> tuple[any, float, float]:
        process = psutil.Process()
        mem_before = process.memory_info().rss

        pr = cProfile.Profile()
        start_time = time.perf_counter()
        pr.enable()
        result = func(self.input_lines.copy())
        pr.disable()
        elapsed_time = time.perf_counter() - start_time

        mem_after = process.memory_info().rss
        mem_used = mem_after - mem_before

        s = StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats("cumulative")
        ps.print_stats(10)

        profile_lines = s.getvalue().split("\n")
        clean_profile = []
        for line in profile_lines:
            if ":" in line and "(" in line:

                func_name = line.split("(")[-1].strip(")")
                parts = line.split()
                if len(parts) >= 6:

                    clean_line = f"{parts[0]:>8} {parts[1]:>8} {parts[2]:>8} {parts[3]:>8} {parts[4]:>8} {func_name}"
                    clean_profile.append(clean_line)
            else:
                clean_profile.append(line)

        return result, elapsed_time, mem_used, "\n".join(clean_profile)


def validate_day(day_arg: str) -> str:
    try:
        day_num = int(day_arg)
        return f"{day_num:02d}"
    except ValueError:
        sys.exit("Error: Day must be an integer")


def print_header(day: str) -> None:
    print("\n" + "=" * 60)
    print(f"🎄 Advent of Code 2023 - Day {day}")
    print(f"🕒 Running at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60 + "\n")


def print_results(
    part: int, result: any, time: float, memory: float, profile_data: str
) -> None:
    table = PrettyTable()
    table.field_names = ["Metric", "Value"]
    table.align["Metric"] = "l"
    table.align["Value"] = "r"

    table.add_row(["Result", result])
    table.add_row(["Time", format_time(time)])
    table.add_row(["Memory", format_memory(memory)])

    print(f"\n🎯 Part {part} Results:")
    print(table)

    print("\n📊 Profile Data (Top 10 functions):")
    print("-" * 60)
    print("   ncalls  tottime  percall  cumtime  percall  function")
    print("-" * 60)
    for line in profile_data.split("\n")[2:12]:
        if line.strip():
            print(line)
    print("-" * 60)


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("Usage: python script.py <day>")

    day = validate_day(sys.argv[1])
    solution = Solution(day)

    print_header(day)

    for part, func in enumerate([solution.part_one, solution.part_two], 1):
        result, time_taken, memory_used, profile_data = solution.run_with_profiling(
            func, part
        )
        print_results(part, result, time_taken, memory_used, profile_data)


if __name__ == "__main__":
    main()
