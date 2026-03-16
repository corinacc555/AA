"""
Interactive Visualization Module for Sorting Algorithms Analysis

This module displays graphs in interactive windows instead of saving to files.
"""

import matplotlib.pyplot as plt
import json
from typing import Dict


class InteractiveVisualizer:
    """Creates interactive visualizations that display in windows."""
    
    def __init__(self, results_file: str = "sorting_results.json"):
        """Load results from JSON file."""
        with open(results_file, 'r') as f:
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
    
    def plot_time_comparison(self, data_type: str = "random"):
        """Display time comparison plot in window."""
        if data_type not in self.results:
            print(f"No results for {data_type} data!")
            return
        
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
        plt.title(f'Sorting Algorithms - Time Comparison\n({data_type.replace("_", " ").title()} Data)', 
                 fontsize=14, fontweight='bold')
        plt.legend(loc='best', fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    def plot_comparisons(self, data_type: str = "random"):
        """Display comparisons plot in window."""
        if data_type not in self.results:
            print(f"No results for {data_type} data!")
            return
        
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
        plt.title(f'Sorting Algorithms - Comparisons\n({data_type.replace("_", " ").title()} Data)', 
                 fontsize=14, fontweight='bold')
        plt.legend(loc='best', fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    def plot_swaps(self, data_type: str = "random"):
        """Display swaps plot in window."""
        if data_type not in self.results:
            print(f"No results for {data_type} data!")
            return
        
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
        plt.title(f'Sorting Algorithms - Swaps\n({data_type.replace("_", " ").title()} Data)', 
                 fontsize=14, fontweight='bold')
        plt.legend(loc='best', fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    def plot_all_metrics(self, data_type: str = "random"):
        """Display all three metrics in subplots."""
        if data_type not in self.results:
            print(f"No results for {data_type} data!")
            return
        
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
        plt.show()
    
    def plot_algorithm_comparison(self, algorithm: str):
        """Compare one algorithm across all data types."""
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
        plt.show()
    
    def show_menu(self):
        """Interactive menu for viewing different plots."""
        print("\n" + "="*60)
        print("INTERACTIVE VISUALIZATION MENU")
        print("="*60)
        
        while True:
            print("\nAvailable options:")
            print("1. Time comparison by data type")
            print("2. Comparisons by data type")
            print("3. Swaps by data type")
            print("4. All metrics (time, comparisons, swaps)")
            print("5. Compare one algorithm across all data types")
            print("6. Exit")
            
            choice = input("\nSelect option (1-6): ").strip()
            
            if choice == '6':
                print("Exiting...")
                break
            
            if choice in ['1', '2', '3', '4']:
                print("\nData types:")
                data_types = list(self.results.keys())
                for i, dt in enumerate(data_types, 1):
                    print(f"{i}. {dt.replace('_', ' ').title()}")
                
                dt_choice = input(f"\nSelect data type (1-{len(data_types)}): ").strip()
                try:
                    dt_idx = int(dt_choice) - 1
                    if 0 <= dt_idx < len(data_types):
                        data_type = data_types[dt_idx]
                        
                        if choice == '1':
                            self.plot_time_comparison(data_type)
                        elif choice == '2':
                            self.plot_comparisons(data_type)
                        elif choice == '3':
                            self.plot_swaps(data_type)
                        elif choice == '4':
                            self.plot_all_metrics(data_type)
                    else:
                        print("Invalid selection!")
                except ValueError:
                    print("Invalid input!")
            
            elif choice == '5':
                print("\nAlgorithms:")
                print("1. QuickSort")
                print("2. MergeSort")
                print("3. HeapSort")
                print("4. InsertionSort")
                
                algo_choice = input("\nSelect algorithm (1-4): ").strip()
                algo_map = {
                    '1': 'quicksort',
                    '2': 'mergesort',
                    '3': 'heapsort',
                    '4': 'insertion_sort'
                }
                
                if algo_choice in algo_map:
                    self.plot_algorithm_comparison(algo_map[algo_choice])
                else:
                    print("Invalid selection!")
            
            else:
                print("Invalid option!")


if __name__ == "__main__":
    try:
        visualizer = InteractiveVisualizer("sorting_results.json")
        visualizer.show_menu()
    except FileNotFoundError:
        print("Error: sorting_results.json not found!")
        print("Run the analysis first: python main.py")
