"""
Laboratory Work 1: Main Execution Script
Study and Empirical Analysis of Algorithms for Determining Fibonacci N-th Term

This is the main script that runs the complete analysis.
"""

import sys
from performance_analyzer import PerformanceAnalyzer
from visualizer import ResultsVisualizer
from fibonacci_algorithms import ALGORITHMS


def print_header():
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(" " * 20 + "LABORATORY WORK 1")
    print(" " * 10 + "Study and Empirical Analysis of Algorithms for")
    print(" " * 15 + "Determining Fibonacci N-th Term")
    print("=" * 80 + "\n")


def print_algorithms_info():
    """Display information about implemented algorithms."""
    print("\nIMPLEMENTED ALGORITHMS:")
    print("-" * 80)
    
    algorithms_info = [
        ("1. Naive Recursive", "O(2^n)", "Simple recursion, exponential time"),
        ("2. Iterative", "O(n)", "Loop-based, constant space"),
        ("3. Recursive with Memoization", "O(n)", "Cached recursion, dynamic programming"),
        ("4. Matrix Exponentiation", "O(log n)", "Fast matrix power, logarithmic time"),
        ("5. Dynamic Programming", "O(n)", "Bottom-up table, stores all values"),
        ("6. Binet's Formula", "O(1)", "Closed-form mathematical formula")
    ]
    
    print(f"{'Algorithm':<35} {'Complexity':<15} {'Description'}")
    print("-" * 80)
    for name, complexity, desc in algorithms_info:
        print(f"{name:<35} {complexity:<15} {desc}")
    print("-" * 80 + "\n")


def get_test_inputs():
    """
    Define test input properties.
    
    Input Format Properties:
    - Small inputs (n ≤ 20): Test all algorithms including naive recursive
    - Medium inputs (20 < n ≤ 35): Test all except very slow naive recursive
    - Large inputs (n > 35): Test only efficient algorithms
    - Coverage: Both sparse and dense ranges to observe growth patterns
    """
    print("\nINPUT FORMAT PROPERTIES:")
    print("-" * 80)
    print("Test cases are designed to reveal algorithm behavior across different scales:")
    print("  • Small range (5-20):    All algorithms including exponential")
    print("  • Medium range (20-35):  Excludes naive recursive (too slow)")
    print("  • Large range (50-200):  Only efficient algorithms")
    print("  • Very large (500-1000): Stress test for O(log n) and O(1)")
    print("-" * 80)
    
    # Define comprehensive test inputs
    small_inputs = list(range(5, 21, 5))      # [5, 10, 15, 20]
    medium_inputs = list(range(25, 36, 5))    # [25, 30, 35]
    large_inputs = [50, 100, 150, 200]        # Large values
    very_large = [500, 1000]                   # Very large values
    
    all_inputs = small_inputs + medium_inputs + large_inputs + very_large
    
    return all_inputs


def run_analysis():
    """Run the complete performance analysis."""
    print_header()
    print_algorithms_info()
    
    # Get test inputs
    test_inputs = get_test_inputs()
    
    print("\nCOMPARISON METRIC:")
    print("-" * 80)
    print("Primary Metric: EXECUTION TIME (wall-clock time in seconds)")
    print("  • Measured using Python's time.perf_counter() for high precision")
    print("  • Each test averaged over 3 iterations for reliability")
    print("  • Captures real-world performance including overhead")
    print("-" * 80)
    
    # Initialize analyzer
    analyzer = PerformanceAnalyzer()
    
    # Run performance comparison
    print("\n" + "=" * 80)
    print("STARTING EMPIRICAL ANALYSIS")
    print("=" * 80)
    
    # Get all algorithm names
    algorithm_names = list(ALGORITHMS.keys())
    
    # Run analysis
    results = analyzer.compare_algorithms(
        test_inputs=test_inputs,
        algorithm_names=algorithm_names,
        iterations=3
    )
    
    # Display results
    print("\n" + "=" * 80)
    print("RESULTS")
    print("=" * 80)
    print(analyzer.generate_comparison_table())
    print(analyzer.generate_analysis_summary())
    
    # Save results
    analyzer.save_results("performance_results.json")
    
    # Generate visualizations
    print("\n" + "=" * 80)
    print("GENERATING VISUAL PRESENTATIONS")
    print("=" * 80)
    
    visualizer = ResultsVisualizer(results)
    visualizer.create_all_plots()
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE!")
    print("=" * 80)
    print("\nGenerated files:")
    print("  • performance_results.json - Raw performance data")
    print("  • all_algorithms_comparison.png - All algorithms on linear scale")
    print("  • algorithms_log_scale.png - Logarithmic scale comparison")
    print("  • efficient_algorithms.png - Efficient algorithms only")
    print("  • complexity_comparison.png - Complexity class breakdown")
    print("\nPlease see README.md for detailed conclusions and analysis.")
    print("=" * 80 + "\n")


def quick_test():
    """Quick test of all algorithms with a small value."""
    print("\n" + "=" * 80)
    print("QUICK VERIFICATION TEST")
    print("=" * 80)
    
    n = 10
    print(f"\nTesting all algorithms with n={n}:")
    print(f"Expected result: F({n}) = 55")
    print("-" * 80)
    
    from fibonacci_algorithms import clear_memoization_cache
    
    for name, func in ALGORITHMS.items():
        if name == 'recursive_memoized':
            clear_memoization_cache()
        
        result = func(n)
        status = "✓" if result == 55 else "✗"
        print(f"{status} {name:30s}: {result}")
    
    print("-" * 80)
    print("All algorithms verified!\n")


def interactive_mode():
    """Interactive mode for testing individual algorithms."""
    print("\n" + "=" * 80)
    print("INTERACTIVE MODE")
    print("=" * 80)
    
    while True:
        print("\nOptions:")
        print("  1. Calculate Fibonacci number")
        print("  2. Compare algorithms for a specific n")
        print("  3. Run full analysis")
        print("  4. Quick test")
        print("  5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            try:
                n = int(input("Enter n: "))
                print("\nAvailable algorithms:")
                for idx, name in enumerate(ALGORITHMS.keys(), 1):
                    print(f"  {idx}. {name}")
                
                algo_choice = int(input("Select algorithm (1-6): ")) - 1
                algo_name = list(ALGORITHMS.keys())[algo_choice]
                
                from fibonacci_algorithms import clear_memoization_cache
                if algo_name == 'recursive_memoized':
                    clear_memoization_cache()
                
                result = ALGORITHMS[algo_name](n)
                print(f"\nF({n}) = {result}")
                
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice == '2':
            try:
                n = int(input("Enter n: "))
                analyzer = PerformanceAnalyzer()
                results = analyzer.compare_algorithms([n], iterations=3)
                print(analyzer.generate_comparison_table())
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice == '3':
            run_analysis()
            
        elif choice == '4':
            quick_test()
            
        elif choice == '5':
            print("\nExiting... Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        if sys.argv[1] == '--quick':
            quick_test()
        elif sys.argv[1] == '--interactive':
            interactive_mode()
        elif sys.argv[1] == '--help':
            print("\nUsage: python main.py [options]")
            print("\nOptions:")
            print("  (no args)      Run full analysis")
            print("  --quick        Quick verification test")
            print("  --interactive  Interactive mode")
            print("  --help         Show this help message")
        else:
            print(f"Unknown option: {sys.argv[1]}")
            print("Use --help for usage information")
    else:
        # Default: run full analysis
        run_analysis()


if __name__ == "__main__":
    main()
