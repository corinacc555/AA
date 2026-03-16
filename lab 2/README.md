# Laboratory Work 2AA: Study and Empirical Analysis of Sorting Algorithms

## Objectives

This laboratory work focuses on the study and empirical analysis of fundamental sorting algorithms. The main goals are:

1. **Implementation**: Implement four sorting algorithms in Python:
   - QuickSort
   - MergeSort
   - HeapSort
   - InsertionSort

2. **Empirical Analysis**: Conduct performance measurements including:
   - Execution time
   - Number of comparisons
   - Number of swaps/moves

3. **Comparative Study**: Compare algorithm behavior on different input types:
   - Random arrays
   - Already sorted arrays
   - Reverse sorted arrays
   - Nearly sorted arrays
   - Arrays with many duplicates

4. **Visualization**: Create graphs showing performance characteristics and trends

## Project Structure

```
lab 2AA/
│
├── sorting_algorithms.py      # Core algorithm implementations
├── performance_analyzer.py    # Performance measurement tools
├── visualizer.py              # Visualization module (matplotlib)
├── main.py                    # Main entry point
└── README.md                  # This file
```

## Algorithms Overview

### 1. QuickSort

**Description**: Divide-and-conquer algorithm that selects a pivot element and partitions the array around it.

**Time Complexity**:
- Best case: O(n log n)
- Average case: O(n log n)
- Worst case: O(n²) - occurs with already sorted data and poor pivot selection

**Space Complexity**: O(log n) due to recursion stack

**Characteristics**:
- Not stable (relative order of equal elements may change)
- In-place sorting
- Cache-friendly due to sequential access patterns
- Performance highly dependent on pivot selection strategy

### 2. MergeSort

**Description**: Divide-and-conquer algorithm that recursively divides the array, sorts subarrays, and merges them.

**Time Complexity**:
- Best case: O(n log n)
- Average case: O(n log n)
- Worst case: O(n log n)

**Space Complexity**: O(n) for temporary merge arrays

**Characteristics**:
- Stable (preserves relative order of equal elements)
- Not in-place (requires additional memory)
- Consistent performance regardless of input
- Ideal for linked lists and external sorting

### 3. HeapSort

**Description**: Comparison-based algorithm using a binary heap data structure.

**Time Complexity**:
- Best case: O(n log n)
- Average case: O(n log n)
- Worst case: O(n log n)

**Space Complexity**: O(1) - sorts in place

**Characteristics**:
- Not stable
- In-place sorting
- No worst-case quadratic behavior
- Less cache-friendly due to scattered memory access
- Good for systems with memory constraints

### 4. InsertionSort

**Description**: Simple algorithm that builds the sorted array one element at a time.

**Time Complexity**:
- Best case: O(n) - when array is already sorted
- Average case: O(n²)
- Worst case: O(n²) - when array is reverse sorted

**Space Complexity**: O(1)

**Characteristics**:
- Stable
- In-place sorting
- Efficient for small arrays (n < 50)
- Excellent for nearly sorted data
- Online algorithm (can sort as data arrives)

## Input Data Properties

The analysis uses five different data types to test algorithm behavior:

1. **Random Arrays**: Uniformly distributed random integers
   - Tests average-case performance
   - Most realistic for general-purpose sorting

2. **Sorted Arrays**: Already in ascending order
   - Best case for some algorithms (InsertionSort)
   - Worst case for naive QuickSort implementations

3. **Reverse Sorted Arrays**: Descending order
   - Worst case for InsertionSort
   - Challenging for many algorithms

4. **Nearly Sorted Arrays**: 90% sorted with 10% random swaps
   - Common in real-world scenarios
   - Tests adaptivity to existing order

5. **Arrays with Many Duplicates**: 80% duplicate values
   - Tests handling of equal elements
   - Important for stability verification

## Measurement Metrics

### 1. Execution Time
- Measured in seconds using high-precision timer
- Averaged over 5 iterations to reduce variance
- Most practical metric for real applications

### 2. Number of Comparisons
- Counts all element-to-element comparisons
- Independent of hardware and implementation details
- Theoretical complexity indicator

### 3. Number of Swaps/Moves
- Counts data movement operations
- Important for large objects or database records
- Indicates memory write operations

