"""
Laboratory Work 2: Sorting Algorithms Implementation
Study and Empirical Analysis of Sorting Algorithms

This module contains implementations of different sorting algorithms.
"""

import random
from typing import List, Tuple


class SortingAlgorithms:
    """Collection of different sorting algorithm implementations with metrics tracking."""
    
    def __init__(self):
        self.comparisons = 0
        self.swaps = 0
    
    def reset_metrics(self):
        """Reset comparison and swap counters."""
        self.comparisons = 0
        self.swaps = 0
    
    def get_metrics(self) -> Tuple[int, int]:
        """Return current metrics (comparisons, swaps)."""
        return self.comparisons, self.swaps
    
    # ==================== QUICKSORT ====================
    
    def quicksort(self, arr: List[int]) -> List[int]:

        self.reset_metrics()
        result = arr.copy()
        self._quicksort_helper(result, 0, len(result) - 1)
        return result
    
    def _quicksort_helper(self, arr: List[int], low: int, high: int):
        """Helper function for quicksort."""
        if low < high:
            # Use insertion sort for small subarrays
            if high - low < 10:
                for i in range(low + 1, high + 1):
                    key = arr[i]
                    j = i - 1
                    while j >= low and arr[j] > key:
                        self.comparisons += 1
                        arr[j + 1] = arr[j]
                        self.swaps += 1
                        j -= 1
                    if j >= low:
                        self.comparisons += 1
                    arr[j + 1] = key
                    self.swaps += 1
            else:
                pi = self._partition(arr, low, high)
                self._quicksort_helper(arr, low, pi - 1)
                self._quicksort_helper(arr, pi + 1, high)
    
    def _partition(self, arr: List[int], low: int, high: int) -> int:
        """Partition function using median-of-three pivot strategy."""
        # Median-of-three pivot selection to avoid worst case on sorted data
        mid = (low + high) // 2
        
        # Sort low, mid, high elements
        if arr[low] > arr[mid]:
            arr[low], arr[mid] = arr[mid], arr[low]
            self.swaps += 1
        if arr[low] > arr[high]:
            arr[low], arr[high] = arr[high], arr[low]
            self.swaps += 1
        if arr[mid] > arr[high]:
            arr[mid], arr[high] = arr[high], arr[mid]
            self.swaps += 1
        
        # Place median at high-1 position
        arr[mid], arr[high - 1] = arr[high - 1], arr[mid]
        self.swaps += 1
        pivot = arr[high - 1]
        
        i = low
        j = high - 1
        
        while True:
            i += 1
            while i < high and arr[i] < pivot:
                self.comparisons += 1
                i += 1
            if i < high:
                self.comparisons += 1
            
            j -= 1
            while j > low and arr[j] > pivot:
                self.comparisons += 1
                j -= 1
            if j > low:
                self.comparisons += 1
            
            if i >= j:
                break
            
            arr[i], arr[j] = arr[j], arr[i]
            self.swaps += 1
        
        arr[i], arr[high - 1] = arr[high - 1], arr[i]
        self.swaps += 1
        return i
    
    # ==================== MERGESORT ====================
    
    def mergesort(self, arr: List[int]) -> List[int]:
  
        self.reset_metrics()
        result = arr.copy()
        self._mergesort_helper(result, 0, len(result) - 1)
        return result
    
    def _mergesort_helper(self, arr: List[int], left: int, right: int):
        """Helper function for mergesort."""
        if left < right:
            mid = (left + right) // 2
            self._mergesort_helper(arr, left, mid)
            self._mergesort_helper(arr, mid + 1, right)
            self._merge(arr, left, mid, right)
    
    def _merge(self, arr: List[int], left: int, mid: int, right: int):
        """Merge two sorted subarrays."""
        left_part = arr[left:mid + 1]
        right_part = arr[mid + 1:right + 1]
        
        i = j = 0
        k = left
        
        while i < len(left_part) and j < len(right_part):
            self.comparisons += 1
            if left_part[i] <= right_part[j]:
                arr[k] = left_part[i]
                i += 1
            else:
                arr[k] = right_part[j]
                j += 1
            self.swaps += 1
            k += 1
        
        while i < len(left_part):
            arr[k] = left_part[i]
            self.swaps += 1
            i += 1
            k += 1
        
        while j < len(right_part):
            arr[k] = right_part[j]
            self.swaps += 1
            j += 1
            k += 1
    
    # ==================== HEAPSORT ====================
    
    def heapsort(self, arr: List[int]) -> List[int]:

        self.reset_metrics()
        result = arr.copy()
        n = len(result)
        # Build max heap
        for i in range(n // 2 - 1, -1, -1):
            self._heapify(result, n, i)
        # Extract elements from heap one by one
        for i in range(n - 1, 0, -1):
            result[0], result[i] = result[i], result[0]
            self.swaps += 1
            self._heapify(result, i, 0)
        
        return result
    
    def _heapify(self, arr: List[int], n: int, i: int):
        """Heapify subtree rooted at index i."""
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        
        if left < n:
            self.comparisons += 1
            if arr[left] > arr[largest]:
                largest = left
        
        if right < n:
            self.comparisons += 1
            if arr[right] > arr[largest]:
                largest = right
        
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            self.swaps += 1
            self._heapify(arr, n, largest)
    
    # ==================== INSERTION SORT ====================
    
    def insertion_sort(self, arr: List[int]) -> List[int]:
  
        self.reset_metrics()
        result = arr.copy()
        
        for i in range(1, len(result)):
            key = result[i]
            j = i - 1
            
            while j >= 0:
                self.comparisons += 1
                if result[j] > key:
                    result[j + 1] = result[j]
                    self.swaps += 1
                    j -= 1
                else:
                    break
            
            result[j + 1] = key
        
        return result


# Dictionary mapping algorithm names to their methods
def get_sorting_algorithms():
    """Return dictionary of sorting algorithms."""
    sorter = SortingAlgorithms()
    return {
        'quicksort': sorter.quicksort,
        'mergesort': sorter.mergesort,
        'heapsort': sorter.heapsort,
        'insertion_sort': sorter.insertion_sort
    }


# Data generation functions
class DataGenerator:
    """Generate different types of test data for sorting algorithms."""
    
    @staticmethod
    def random_data(size: int, min_val: int = 0, max_val: int = 10000) -> List[int]:
        """Generate random unsorted data."""
        return [random.randint(min_val, max_val) for _ in range(size)]
    
    @staticmethod
    def sorted_data(size: int) -> List[int]:
        """Generate already sorted data (best case for some algorithms)."""
        return list(range(size))
    
    @staticmethod
    def reverse_sorted_data(size: int) -> List[int]:
        """Generate reverse sorted data (worst case for some algorithms)."""
        return list(range(size, 0, -1))
    
    @staticmethod
    def nearly_sorted_data(size: int, swaps: int = None) -> List[int]:
        """Generate nearly sorted data with a few random swaps."""
        if swaps is None:
            swaps = size // 10  # 10% disorder
        
        arr = list(range(size))
        for _ in range(swaps):
            i, j = random.randint(0, size - 1), random.randint(0, size - 1)
            arr[i], arr[j] = arr[j], arr[i]
        return arr
    
    @staticmethod
    def duplicate_data(size: int, unique_values: int = None) -> List[int]:
        """Generate data with many duplicates."""
        if unique_values is None:
            unique_values = size // 10
        
        return [random.randint(0, unique_values) for _ in range(size)]
    
    @staticmethod
    def all_same(size: int, value: int = 5) -> List[int]:
        """Generate data where all elements are the same."""
        return [value] * size


if __name__ == "__main__":
    # Simple test
    print("Testing Sorting Algorithms")
    print("=" * 60)
    
    test_data = [64, 34, 25, 12, 22, 11, 90]
    print(f"Original array: {test_data}\n")
    
    sorter = SortingAlgorithms()
    algorithms = get_sorting_algorithms()
    
    for name, func in algorithms.items():
        sorted_arr = func(test_data)
        comps, swps = sorter.get_metrics()
        print(f"{name:20s}: {sorted_arr}")
        print(f"{'':20s}  Comparisons: {comps}, Swaps: {swps}\n")
