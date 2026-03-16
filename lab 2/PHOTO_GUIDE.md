# Photo/Graph Guide for Lab 2AA Report

## Required Images and Their Locations

### 1. Algorithm Implementation Screenshots

#### QuickSort (Page ~7)
- **File to screenshot**: `sorting_algorithms.py`
- **Lines to capture**: Lines showing `quicksort()`, `_quicksort_helper()`, and `_partition()` methods
- **Replace**: `[INSERT SCREENSHOT HERE]` in Figure \ref{fig:quicksort_impl}
- **What to show**: The optimized QuickSort implementation with median-of-three pivot

#### Terminal Output - QuickSort
- **Command to run**: `python main.py --quick`
- **What to capture**: Terminal output showing QuickSort test results with comparisons and swaps
- **Replace**: `[INSERT SCREENSHOT HERE]` in Figure \ref{fig:quicksort_results}

#### QuickSort Graph
- **File**: `time_comparison_random.png`
- **Replace**: `[INSERT GRAPH HERE]` in Figure \ref{fig:quicksort_graph}
- **Note**: Can highlight/circle the QuickSort (blue) line

---

#### MergeSort (Page ~8)
- **File to screenshot**: `sorting_algorithms.py`
- **Lines to capture**: `mergesort()`, `_mergesort_helper()`, and `_merge()` methods
- **Replace**: `[INSERT SCREENSHOT HERE]` in Figure \ref{fig:mergesort_impl}

#### MergeSort Comparison Graph
- **File**: `all_metrics_random.png`
- **Replace**: `[INSERT GRAPH HERE]` in Figure \ref{fig:mergesort_graph}
- **Note**: Shows MergeSort (orange line) with all metrics

#### MergeSort Data Types
- **File**: `mergesort_data_types.png`
- **Replace**: `[INSERT GRAPH HERE]` in Figure \ref{fig:mergesort_datatypes}
- **Shows**: MergeSort performance on all 5 data types (consistent curves)

---

#### HeapSort (Page ~9)
- **File to screenshot**: `sorting_algorithms.py`
- **Lines to capture**: `heapsort()` and `_heapify()` methods
- **Replace**: `[INSERT SCREENSHOT HERE]` in Figure \ref{fig:heapsort_impl}

#### HeapSort Comparisons
- **File**: `comparisons_random.png`
- **Replace**: `[INSERT GRAPH HERE]` in Figure \ref{fig:heapsort_comparisons}
- **Note**: HeapSort (green line) shows highest comparison count

#### HeapSort Data Types
- **File**: `heapsort_data_types.png`
- **Replace**: `[INSERT GRAPH HERE]` in Figure \ref{fig:heapsort_datatypes}

---

#### InsertionSort (Page ~10)
- **File to screenshot**: `sorting_algorithms.py`
- **Lines to capture**: `insertion_sort()` method
- **Replace**: `[INSERT SCREENSHOT HERE]` in Figure \ref{fig:insertion_impl}

#### InsertionSort Quadratic Growth
- **File**: `time_comparison_random.png`
- **Replace**: `[INSERT GRAPH HERE]` in Figure \ref{fig:insertion_quadratic}
- **Note**: InsertionSort (red line) shows clear O(n²) curve rising steeply

#### InsertionSort Data Types
- **File**: `insertion_sort_data_types.png`
- **Replace**: `[INSERT GRAPH HERE]` in Figure \ref{fig:insertion_datatypes}
- **Shows**: Dramatic difference between sorted (flat/fast) and reverse (steep/slow)

---

### 2. Comparative Analysis Graphs (Pages ~11-13)

#### All Metrics Random Data
- **File**: `all_metrics_random.png`
- **Replace**: `[INSERT GRAPH HERE]` in Figure \ref{fig:all_metrics_random}
- **Shows**: 3 subplots (time, comparisons, swaps) with all 4 algorithms

#### Sorted Data Comparison
- **File**: `time_comparison_sorted.png`
- **Replace**: `[INSERT GRAPH HERE]` in Figure \ref{fig:sorted_comparison}
- **Shows**: InsertionSort dramatically faster (flat line), others similar

#### Reverse Sorted Comparison
- **File**: `time_comparison_reverse.png`
- **Replace**: `[INSERT GRAPH HERE]` in Figure \ref{fig:reverse_comparison}
- **Shows**: InsertionSort worst case (steep curve)

#### Comparisons Analysis
- **File**: `comparisons_random.png`
- **Replace**: `[INSERT GRAPH HERE]` in Figure \ref{fig:comparisons_analysis}
- **Shows**: All 4 algorithms with HeapSort highest, InsertionSort exponential

#### Swaps Analysis
- **File**: `swaps_random.png`
- **Replace**: `[INSERT GRAPH HERE]` in Figure \ref{fig:swaps_analysis}
- **Shows**: Data movement operations for all algorithms

#### Final Comparison
- **File**: `time_comparison_nearly_sorted.png`
- **Replace**: `[INSERT GRAPH HERE]` in Figure \ref{fig:final_comparison}
- **Shows**: InsertionSort excelling on nearly-sorted data

---

## How to Insert Images in LaTeX

### For PNG files:
Replace:
```latex
\fbox{\parbox{0.9\linewidth}{\centering \textbf{[INSERT GRAPH HERE]} \\ File: xxx.png}}
```

With:
```latex
\includegraphics[width=0.9\linewidth]{filename.png}
```

### For screenshots:
1. Take screenshot of relevant code/terminal
2. Save as PNG file (e.g., `quicksort_code.png`)
3. Replace the `\fbox` line with:
```latex
\includegraphics[width=0.9\linewidth]{quicksort_code.png}
```

---

## Summary of Files Needed

**Generated Graphs** (already exist):
- time_comparison_random.png
- time_comparison_sorted.png
- time_comparison_reverse.png
- time_comparison_nearly_sorted.png
- comparisons_random.png
- swaps_random.png
- all_metrics_random.png
- quicksort_data_types.png
- mergesort_data_types.png
- heapsort_data_types.png
- insertion_sort_data_types.png

**Screenshots to Take** (4 total):
1. QuickSort implementation code
2. MergeSort implementation code
3. HeapSort implementation code
4. InsertionSort implementation code
5. Terminal output from `python main.py --quick`

**Note**: All PNG graphs are already in `d:\LAB 2\lab 2AA\` folder. You just need to take screenshots of the code and terminal output.