## Usage

### Full Analysis (Recommended)

Run complete analysis with all algorithms, data types, and visualizations:

```bash
python main.py
```

This will:
- Test all algorithms on all data types
- Measure time, comparisons, and swaps
- Generate JSON results file
- Create PNG visualization plots

### Quick Verification

Test that all algorithms work correctly:

```bash
python main.py --quick
```

### Interactive Mode

Test specific algorithm/data type combinations:

```bash
python main.py --interactive
```

## Results and Analysis

After running the full analysis, the following files are generated:

- `sorting_results.json`: Raw performance data
- `time_comparison_*.png`: Execution time plots for each data type
- `comparisons_*.png`: Comparison count plots
- `swaps_*.png`: Swap count plots
- `all_metrics_*.png`: Combined metric visualizations
- `*_data_types.png`: Per-algorithm comparison across data types

## Conclusions

Through this empirical analysis, I gained valuable insights into how different sorting algorithms behave in practice. The theoretical complexity classes like O(n log n) and O(n²) became much more tangible when I could see the actual execution times plotted on graphs.

**QuickSort** proved to be the fastest algorithm for random data, which makes sense given its excellent cache locality and few data movements. However, I was surprised by how dramatically its performance degraded on already sorted data when using the simple first-element pivot strategy. This really drove home the importance of implementation details—theory tells you the worst case is O(n²), but seeing it happen with sorted input was eye-opening. In practice, QuickSort with a good pivot selection (like median-of-three) remains an excellent general-purpose choice.

**MergeSort** showed the most consistent behavior across all data types, which aligns perfectly with its guaranteed O(n log n) complexity. The graphs showed almost identical curves whether the input was random, sorted, or reversed. This predictability comes at a cost though—the extra memory for merging and the larger number of data moves make it slower than QuickSort on average-case data. I found it particularly interesting that MergeSort's stability property makes it invaluable when sorting complex objects where you need to preserve the order of equivalent elements.

**HeapSort** surprised me with its performance characteristics. While it guarantees O(n log n) like MergeSort, it was consistently slower in practice. After examining the comparison counts, I understood why—the heap structure causes scattered memory accesses that don't play well with modern CPU caches. Despite this, HeapSort's in-place sorting with guaranteed worst-case performance makes it perfect for embedded systems or situations where you absolutely cannot afford extra memory or unpredictable timing.

**InsertionSort** gave me the most dramatic results. On nearly sorted data, it was incredibly fast—sometimes even beating the O(n log n) algorithms for small arrays. The graphs showed its true O(n) best-case behavior beautifully. However, on reverse-sorted arrays, watching it struggle with O(n²) performance really illustrated why algorithm selection matters. I learned that InsertionSort isn't just an academic example; it's actually used in practice for small subarrays in optimized implementations of QuickSort and MergeSort.

The different data types revealed fascinating algorithm behaviors. Nearly sorted data showed InsertionSort's adaptivity, while arrays with many duplicates exposed how three-way partitioning could improve QuickSort. Sorted data was ironically the worst case for basic QuickSort but the best case for InsertionSort—a reminder that "sorted" isn't uniformly good or bad, it depends entirely on your algorithm.

Perhaps the most important lesson was understanding the trade-offs: speed versus memory usage (QuickSort vs MergeSort), predictability versus average performance (HeapSort vs QuickSort), and versatility versus specialization (general O(n log n) algorithms vs InsertionSort for small/nearly-sorted data). There's no single "best" sorting algorithm—the right choice depends on your data characteristics, memory constraints, stability requirements, and performance predictability needs.

This empirical work transformed sorting algorithms from abstract concepts into practical tools. Seeing the theory validated by measurements, but also seeing where real-world factors like cache behavior and constant factors matter, gave me a much deeper appreciation for algorithm analysis and the engineering decisions behind standard library implementations.

## Requirements

- Python 3.7+
- matplotlib
- numpy

Install dependencies:
```bash
pip install matplotlib numpy
```

## Author

Laboratory work completed as part of Object-Oriented Programming course.

---

**Note**: This project provides both educational insights and practical performance data for understanding sorting algorithm behavior in real-world scenarios.
