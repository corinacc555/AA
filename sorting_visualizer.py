"""
Real-Time Sorting Algorithm Visualizer

This module creates animated visualizations showing how sorting algorithms work step-by-step.
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import time
from typing import List, Tuple, Generator


class SortingVisualizer:
    """Visualizes sorting algorithms in real-time with animations."""
    
    def __init__(self, array_size: int = 50):
        """
        Initialize the visualizer.
        
        Args:
            array_size: Number of elements to sort
        """
        self.array_size = array_size
        self.array = None
        self.fig, self.ax = plt.subplots(figsize=(12, 7))
        self.bar_rects = None
        self.iteration = [0]
        self.text = self.ax.text(0.02, 0.95, "", transform=self.ax.transAxes)
        
    def generate_array(self, data_type: str = "random"):
        """Generate array based on type."""
        if data_type == "random":
            self.array = [random.randint(1, 100) for _ in range(self.array_size)]
        elif data_type == "sorted":
            self.array = list(range(1, self.array_size + 1))
        elif data_type == "reverse":
            self.array = list(range(self.array_size, 0, -1))
        elif data_type == "nearly_sorted":
            self.array = list(range(1, self.array_size + 1))
            # Swap 10% of elements
            for _ in range(self.array_size // 10):
                i, j = random.randint(0, self.array_size - 1), random.randint(0, self.array_size - 1)
                self.array[i], self.array[j] = self.array[j], self.array[i]
        else:
            self.array = [random.randint(1, 100) for _ in range(self.array_size)]
        
        return self.array.copy()
    
    def update_bars(self, arr, colors=None):
        """Update the visualization bars."""
        if colors is None:
            colors = ['blue'] * len(arr)
        
        for rect, val, color in zip(self.bar_rects, arr, colors):
            rect.set_height(val)
            rect.set_color(color)
        
        self.iteration[0] += 1
        self.text.set_text(f"Operations: {self.iteration[0]}")
    
    # ==================== BUBBLE SORT ANIMATION ====================
    
    def bubble_sort_generator(self, arr: List[int]) -> Generator:
        """Generator for bubble sort animation."""
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                # Highlight comparison
                colors = ['blue'] * n
                colors[j] = 'red'
                colors[j + 1] = 'red'
                yield arr.copy(), colors
                
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    # Highlight swap
                    colors[j] = 'green'
                    colors[j + 1] = 'green'
                    yield arr.copy(), colors
        
        # Final state - all sorted
        colors = ['green'] * n
        yield arr.copy(), colors
    
    # ==================== INSERTION SORT ANIMATION ====================
    
    def insertion_sort_generator(self, arr: List[int]) -> Generator:
        """Generator for insertion sort animation."""
        n = len(arr)
        
        for i in range(1, n):
            key = arr[i]
            j = i - 1
            
            # Highlight current element
            colors = ['blue'] * n
            colors[i] = 'red'
            for k in range(i):
                colors[k] = 'green'
            yield arr.copy(), colors
            
            while j >= 0 and arr[j] > key:
                arr[j + 1] = arr[j]
                
                # Show shifting
                colors = ['blue'] * n
                colors[j] = 'yellow'
                colors[j + 1] = 'red'
                for k in range(j):
                    colors[k] = 'green'
                yield arr.copy(), colors
                
                j -= 1
            
            arr[j + 1] = key
            
            # Show insertion
            colors = ['blue'] * n
            for k in range(i + 1):
                colors[k] = 'green'
            yield arr.copy(), colors
        
        # Final state
        colors = ['green'] * n
        yield arr.copy(), colors
    
    # ==================== SELECTION SORT ANIMATION ====================
    
    def selection_sort_generator(self, arr: List[int]) -> Generator:
        """Generator for selection sort animation."""
        n = len(arr)
        
        for i in range(n):
            min_idx = i
            colors = ['blue'] * n
            
            # Mark sorted portion
            for k in range(i):
                colors[k] = 'green'
            
            for j in range(i + 1, n):
                # Highlight comparison
                colors = ['blue'] * n
                for k in range(i):
                    colors[k] = 'green'
                colors[i] = 'yellow'
                colors[min_idx] = 'red'
                colors[j] = 'red'
                yield arr.copy(), colors
                
                if arr[j] < arr[min_idx]:
                    min_idx = j
            
            # Swap
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            
            # Show swap
            colors = ['blue'] * n
            for k in range(i + 1):
                colors[k] = 'green'
            yield arr.copy(), colors
        
        # Final state
        colors = ['green'] * n
        yield arr.copy(), colors
    
    # ==================== QUICK SORT ANIMATION ====================
    
    def quick_sort_generator(self, arr: List[int], low: int = 0, high: int = None) -> Generator:
        """Generator for quick sort animation."""
        if high is None:
            high = len(arr) - 1
        
        def partition(arr, low, high):
            pivot = arr[high]
            i = low - 1
            
            for j in range(low, high):
                # Highlight comparison with pivot
                colors = ['blue'] * len(arr)
                colors[high] = 'yellow'  # pivot
                colors[j] = 'red'
                if i >= 0:
                    colors[i] = 'green'
                yield arr.copy(), colors
                
                if arr[j] <= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
                    
                    # Show swap
                    colors = ['blue'] * len(arr)
                    colors[high] = 'yellow'
                    colors[i] = 'green'
                    colors[j] = 'green'
                    yield arr.copy(), colors
            
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            
            # Show pivot placement
            colors = ['blue'] * len(arr)
            colors[i + 1] = 'green'
            yield arr.copy(), colors
            
            return i + 1
        
        def quick_sort_helper(arr, low, high):
            if low < high:
                # Partition
                pi_gen = partition(arr, low, high)
                for state in pi_gen:
                    yield state
                
                pi = low
                temp_pivot = arr[high]
                for k in range(low, high):
                    if arr[k] <= temp_pivot:
                        pi += 1
                
                # Actually do the partition for recursion
                pivot = arr[high]
                i = low - 1
                for j in range(low, high):
                    if arr[j] <= pivot:
                        i += 1
                        arr[i], arr[j] = arr[j], arr[i]
                arr[i + 1], arr[high] = arr[high], arr[i + 1]
                pi = i + 1
                
                # Recurse left
                yield from quick_sort_helper(arr, low, pi - 1)
                # Recurse right
                yield from quick_sort_helper(arr, pi + 1, high)
        
        yield from quick_sort_helper(arr, low, high)
        
        # Final state
        colors = ['green'] * len(arr)
        yield arr.copy(), colors
    
    # ==================== MERGE SORT ANIMATION ====================
    
    def merge_sort_generator(self, arr: List[int]) -> Generator:
        """Generator for merge sort animation."""
        
        def merge_sort_helper(arr, left, right):
            if left < right:
                mid = (left + right) // 2
                
                # Highlight section being sorted
                colors = ['blue'] * len(arr)
                for i in range(left, right + 1):
                    colors[i] = 'yellow'
                yield arr.copy(), colors
                
                # Sort left half
                yield from merge_sort_helper(arr, left, mid)
                # Sort right half
                yield from merge_sort_helper(arr, mid + 1, right)
                # Merge
                yield from merge(arr, left, mid, right)
        
        def merge(arr, left, mid, right):
            left_part = arr[left:mid + 1]
            right_part = arr[mid + 1:right + 1]
            
            i = j = 0
            k = left
            
            while i < len(left_part) and j < len(right_part):
                # Highlight comparison
                colors = ['blue'] * len(arr)
                colors[k] = 'red'
                yield arr.copy(), colors
                
                if left_part[i] <= right_part[j]:
                    arr[k] = left_part[i]
                    i += 1
                else:
                    arr[k] = right_part[j]
                    j += 1
                
                # Show merge
                colors = ['blue'] * len(arr)
                colors[k] = 'green'
                yield arr.copy(), colors
                
                k += 1
            
            while i < len(left_part):
                arr[k] = left_part[i]
                colors = ['blue'] * len(arr)
                colors[k] = 'green'
                yield arr.copy(), colors
                i += 1
                k += 1
            
            while j < len(right_part):
                arr[k] = right_part[j]
                colors = ['blue'] * len(arr)
                colors[k] = 'green'
                yield arr.copy(), colors
                j += 1
                k += 1
        
        yield from merge_sort_helper(arr, 0, len(arr) - 1)
        
        # Final state
        colors = ['green'] * len(arr)
        yield arr.copy(), colors
    
    # ==================== VISUALIZATION ====================
    
    def visualize(self, algorithm: str, data_type: str = "random", speed: int = 50):
        """
        Visualize a sorting algorithm.
        
        Args:
            algorithm: Algorithm name ('bubble', 'insertion', 'selection', 'quick', 'merge')
            data_type: Type of data ('random', 'sorted', 'reverse', 'nearly_sorted')
            speed: Animation speed in milliseconds (lower = faster)
        """
        # Generate array
        arr = self.generate_array(data_type)
        self.iteration = [0]
        
        # Get generator
        if algorithm.lower() == 'bubble':
            generator = self.bubble_sort_generator(arr)
            title = "Bubble Sort"
        elif algorithm.lower() == 'insertion':
            generator = self.insertion_sort_generator(arr)
            title = "Insertion Sort"
        elif algorithm.lower() == 'selection':
            generator = self.selection_sort_generator(arr)
            title = "Selection Sort"
        elif algorithm.lower() == 'quick':
            generator = self.quick_sort_generator(arr)
            title = "Quick Sort"
        elif algorithm.lower() == 'merge':
            generator = self.merge_sort_generator(arr)
            title = "Merge Sort"
        else:
            print(f"Unknown algorithm: {algorithm}")
            return
        
        # Setup plot
        self.ax.clear()
        self.ax.set_title(f"{title} - {data_type.title()} Data (n={self.array_size})", 
                         fontsize=14, fontweight='bold')
        self.ax.set_xlabel("Index", fontsize=11)
        self.ax.set_ylabel("Value", fontsize=11)
        self.text = self.ax.text(0.02, 0.95, "", transform=self.ax.transAxes, fontsize=12)
        
        # Create bars
        self.bar_rects = self.ax.bar(range(len(arr)), arr, align="edge", color='blue')
        self.ax.set_xlim(0, len(arr))
        self.ax.set_ylim(0, int(1.1 * max(arr)))
        
        # Animation function
        def animate(frame):
            arr_state, colors = frame
            self.update_bars(arr_state, colors)
        
        # Create animation
        anim = animation.FuncAnimation(
            self.fig, animate, frames=generator,
            interval=speed, repeat=False, cache_frame_data=False
        )
        
        plt.show()


def main():
    """Interactive menu for sorting visualization."""
    print("=" * 60)
    print("REAL-TIME SORTING ALGORITHM VISUALIZER")
    print("=" * 60)
    
    while True:
        print("\nSelect sorting algorithm:")
        print("1. Bubble Sort")
        print("2. Insertion Sort")
        print("3. Selection Sort")
        print("4. Quick Sort")
        print("5. Merge Sort")
        print("6. Exit")
        
        choice = input("\nSelect option (1-6): ").strip()
        
        if choice == '6':
            print("Exiting...")
            break
        
        algo_map = {
            '1': 'bubble',
            '2': 'insertion',
            '3': 'selection',
            '4': 'quick',
            '5': 'merge'
        }
        
        if choice not in algo_map:
            print("Invalid choice!")
            continue
        
        print("\nSelect data type:")
        print("1. Random")
        print("2. Sorted")
        print("3. Reverse sorted")
        print("4. Nearly sorted")
        
        data_choice = input("\nSelect data type (1-4): ").strip()
        data_map = {
            '1': 'random',
            '2': 'sorted',
            '3': 'reverse',
            '4': 'nearly_sorted'
        }
        
        if data_choice not in data_map:
            print("Invalid choice!")
            continue
        
        size = input("\nArray size (default=50, max=100): ").strip()
        try:
            size = int(size) if size else 50
            size = min(size, 100)
        except ValueError:
            size = 50
        
        speed = input("\nAnimation speed in ms (default=50, lower=faster): ").strip()
        try:
            speed = int(speed) if speed else 50
        except ValueError:
            speed = 50
        
        print(f"\nStarting visualization...")
        print("Close the window to return to menu.\n")
        
        visualizer = SortingVisualizer(array_size=size)
        visualizer.visualize(algo_map[choice], data_map[data_choice], speed)


if __name__ == "__main__":
    main()
