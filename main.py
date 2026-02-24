"""
Laboratory Work 2AA: Study and Empirical Analysis of Sorting Algorithms

This module provides the main entry point for analyzing sorting algorithms.

Usage:
    python main.py              # Full analysis with visualizations
    python main.py --quick      # Quick verification test
    python main.py --interactive # Interactive mode
"""

import argparse
import sys
from sorting_algorithms import SortingAlgorithms, DataGenerator
from performance_analyzer import PerformanceAnalyzer
from visualizer import ResultsVisualizer


def quick_test():
    """Quick verification that all algorithms work correctly."""
    print("=" * 60)
    print("QUICK VERIFICATION TEST")
    print("=" * 60)
    
    test_data = [64, 34, 25, 12, 22, 11, 90, 88, 45, 50, 30, 17, 28, 40]
    print(f"\nOriginal array: {test_data}")
    print("-" * 60)
    
    sorter = SortingAlgorithms()
    algorithms = ['quicksort', 'mergesort', 'heapsort', 'insertion_sort']
    
    for algo_name in algorithms:
        data_copy = test_data.copy()
        algo_func = getattr(sorter, algo_name)
        sorted_data = algo_func(data_copy)
        
        is_sorted = sorted_data == sorted(test_data)
        status = "✓ PASS" if is_sorted else "✗ FAIL"
        
        print(f"{algo_name:15s}: {status}")
        print(f"  Comparisons: {sorter.comparisons:6d}")
        print(f"  Swaps:       {sorter.swaps:6d}")
        print(f"  Result: {sorted_data[:5]}...{sorted_data[-3:]}")
        print()
    
    print("=" * 60)
    print("Verification complete!")


def interactive_mode():
    """Interactive mode for custom testing."""
    print("=" * 60)
    print("INTERACTIVE MODE")
    print("=" * 60)
    
    analyzer = PerformanceAnalyzer()
    
    print("\nAvailable algorithms:")
    print("1. QuickSort")
    print("2. MergeSort")
    print("3. HeapSort")
    print("4. InsertionSort")
    
    algo_map = {
        '1': 'quicksort',
        '2': 'mergesort',
        '3': 'heapsort',
        '4': 'insertion_sort'
    }
    
    print("\nAvailable data types:")
    print("1. Random")
    print("2. Sorted")
    print("3. Reverse sorted")
    print("4. Nearly sorted")
    print("5. Many duplicates")
    
    data_map = {
        '1': 'random',
        '2': 'sorted',
        '3': 'reverse',
        '4': 'nearly_sorted',
        '5': 'duplicates'
    }
    
    while True:
        print("\n" + "-" * 60)
        algo_choice = input("\nSelect algorithm (1-4, or 'q' to quit): ").strip()
        
        if algo_choice.lower() == 'q':
            print("Exiting interactive mode...")
            break
        
        if algo_choice not in algo_map:
            print("Invalid choice! Please select 1-4.")
            continue
        
        data_choice = input("Select data type (1-5): ").strip()
        if data_choice not in data_map:
            print("Invalid choice! Please select 1-5.")
            continue
        
        try:
            size = int(input("Enter array size (e.g., 1000): ").strip())
            if size <= 0:
                print("Size must be positive!")
                continue
        except ValueError:
            print("Invalid size!")
            continue
        
        algorithm = algo_map[algo_choice]
        data_type = data_map[data_choice]
        
        print(f"\nTesting {algorithm} on {data_type} data (size={size})...")
        print("Running 5 iterations...")
        
        # Generate appropriate data
        generator = DataGenerator()
        if data_type == "random":
            data = generator.random_data(size)
        elif data_type == "sorted":
            data = generator.sorted_data(size)
        elif data_type == "reverse":
            data = generator.reverse_sorted_data(size)
        elif data_type == "nearly_sorted":
            data = generator.nearly_sorted_data(size)
        elif data_type == "duplicates":
            data = generator.duplicate_data(size)
        
        exec_time, comps, swaps = analyzer.measure_performance(algorithm, data, iterations=5)
        
        print(f"\nResults:")
        print(f"  Average Time:        {exec_time:.6f} seconds")
        print(f"  Average Comparisons: {comps:,}")
        print(f"  Average Swaps:       {swaps:,}")


def full_analysis():
    """Run complete performance analysis with visualizations."""
    print("=" * 60)
    print("LABORATORY WORK 2AA")
    print("Study and Empirical Analysis of Sorting Algorithms")
    print("=" * 60)
    
    print("\nAnalyzing algorithms:")
    print("  - QuickSort")
    print("  - MergeSort")
    print("  - HeapSort")
    print("  - InsertionSort")
    
    print("\nData types:")
    print("  - Random arrays")
    print("  - Already sorted arrays")
    print("  - Reverse sorted arrays")
    print("  - Nearly sorted arrays")
    print("  - Arrays with many duplicates")
    
    print("\nInput sizes: 100, 500, 1000, 2000")
    print("\n" + "=" * 60)
    
    # Initialize analyzer
    analyzer = PerformanceAnalyzer()
    
    # Define test parameters (reduced for faster execution)
    sizes = [100, 500, 1000, 2000]
    
    # Run comprehensive analysis
    print("\nStarting comprehensive analysis...")
    print("This may take several minutes...")
    print("-" * 60)
    
    analyzer.analyze_all_data_types(sizes)
    
    # Save results
    print("\nSaving results to JSON...")
    analyzer.save_results("sorting_results.json")
    
    # Generate summary
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)
    
    summary = analyzer.generate_summary()
    print(summary)
    
    # Create visualizations
    print("\n" + "=" * 60)
    print("GENERATING VISUALIZATIONS")
    print("=" * 60)
    
    visualizer = ResultsVisualizer(analyzer.results)
    visualizer.create_all_plots()
    
    print("\n" + "=" * 60)
    print("ALL TASKS COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\nGenerated files:")
    print("  - sorting_results.json (raw data)")
    print("  - *.png (visualization plots)")
    print("\nReview the graphs and results for detailed analysis.")


def main():
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(
        description='Laboratory Work 2AA: Sorting Algorithms Analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py              # Run full analysis
  python main.py --quick      # Quick verification
  python main.py --interactive # Interactive testing
        """
    )
    
    parser.add_argument(
        '--quick',
        action='store_true',
        help='Run quick verification test only'
    )
    
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Run in interactive mode'
    )
    
    args = parser.parse_args()
    
    try:
        if args.quick:
            quick_test()
        elif args.interactive:
            interactive_mode()
        else:
            full_analysis()
    
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
