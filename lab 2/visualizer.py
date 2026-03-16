"""
Visualization Module for Sorting Algorithms Analysis

This module creates graphs and charts to visualize performance comparisons.
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import Dict
import json


class ResultsVisualizer:
    """Creates visualizations for sorting algorithm performance data."""
    
    def __init__(self, results: Dict = None):
        """
        Initialize visualizer with results data.
        
        Args:
            results: Dictionary of data_type -> algorithm -> {size -> metrics}
        """
        self.results = results
        
        # Set style
        plt.style.use('seaborn-v0_8-darkgrid' if 'seaborn-v0_8-darkgrid' in plt.style.available 
                      else 'default')
        
        # Color scheme for algorithms
        self.colors = {
            'quicksort': '#1f77b4',
            'mergesort': '#ff7f0e',
            'heapsort': '#2ca02c',
            'insertion_sort': '#d62728'
        }
        
        self.markers = {
            'quicksort': 'o',
            'mergesort': 's',
            'heapsort': '^',
            'insertion_sort': 'D'
        }
    
    def load_results(self, filename: str = "sorting_results.json"):
        """
        Load results from JSON file.
        
        Args:
            filename: Input filename
        """
        with open(filename, 'r') as f:
            data = json.load(f)
        
        # Convert back to proper format
        self.results = {}
        for data_type, data_results in data.items():
            self.results[data_type] = {}
            for algo_name, algo_results in data_results.items():
                self.results[data_type][algo_name] = {
                    int(size): metrics
                    for size, metrics in algo_results.items()
                }
    
    def plot_time_comparison(self, data_type: str = "random", 
                            output_file: str = None):
        """
        Plot execution time comparison for all algorithms.
        
        Args:
            data_type: Type of data to plot
            output_file: Output filename (None = auto-generate)
        """
        if not self.results or data_type not in self.results:
            print(f"No results available for {data_type} data!")
            return
        
        if output_file is None:
            output_file = f"time_comparison_{data_type}.png"
        
        plt.figure(figsize=(12, 7))
        
        for algo_name, algo_results in self.results[data_type].items():
            sizes = sorted(algo_results.keys())
            times = [algo_results[s]['time'] for s in sizes]
            
            plt.plot(sizes, times, 
                    marker=self.markers.get(algo_name, 'o'),
                    label=algo_name.replace('_', ' ').title(),
                    linewidth=2, markersize=8,
                    color=self.colors.get(algo_name, '#000000'))
        
        plt.xlabel('Input Size (n)', fontsize=12, fontweight='bold')
        plt.ylabel('Execution Time (seconds)', fontsize=12, fontweight='bold')
        plt.title(f'Sorting Algorithms - Time Comparison\\n({data_type.replace("_", " ").title()} Data)', 
                 fontsize=14, fontweight='bold')
        plt.legend(loc='best', fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {output_file}")
        plt.close()
    
    def plot_comparisons(self, data_type: str = "random", 
                        output_file: str = None):
        """
        Plot number of comparisons for all algorithms.
        
        Args:
            data_type: Type of data to plot
            output_file: Output filename
        """
        if not self.results or data_type not in self.results:
            print(f"No results available for {data_type} data!")
            return
        
        if output_file is None:
            output_file = f"comparisons_{data_type}.png"
        
        plt.figure(figsize=(12, 7))
        
        for algo_name, algo_results in self.results[data_type].items():
            sizes = sorted(algo_results.keys())
            comps = [algo_results[s]['comparisons'] for s in sizes]
            
            plt.plot(sizes, comps, 
                    marker=self.markers.get(algo_name, 'o'),
                    label=algo_name.replace('_', ' ').title(),
                    linewidth=2, markersize=8,
                    color=self.colors.get(algo_name, '#000000'))
        
        plt.xlabel('Input Size (n)', fontsize=12, fontweight='bold')
        plt.ylabel('Number of Comparisons', fontsize=12, fontweight='bold')
        plt.title(f'Sorting Algorithms - Comparisons\\n({data_type.replace("_", " ").title()} Data)', 
                 fontsize=14, fontweight='bold')
        plt.legend(loc='best', fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {output_file}")
        plt.close()
    
    def plot_swaps(self, data_type: str = "random", 
                   output_file: str = None):
        """
        Plot number of swaps for all algorithms.
        
        Args:
            data_type: Type of data to plot
            output_file: Output filename
        """
        if not self.results or data_type not in self.results:
            print(f"No results available for {data_type} data!")
            return
        
        if output_file is None:
            output_file = f"swaps_{data_type}.png"
        
        plt.figure(figsize=(12, 7))
        
        for algo_name, algo_results in self.results[data_type].items():
            sizes = sorted(algo_results.keys())
            swaps = [algo_results[s]['swaps'] for s in sizes]
            
            plt.plot(sizes, swaps, 
                    marker=self.markers.get(algo_name, 'o'),
                    label=algo_name.replace('_', ' ').title(),
                    linewidth=2, markersize=8,
                    color=self.colors.get(algo_name, '#000000'))
        
        plt.xlabel('Input Size (n)', fontsize=12, fontweight='bold')
        plt.ylabel('Number of Swaps', fontsize=12, fontweight='bold')
        plt.title(f'Sorting Algorithms - Swaps\\n({data_type.replace("_", " ").title()} Data)', 
                 fontsize=14, fontweight='bold')
        plt.legend(loc='best', fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {output_file}")
        plt.close()
    
    def plot_all_metrics(self, data_type: str = "random", 
                        output_file: str = None):
        """
        Create subplot with all three metrics.
        
        Args:
            data_type: Type of data to plot
            output_file: Output filename
        """
        if not self.results or data_type not in self.results:
            print(f"No results available for {data_type} data!")
            return
        
        if output_file is None:
            output_file = f"all_metrics_{data_type}.png"
        
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))
        fig.suptitle(f'Sorting Algorithms - All Metrics ({data_type.replace("_", " ").title()} Data)', 
                    fontsize=16, fontweight='bold')
        
        metrics = ['time', 'comparisons', 'swaps']
        ylabels = ['Execution Time (seconds)', 'Number of Comparisons', 'Number of Swaps']
        
        for idx, (metric, ylabel) in enumerate(zip(metrics, ylabels)):
            ax = axes[idx]
            
            for algo_name, algo_results in self.results[data_type].items():
                sizes = sorted(algo_results.keys())
                values = [algo_results[s][metric] for s in sizes]
                
                ax.plot(sizes, values, 
                       marker=self.markers.get(algo_name, 'o'),
                       label=algo_name.replace('_', ' ').title(),
                       linewidth=2, markersize=6,
                       color=self.colors.get(algo_name, '#000000'))
            
            ax.set_xlabel('Input Size (n)', fontweight='bold')
            ax.set_ylabel(ylabel, fontweight='bold')
            ax.legend(fontsize=8)
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {output_file}")
        plt.close()
    
    def plot_data_type_comparison(self, algorithm: str, 
                                  output_file: str = None):
        """
        Compare single algorithm across different data types.
        
        Args:
            algorithm: Algorithm name to analyze
            output_file: Output filename
        """
        if not self.results:
            print("No results available!")
            return
        
        if output_file is None:
            output_file = f"{algorithm}_data_types.png"
        
        plt.figure(figsize=(12, 7))
        
        data_type_colors = {
            'random': '#1f77b4',
            'sorted': '#2ca02c',
            'reverse': '#d62728',
            'nearly_sorted': '#ff7f0e',
            'duplicates': '#9467bd'
        }
        
        for data_type in self.results.keys():
            if algorithm in self.results[data_type]:
                algo_results = self.results[data_type][algorithm]
                sizes = sorted(algo_results.keys())
                times = [algo_results[s]['time'] for s in sizes]
                
                plt.plot(sizes, times, 
                        marker='o',
                        label=data_type.replace('_', ' ').title(),
                        linewidth=2, markersize=8,
                        color=data_type_colors.get(data_type, '#000000'))
        
        plt.xlabel('Input Size (n)', fontsize=12, fontweight='bold')
        plt.ylabel('Execution Time (seconds)', fontsize=12, fontweight='bold')
        plt.title(f'{algorithm.replace("_", " ").title()} - Performance on Different Data Types', 
                 fontsize=14, fontweight='bold')
        plt.legend(loc='best', fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {output_file}")
        plt.close()
    
    def create_all_plots(self):
        """Create all standard visualization plots."""
        if not self.results:
            print("No results to plot!")
            return
        
        print("\nGenerating visualizations...")
        print("-" * 60)
        
        # Plot for each data type
        for data_type in self.results.keys():
            self.plot_time_comparison(data_type)
            self.plot_comparisons(data_type)
            self.plot_swaps(data_type)
            self.plot_all_metrics(data_type)
        
        # Plot data type comparison for each algorithm
        if self.results:
            first_data_type = list(self.results.keys())[0]
            for algo_name in self.results[first_data_type].keys():
                self.plot_data_type_comparison(algo_name)
        
        print("-" * 60)
        print("All visualizations generated successfully!")


if __name__ == "__main__":
    # Example usage
    visualizer = ResultsVisualizer()
    
    # Load results from file
    try:
        visualizer.load_results("sorting_results.json")
        visualizer.create_all_plots()
    except FileNotFoundError:
        print("No results file found. Run performance analysis first!")
