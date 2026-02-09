"""
Performance Analysis Module for Fibonacci Algorithms

This module provides tools for empirical analysis of different Fibonacci algorithms.
It measures execution time and compares algorithm performance.
"""

import time
import sys
from typing import Dict, List, Callable, Tuple
import json
from fibonacci_algorithms import ALGORITHMS, clear_memoization_cache


class PerformanceAnalyzer:
    """Analyzes and compares performance of different algorithms."""
    
    def __init__(self):
        self.results = {}
    
    def measure_execution_time(self, func: Callable, n: int, iterations: int = 1) -> float:
        """
        Measure the execution time of a function.
        
        Args:
            func: The function to measure
            n: The input parameter
            iterations: Number of times to run (for averaging)
            
        Returns:
            Average execution time in seconds
        """
        total_time = 0
        
        for _ in range(iterations):
            start_time = time.perf_counter()
            try:
                result = func(n)
                end_time = time.perf_counter()
                total_time += (end_time - start_time)
            except RecursionError:
                return float('inf')  # Indicates stack overflow
            except Exception as e:
                print(f"Error: {e}")
                return float('inf')
        
        return total_time / iterations
    
    def analyze_algorithm(self, algorithm_name: str, test_inputs: List[int], 
                         iterations: int = 3) -> Dict[int, float]:
        """
        Analyze a single algorithm across multiple inputs.
        
        Args:
            algorithm_name: Name of the algorithm to test
            test_inputs: List of n values to test
            iterations: Number of iterations for each test
            
        Returns:
            Dictionary mapping input -> execution time
        """
        func = ALGORITHMS[algorithm_name]
        results = {}
        
        print(f"\nTesting {algorithm_name}...")
        
        for n in test_inputs:
            # Clear cache for memoized version
            if algorithm_name == 'recursive_memoized':
                clear_memoization_cache()
            
            # Skip naive recursive for large values (too slow)
            if algorithm_name == 'recursive_naive' and n > 35:
                results[n] = None  # Too slow to measure
                print(f"  n={n:3d}: Skipped (too slow)")
                continue
            
            exec_time = self.measure_execution_time(func, n, iterations)
            results[n] = exec_time
            
            if exec_time == float('inf'):
                print(f"  n={n:3d}: Error (recursion limit or timeout)")
            else:
                print(f"  n={n:3d}: {exec_time:.6f} seconds")
        
        return results
    
    def compare_algorithms(self, test_inputs: List[int], 
                          algorithm_names: List[str] = None,
                          iterations: int = 3) -> Dict[str, Dict[int, float]]:
        """
        Compare multiple algorithms across the same inputs.
        
        Args:
            test_inputs: List of n values to test
            algorithm_names: List of algorithm names (None = all)
            iterations: Number of iterations per test
            
        Returns:
            Nested dictionary: algorithm_name -> {input -> time}
        """
        if algorithm_names is None:
            algorithm_names = list(ALGORITHMS.keys())
        
        print("=" * 70)
        print("FIBONACCI ALGORITHMS - EMPIRICAL PERFORMANCE ANALYSIS")
        print("=" * 70)
        print(f"Test inputs (n): {test_inputs}")
        print(f"Iterations per test: {iterations}")
        print("=" * 70)
        
        results = {}
        for algo_name in algorithm_names:
            results[algo_name] = self.analyze_algorithm(algo_name, test_inputs, iterations)
        
        self.results = results
        return results
    
    def generate_comparison_table(self) -> str:
        """
        Generate a formatted comparison table of results.
        
        Returns:
            Formatted string table
        """
        if not self.results:
            return "No results available. Run compare_algorithms first."
        
        # Get all test inputs
        all_inputs = set()
        for algo_results in self.results.values():
            all_inputs.update(algo_results.keys())
        all_inputs = sorted(all_inputs)
        
        # Build table
        table = "\n" + "=" * 100 + "\n"
        table += "PERFORMANCE COMPARISON TABLE (Execution Time in Seconds)\n"
        table += "=" * 100 + "\n"
        
        # Header
        header = f"{'n':>5} |"
        for algo_name in self.results.keys():
            header += f" {algo_name:>20} |"
        table += header + "\n"
        table += "-" * 100 + "\n"
        
        # Rows
        for n in all_inputs:
            row = f"{n:>5} |"
            for algo_name in self.results.keys():
                time_val = self.results[algo_name].get(n)
                if time_val is None:
                    row += f" {'SKIPPED':>20} |"
                elif time_val == float('inf'):
                    row += f" {'ERROR':>20} |"
                else:
                    row += f" {time_val:>20.8f} |"
            table += row + "\n"
        
        table += "=" * 100 + "\n"
        
        return table
    
    def save_results(self, filename: str = "performance_results.json"):
        """
        Save results to a JSON file.
        
        Args:
            filename: Output filename
        """
        # Convert results to serializable format
        serializable_results = {}
        for algo_name, algo_results in self.results.items():
            serializable_results[algo_name] = {
                str(n): (None if time_val is None 
                        else "inf" if time_val == float('inf') 
                        else time_val)
                for n, time_val in algo_results.items()
            }
        
        with open(filename, 'w') as f:
            json.dump(serializable_results, f, indent=2)
        
        print(f"\nResults saved to {filename}")
    
    def find_best_algorithm(self, n: int) -> Tuple[str, float]:
        """
        Find the best (fastest) algorithm for a given input.
        
        Args:
            n: The input value
            
        Returns:
            Tuple of (algorithm_name, execution_time)
        """
        if not self.results:
            return None, None
        
        best_algo = None
        best_time = float('inf')
        
        for algo_name, algo_results in self.results.items():
            if n in algo_results and algo_results[n] is not None:
                if algo_results[n] < best_time:
                    best_time = algo_results[n]
                    best_algo = algo_name
        
        return best_algo, best_time
    
    def generate_analysis_summary(self) -> str:
        """
        Generate a text summary of the analysis.
        
        Returns:
            Formatted analysis summary
        """
        summary = "\n" + "=" * 70 + "\n"
        summary += "ANALYSIS SUMMARY\n"
        summary += "=" * 70 + "\n\n"
        
        # Get all test inputs
        all_inputs = set()
        for algo_results in self.results.values():
            all_inputs.update(algo_results.keys())
        all_inputs = sorted(all_inputs)
        
        # Best algorithm for each input size
        summary += "Best Algorithm for Each Input Size:\n"
        summary += "-" * 70 + "\n"
        for n in all_inputs:
            best_algo, best_time = self.find_best_algorithm(n)
            if best_algo:
                summary += f"n={n:3d}: {best_algo:30s} ({best_time:.8f}s)\n"
        
        summary += "\n" + "-" * 70 + "\n"
        summary += "Algorithm Characteristics:\n"
        summary += "-" * 70 + "\n"
        
        characteristics = {
            'recursive_naive': "O(2^n) - Exponential | Impractical for n>35",
            'iterative': "O(n) - Linear | Memory efficient, good performance",
            'recursive_memoized': "O(n) - Linear | Fast with caching",
            'matrix_exponentiation': "O(log n) - Logarithmic | Best for very large n",
            'dynamic_programming': "O(n) - Linear | Stores all values",
            'binet_formula': "O(1) - Constant | Fast but precision issues"
        }
        
        for algo_name in self.results.keys():
            summary += f"{algo_name:25s}: {characteristics.get(algo_name, 'N/A')}\n"
        
        summary += "=" * 70 + "\n"
        
        return summary


if __name__ == "__main__":
    # Example usage
    analyzer = PerformanceAnalyzer()
    
    # Define test inputs
    test_inputs = [5, 10, 15, 20, 25, 30, 35]
    
    # Run comparison
    results = analyzer.compare_algorithms(test_inputs)
    
    # Display results
    print(analyzer.generate_comparison_table())
    print(analyzer.generate_analysis_summary())
    
    # Save results
    analyzer.save_results()
