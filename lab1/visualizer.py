"""
Visualization Module for Fibonacci Algorithms Analysis

This module creates graphs and charts to visualize performance comparisons.
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import Dict
import json


class ResultsVisualizer:
    """Creates visualizations for algorithm performance data."""
    
    def __init__(self, results: Dict[str, Dict[int, float]] = None):
        """
        Initialize visualizer with results data.
        
        Args:
            results: Dictionary of algorithm_name -> {input -> time}
        """
        self.results = results
        
        # Set style
        plt.style.use('seaborn-v0_8-darkgrid' if 'seaborn-v0_8-darkgrid' in plt.style.available 
                      else 'default')
    
    def load_results(self, filename: str = "performance_results.json"):
        """
        Load results from JSON file.
        
        Args:
            filename: Input filename
        """
        with open(filename, 'r') as f:
            data = json.load(f)
        
        # Convert back to proper format
        self.results = {}
        for algo_name, algo_results in data.items():
            self.results[algo_name] = {
                int(n): (None if time_val is None 
                        else float('inf') if time_val == "inf" 
                        else time_val)
                for n, time_val in algo_results.items()
            }
    
    def plot_all_algorithms(self, output_file: str = "all_algorithms_comparison.png"):
        """
        Plot all algorithms on the same graph (linear scale).
        
        Args:
            output_file: Output filename for the plot
        """
        if not self.results:
            print("No results to plot!")
            return
        
        plt.figure(figsize=(12, 7))
        
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
        markers = ['o', 's', '^', 'D', 'v', 'p']
        
        for idx, (algo_name, algo_results) in enumerate(self.results.items()):
            # Filter out None and inf values
            valid_data = [(n, time) for n, time in algo_results.items() 
                         if time is not None and time != float('inf')]
            
            if valid_data:
                ns, times = zip(*valid_data)
                plt.plot(ns, times, marker=markers[idx % len(markers)], 
                        label=algo_name, linewidth=2, markersize=8,
                        color=colors[idx % len(colors)])
        
        plt.xlabel('Input Size (n)', fontsize=12, fontweight='bold')
        plt.ylabel('Execution Time (seconds)', fontsize=12, fontweight='bold')
        plt.title('Fibonacci Algorithms - Performance Comparison\n(All Algorithms - Linear Scale)', 
                 fontsize=14, fontweight='bold')
        plt.legend(loc='best', fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {output_file}")
        plt.close()
    
    def plot_logarithmic_scale(self, output_file: str = "algorithms_log_scale.png"):
        """
        Plot algorithms on logarithmic scale for better comparison.
        
        Args:
            output_file: Output filename for the plot
        """
        if not self.results:
            print("No results to plot!")
            return
        
        plt.figure(figsize=(12, 7))
        
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
        markers = ['o', 's', '^', 'D', 'v', 'p']
        
        for idx, (algo_name, algo_results) in enumerate(self.results.items()):
            valid_data = [(n, time) for n, time in algo_results.items() 
                         if time is not None and time != float('inf') and time > 0]
            
            if valid_data:
                ns, times = zip(*valid_data)
                plt.semilogy(ns, times, marker=markers[idx % len(markers)], 
                           label=algo_name, linewidth=2, markersize=8,
                           color=colors[idx % len(colors)])
        
        plt.xlabel('Input Size (n)', fontsize=12, fontweight='bold')
        plt.ylabel('Execution Time (seconds, log scale)', fontsize=12, fontweight='bold')
        plt.title('Fibonacci Algorithms - Performance Comparison\n(Logarithmic Scale)', 
                 fontsize=14, fontweight='bold')
        plt.legend(loc='best', fontsize=10)
        plt.grid(True, alpha=0.3, which='both')
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {output_file}")
        plt.close()
    
    def plot_efficient_algorithms(self, output_file: str = "efficient_algorithms.png"):
        """
        Plot only efficient algorithms (excluding naive recursive).
        
        Args:
            output_file: Output filename for the plot
        """
        if not self.results:
            print("No results to plot!")
            return
        
        plt.figure(figsize=(12, 7))
        
        colors = ['#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
        markers = ['s', '^', 'D', 'v', 'p']
        
        # Exclude naive recursive
        efficient_algos = {k: v for k, v in self.results.items() 
                          if k != 'recursive_naive'}
        
        for idx, (algo_name, algo_results) in enumerate(efficient_algos.items()):
            valid_data = [(n, time) for n, time in algo_results.items() 
                         if time is not None and time != float('inf')]
            
            if valid_data:
                ns, times = zip(*valid_data)
                plt.plot(ns, times, marker=markers[idx % len(markers)], 
                        label=algo_name, linewidth=2, markersize=8,
                        color=colors[idx % len(colors)])
        
        plt.xlabel('Input Size (n)', fontsize=12, fontweight='bold')
        plt.ylabel('Execution Time (seconds)', fontsize=12, fontweight='bold')
        plt.title('Fibonacci Algorithms - Efficient Algorithms Comparison\n(Excluding Naive Recursive)', 
                 fontsize=14, fontweight='bold')
        plt.legend(loc='best', fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {output_file}")
        plt.close()
    
    def plot_complexity_comparison(self, output_file: str = "complexity_comparison.png"):
        """
        Create subplots showing different complexity classes.
        
        Args:
            output_file: Output filename for the plot
        """
        if not self.results:
            print("No results to plot!")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Fibonacci Algorithms - Complexity Analysis', 
                    fontsize=16, fontweight='bold')
        
        # Exponential (Naive Recursive)
        if 'recursive_naive' in self.results:
            ax = axes[0, 0]
            data = [(n, time) for n, time in self.results['recursive_naive'].items() 
                   if time is not None and time != float('inf')]
            if data:
                ns, times = zip(*data)
                ax.plot(ns, times, 'ro-', linewidth=2, markersize=8)
                ax.set_xlabel('Input Size (n)', fontweight='bold')
                ax.set_ylabel('Time (seconds)', fontweight='bold')
                ax.set_title('Exponential: O(2^n)\nNaive Recursive', fontweight='bold')
                ax.grid(True, alpha=0.3)
        
        # Linear (Iterative, Memoized, DP)
        ax = axes[0, 1]
        linear_algos = ['iterative', 'recursive_memoized', 'dynamic_programming']
        colors = ['#ff7f0e', '#2ca02c', '#d62728']
        for idx, algo in enumerate(linear_algos):
            if algo in self.results:
                data = [(n, time) for n, time in self.results[algo].items() 
                       if time is not None and time != float('inf')]
                if data:
                    ns, times = zip(*data)
                    ax.plot(ns, times, marker='o', label=algo, 
                          linewidth=2, markersize=6, color=colors[idx])
        ax.set_xlabel('Input Size (n)', fontweight='bold')
        ax.set_ylabel('Time (seconds)', fontweight='bold')
        ax.set_title('Linear: O(n)', fontweight='bold')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)
        
        # Logarithmic (Matrix)
        ax = axes[1, 0]
        if 'matrix_exponentiation' in self.results:
            data = [(n, time) for n, time in self.results['matrix_exponentiation'].items() 
                   if time is not None and time != float('inf')]
            if data:
                ns, times = zip(*data)
                ax.plot(ns, times, 'g^-', linewidth=2, markersize=8)
                ax.set_xlabel('Input Size (n)', fontweight='bold')
                ax.set_ylabel('Time (seconds)', fontweight='bold')
                ax.set_title('Logarithmic: O(log n)\nMatrix Exponentiation', fontweight='bold')
                ax.grid(True, alpha=0.3)
        
        # Constant (Binet's Formula)
        ax = axes[1, 1]
        if 'binet_formula' in self.results:
            data = [(n, time) for n, time in self.results['binet_formula'].items() 
                   if time is not None and time != float('inf')]
            if data:
                ns, times = zip(*data)
                ax.plot(ns, times, 'mD-', linewidth=2, markersize=8)
                ax.set_xlabel('Input Size (n)', fontweight='bold')
                ax.set_ylabel('Time (seconds)', fontweight='bold')
                ax.set_title('Constant: O(1)\nBinet\'s Formula', fontweight='bold')
                ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {output_file}")
        plt.close()
    
    def create_all_plots(self):
        """Create all visualization plots."""
        print("\nGenerating visualizations...")
        print("-" * 50)
        
        self.plot_all_algorithms()
        self.plot_logarithmic_scale()
        self.plot_efficient_algorithms()
        self.plot_complexity_comparison()
        
        print("-" * 50)
        print("All visualizations generated successfully!")


if __name__ == "__main__":
    # Example usage
    visualizer = ResultsVisualizer()
    
    # Load results from file
    try:
        visualizer.load_results("performance_results.json")
        visualizer.create_all_plots()
    except FileNotFoundError:
        print("No results file found. Run performance analysis first!")
