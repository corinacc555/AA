"""
main.py - Entry point for Lab 4: Dynamic Programming, Dijkstra and Floyd–Warshall.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from performance_analyzer import PerformanceAnalyzer, DEFAULT_SIZES, RESULTS_FILE
from visualizer import Visualizer
from interactive_visualizer import interactive_menu

BASE_DIR = Path(__file__).resolve().parent
QUICK_RESULTS_FILE = BASE_DIR / "lab4_results_quick.json"


def quick_test() -> None:
    analyzer = PerformanceAnalyzer()
    analyzer.run(sizes=[20, 40, 60], iterations=2)
    analyzer.print_summary()
    Visualizer(analyzer.results).plot_all()
    analyzer.save_results(QUICK_RESULTS_FILE)


def full_analysis() -> None:
    analyzer = PerformanceAnalyzer()
    analyzer.run(sizes=DEFAULT_SIZES, iterations=3)
    analyzer.print_summary()
    Visualizer(analyzer.results).plot_all()
    analyzer.save_results(RESULTS_FILE)


def load_and_plot() -> None:
    analyzer = PerformanceAnalyzer()
    analyzer.load_results(RESULTS_FILE)
    analyzer.print_summary()
    Visualizer(analyzer.results).plot_all()


def live_demo() -> None:
    interactive_menu()


def main() -> None:
    parser = argparse.ArgumentParser(description="Lab 4 - Dynamic Programming / Shortest Paths")
    parser.add_argument("--quick", action="store_true", help="Run a small fast analysis")
    parser.add_argument("--load", action="store_true", help="Load saved results and replot")
    parser.add_argument("--live", action="store_true", help="Run a real-time interactive demo")
    args = parser.parse_args()

    if args.live:
        live_demo()
    elif args.quick:
        quick_test()
    elif args.load:
        load_and_plot()
    else:
        full_analysis()


if __name__ == "__main__":
    main()
