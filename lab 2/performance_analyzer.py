"""
Performance Analysis Module for Sorting Algorithms

This module provides tools for empirical analysis of different sorting algorithms.
It measures execution time, comparisons, and swaps for various input types and sizes.
"""

import time
import json
from typing import Dict, List, Callable, Tuple
from sorting_algorithms import SortingAlgorithms, DataGenerator


class PerformanceAnalyzer:
    """Analyzes and compares performance of different sorting algorithms."""
    
    def __init__(self):
        self.results = {}
        self.sorter = SortingAlgorithms()
    
    def measure_performance(self, algo_name: str, data: List[int], 
                          iterations: int = 3) -> Tuple[float, int, int]:
        """
        Measure execution time, comparisons, and swaps for a sorting algorithm.
        
        Args:
            algo_name: Name of the sorting algorithm ('quicksort', 'mergesort', etc.)
            data: Input data to sort
            iterations: Number of times to run (for averaging)
            
        Returns:
            Tuple of (average_time, comparisons, swaps)
        """
        total_time = 0
        total_comparisons = 0
        total_swaps = 0
        
        # Get the algorithm method from self.sorter
        algorithm = getattr(self.sorter, algo_name)
        
        for _ in range(iterations):
            test_data = data.copy()
            
            start_time = time.perf_counter()
            sorted_arr = algorithm(test_data)
            end_time = time.perf_counter()
            
            total_time += (end_time - start_time)
            comps, swps = self.sorter.get_metrics()
            total_comparisons += comps
            total_swaps += swps
        
        return (total_time / iterations, 
                total_comparisons // iterations, 
                total_swaps // iterations)
    
    def analyze_single_algorithm(self, algo_name: str,
                                 data_sizes: List[int], 
                                 data_type: str = "random") -> Dict:
        """
        Analyze a single algorithm across multiple input sizes.
        
        Args:
            algo_name: Name of the algorithm
            data_sizes: List of input sizes to test
            data_type: Type of data ('random', 'sorted', 'reverse', etc.)
            
        Returns:
            Dictionary mapping size -> metrics
        """
        print(f"\nAnalyzing {algo_name} with {data_type} data...")
        
        results = {}
        generator = DataGenerator()
        
        for size in data_sizes:
            # Generate appropriate data type
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
            else:
                data = generator.random_data(size)
            
            exec_time, comps, swaps = self.measure_performance(algo_name, data)
            results[size] = {
                'time': exec_time,
                'comparisons': comps,
                'swaps': swaps
            }
            
            print(f"  n={size:6d}: {exec_time:.6f}s, comps={comps:10d}, swaps={swaps:10d}")
        
        return results
    
    def compare_algorithms(self, data_sizes: List[int], 
                          data_type: str = "random",
                          iterations: int = 3) -> Dict:
        """
        Compare all algorithms across the same inputs.
        
        Args:
            data_sizes: List of input sizes to test
            data_type: Type of data to generate
            iterations: Number of iterations per test
            
        Returns:
            Nested dictionary: algorithm -> size -> metrics
        """
        print("=" * 80)
        print("SORTING ALGORITHMS - EMPIRICAL PERFORMANCE ANALYSIS")
        print("=" * 80)
        print(f"Input sizes: {data_sizes}")
        print(f"Data type: {data_type}")
        print(f"Iterations per test: {iterations}")
        print("=" * 80)
        
        algorithm_names = ['quicksort', 'mergesort', 'heapsort', 'insertion_sort']
        results = {}
        
        for algo_name in algorithm_names:
            results[algo_name] = self.analyze_single_algorithm(
                algo_name, data_sizes, data_type
            )
        
        self.results[data_type] = results
        return results
    
    def analyze_all_data_types(self, data_sizes: List[int]):
        """
        Analyze algorithms across different data types.
        
        Args:
            data_sizes: List of input sizes to test
        """
        data_types = ['random', 'sorted', 'reverse', 'nearly_sorted', 'duplicates']
        
        print("\n" + "=" * 80)
        print("COMPREHENSIVE ANALYSIS ACROSS ALL DATA TYPES")
        print("=" * 80)
        
        for data_type in data_types:
            self.compare_algorithms(data_sizes, data_type)
    
    def generate_comparison_table(self, data_type: str = "random", 
                                 metric: str = "time") -> str:
        """
        Generate a formatted comparison table.
        
        Args:
            data_type: Type of data to display
            metric: Metric to display ('time', 'comparisons', 'swaps')
            
        Returns:
            Formatted string table
        """
        if data_type not in self.results:
            return "No results available for this data type."
        
        results = self.results[data_type]
        
        # Get all sizes
        all_sizes = set()
        for algo_results in results.values():
            all_sizes.update(algo_results.keys())
        all_sizes = sorted(all_sizes)
        
        # Build table
        table = "\n" + "=" * 100 + "\n"
        table += f"PERFORMANCE COMPARISON - {data_type.upper()} DATA ({metric.upper()})\n"
        table += "=" * 100 + "\n"
        
        # Header
        header = f"{'Size':>8} |"
        for algo_name in results.keys():
            header += f" {algo_name:>18} |"
        table += header + "\n"
        table += "-" * 100 + "\n"
        
        # Rows
        for size in all_sizes:
            row = f"{size:>8} |"
            for algo_name in results.keys():
                if size in results[algo_name]:
                    value = results[algo_name][size][metric]
                    if metric == 'time':
                        row += f" {value:>18.6f} |"
                    else:
                        row += f" {value:>18,} |"
                else:
                    row += f" {'N/A':>18} |"
            table += row + "\n"
        
        table += "=" * 100 + "\n"
        
        return table
    
    def save_results(self, filename: str = "sorting_results.json"):
        """
        Save results to a JSON file.
        
        Args:
            filename: Output filename
        """
        # Convert results to serializable format
        serializable_results = {}
        for data_type, data_results in self.results.items():
            serializable_results[data_type] = {}
            for algo_name, algo_results in data_results.items():
                serializable_results[data_type][algo_name] = {
                    str(size): metrics
                    for size, metrics in algo_results.items()
                }
        
        with open(filename, 'w') as f:
            json.dump(serializable_results, f, indent=2)
        
        print(f"\nResults saved to {filename}")
    
    def find_fastest_algorithm(self, data_type: str, size: int) -> Tuple[str, float]:
        """
        Find the fastest algorithm for given data type and size.
        
        Args:
            data_type: Type of data
            size: Input size
            
        Returns:
            Tuple of (algorithm_name, execution_time)
        """
        if data_type not in self.results:
            return None, None
        
        fastest_algo = None
        fastest_time = float('inf')
        
        for algo_name, algo_results in self.results[data_type].items():
            if size in algo_results:
                time = algo_results[size]['time']
                if time < fastest_time:
                    fastest_time = time
                    fastest_algo = algo_name
        
        return fastest_algo, fastest_time
    
    def generate_summary(self) -> str:
        """
        Generate a text summary of the analysis.
        
        Returns:
            Formatted analysis summary
        """
        summary = "\n" + "=" * 80 + "\n"
        summary += "ANALYSIS SUMMARY\n"
        summary += "=" * 80 + "\n\n"
        
        # Algorithm characteristics
        summary += "Algorithm Characteristics:\n"
        summary += "-" * 80 + "\n"
        characteristics = {
            'quicksort': "O(n log n) avg | O(n²) worst | O(log n) space | Unstable | Fast",
            'mergesort': "O(n log n) always | O(n) space | Stable | Predictable",
            'heapsort': "O(n log n) always | O(1) space | Unstable | No worst case",
            'insertion_sort': "O(n²) avg | O(n) best | O(1) space | Stable | Good for small n"
        }
        
        for algo_name, char in characteristics.items():
            summary += f"{algo_name:20s}: {char}\n"
        
        summary += "\n" + "-" * 80 + "\n"
        summary += "Best Algorithm by Data Type:\n"
        summary += "-" * 80 + "\n"
        
        for data_type in self.results.keys():
            summary += f"\n{data_type.upper()}:\n"
            # Check for largest size
            all_sizes = set()
            for algo_results in self.results[data_type].values():
                all_sizes.update(algo_results.keys())
            
            if all_sizes:
                max_size = max(all_sizes)
                fastest, time = self.find_fastest_algorithm(data_type, max_size)
                if fastest:
                    summary += f"  Size {max_size}: {fastest} ({time:.6f}s)\n"
        
        summary += "\n" + "=" * 80 + "\n"
        
        return summary


if __name__ == "__main__":
    # Example usage
    analyzer = PerformanceAnalyzer()
    
    # Test with small, medium, and large sizes
    small_sizes = [100, 500, 1000, 2000]
    
    # Compare algorithms on random data
    results = analyzer.compare_algorithms(small_sizes, data_type="random")
    
    # Display results
    print(analyzer.generate_comparison_table(data_type="random", metric="time"))
    print(analyzer.generate_comparison_table(data_type="random", metric="comparisons"))
    print(analyzer.generate_summary())
    
    # Save results
    analyzer.save_results()
