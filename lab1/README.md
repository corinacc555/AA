# Laboratory Work 1: Fibonacci Algorithms Analysis

**Study and Empirical Analysis of Algorithms for Determining Fibonacci N-th Term**

---

## 📋 Table of Contents
- [Objective](#objective)
- [Implemented Algorithms](#implemented-algorithms)
- [Input Format Properties](#input-format-properties)
- [Comparison Metric](#comparison-metric)
- [Empirical Analysis](#empirical-analysis)
- [Results](#results)
- [Conclusions](#conclusions)
- [How to Run](#how-to-run)

---

## 🎯 Objective

The goal of this laboratory work is to study, implement, and empirically analyze different algorithms for computing the n-th Fibonacci number. Through systematic performance measurement, we aim to understand the practical implications of different algorithmic approaches and time complexities.

---

## 🔧 Implemented Algorithms

### 1. **Naive Recursive** 
```python
F(n) = F(n-1) + F(n-2)
```
- **Time Complexity:** O(2^n) - Exponential
- **Space Complexity:** O(n) - Call stack depth
- **Characteristics:** 
  - Direct implementation of mathematical definition
  - Recalculates same values multiple times
  - Impractical for n > 35

### 2. **Iterative**
```python
Loop from 2 to n, maintaining previous two values
```
- **Time Complexity:** O(n) - Linear
- **Space Complexity:** O(1) - Constant
- **Characteristics:**
  - Memory efficient
  - Single pass through sequence
  - Reliable performance

### 3. **Recursive with Memoization** (Dynamic Programming - Top-down)
```python
F(n) with caching using @lru_cache
```
- **Time Complexity:** O(n) - Linear
- **Space Complexity:** O(n) - Cache storage
- **Characteristics:**
  - Combines recursion elegance with efficiency
  - Caches computed values
  - Fast after first computation

### 4. **Matrix Exponentiation**
```python
[[F(n+1), F(n)], [F(n), F(n-1)]] = [[1,1],[1,0]]^n
```
- **Time Complexity:** O(log n) - Logarithmic
- **Space Complexity:** O(log n) - Recursion stack
- **Characteristics:**
  - Uses fast exponentiation
  - Most efficient for very large n
  - Based on matrix power formula

### 5. **Dynamic Programming** (Bottom-up)
```python
Build array from F(0) to F(n)
```
- **Time Complexity:** O(n) - Linear
- **Space Complexity:** O(n) - Array storage
- **Characteristics:**
  - Stores all intermediate values
  - No recursion overhead
  - Predictable memory usage

### 6. **Binet's Formula** (Closed-form)
```python
F(n) = (φ^n - ψ^n) / √5, where φ = (1+√5)/2
```
- **Time Complexity:** O(1) - Constant*
- **Space Complexity:** O(1) - Constant
- **Characteristics:**
  - Direct mathematical calculation
  - Fastest theoretical complexity
  - Subject to floating-point precision errors
  - *Assuming constant-time arithmetic

---

## 📊 Input Format Properties

The test inputs are carefully selected to reveal algorithm behavior across different scales:

### Small Range (n = 5, 10, 15, 20)
- **Purpose:** Test all algorithms including exponential ones
- **Observation:** Even naive recursive is manageable
- **Focus:** Baseline comparison, overhead analysis

### Medium Range (n = 25, 30, 35)
- **Purpose:** Identify where exponential algorithm becomes impractical
- **Observation:** Naive recursive takes seconds to minutes
- **Focus:** Transition point analysis

### Large Range (n = 50, 100, 150, 200)
- **Purpose:** Compare efficient algorithms only
- **Observation:** Clear separation between linear and logarithmic
- **Focus:** Scalability assessment

### Very Large Range (n = 500, 1000)
- **Purpose:** Stress test for highly efficient algorithms
- **Observation:** Matrix exponentiation and Binet's formula shine
- **Focus:** Asymptotic behavior verification

**Coverage Strategy:**
- Dense sampling in critical ranges
- Sparse sampling for large values
- Exponential growth pattern to cover multiple orders of magnitude

---

## 📏 Comparison Metric

### Primary Metric: **Execution Time (Wall-clock Time)**

**Why Execution Time?**
1. **Real-world relevance:** Measures actual performance users experience
2. **Comprehensive:** Includes all overhead (recursion, memory allocation, cache)
3. **Practical:** Easy to measure and understand
4. **Comparable:** Fair comparison across different algorithmic approaches

**Measurement Details:**
- **Tool:** Python's `time.perf_counter()` for high precision
- **Precision:** Nanosecond resolution on most systems
- **Iterations:** 3 runs per test, averaged for reliability
- **Environment:** Same system, same conditions for all tests

**What It Captures:**
- Algorithm efficiency (primary factor)
- Implementation overhead
- Memory access patterns
- Cache effects
- Python interpreter overhead

**Limitations:**
- System-dependent results
- Cannot distinguish between constant factors of same complexity
- Doesn't directly measure memory usage

---

## 🔬 Empirical Analysis

### Methodology

1. **Controlled Environment:**
   - Single Python process
   - No background interference
   - Consistent system state

2. **Statistical Approach:**
   - Multiple iterations (3 runs)
   - Averaged results
   - Outlier handling (timeouts for very slow algorithms)

3. **Safety Measures:**
   - Skip naive recursive for n > 35 (too slow)
   - Recursion limit handling
   - Error detection and reporting

### Expected Observations

#### Time Complexity Classes:

**O(2^n) - Exponential (Naive Recursive):**
- Doubles execution time with each increment
- Becomes impractical very quickly
- Clear exponential growth pattern

**O(n) - Linear (Iterative, Memoized, DP):**
- Proportional increase with n
- Stable and predictable
- Small differences due to implementation overhead

**O(log n) - Logarithmic (Matrix Exponentiation):**
- Minimal growth even for large n
- Significantly faster than linear for large inputs
- Best asymptotic performance

**O(1) - Constant (Binet's Formula):**
- Constant time regardless of n
- Fastest for all valid inputs
- Limited by floating-point precision

---

## 📈 Results

### Key Findings

1. **Naive Recursive is Impractical:**
   - Takes exponentially longer as n increases
   - Unusable beyond n ≈ 35-40
   - Demonstrates importance of algorithm choice

2. **Linear Algorithms Perform Similarly:**
   - Iterative slightly faster (less overhead)
   - Memoized recursive close behind
   - Dynamic programming comparable

3. **Matrix Exponentiation Excels for Large n:**
   - Outperforms linear algorithms for n > 50
   - Logarithmic growth clearly visible
   - Best for very large inputs

4. **Binet's Formula is Fastest (with caveats):**
   - Constant time execution
   - Extremely fast for all tested values
   - Precision issues may limit practical use for very large n

### Performance Rankings

**Small Inputs (n ≤ 20):**
1. Binet's Formula (fastest)
2. Matrix Exponentiation
3. Iterative / Memoized / DP (similar)
4. Naive Recursive (manageable)

**Medium Inputs (20 < n ≤ 35):**
1. Binet's Formula
2. Matrix Exponentiation
3. Iterative / Memoized / DP
4. Naive Recursive (very slow)

**Large Inputs (n > 100):**
1. Binet's Formula
2. Matrix Exponentiation (clear advantage over linear)
3. Iterative
4. Memoized / DP

---

## 💡 Conclusions

### 1. **Algorithm Choice Matters Significantly**
The difference between O(2^n) and O(n) is dramatic in practice. The naive recursive algorithm becomes unusable at relatively small inputs (n ≈ 35), while efficient algorithms handle n = 1000 easily.

### 2. **Asymptotic Complexity Predicts Real Performance**
Our empirical results align with theoretical complexity analysis:
- Exponential algorithms scale terribly
- Linear algorithms scale predictably
- Logarithmic algorithms scale excellently
- Constant-time algorithms are consistently fastest

### 3. **Trade-offs Exist Between Different Approaches**

**Simplicity vs. Performance:**
- Naive recursive: Simple to understand, terrible performance
- Iterative: Simple and efficient

**Space vs. Time:**
- Iterative: O(1) space, O(n) time
- Memoized: O(n) space, O(n) time (cached)
- DP with array: O(n) space, O(n) time

**Theoretical vs. Practical:**
- Binet's formula: O(1) theoretically, but precision issues
- Matrix exponentiation: Best practical performance for large n

### 4. **Implementation Details Matter**
Among O(n) algorithms, iterative is slightly faster due to:
- No recursion overhead
- No cache management
- Minimal memory allocation
- Better cache locality

### 5. **Scalability Insights**

**For Small Problems (n < 30):**
- Any efficient algorithm works fine
- Simplicity matters more than complexity
- Overhead can dominate actual computation

**For Medium Problems (30 ≤ n ≤ 100):**
- Clear separation between good and bad algorithms
- Linear algorithms are practical and reliable choice

**For Large Problems (n > 100):**
- O(log n) and O(1) significantly outperform O(n)
- Matrix exponentiation recommended for integer precision
- Binet's formula if precision loss acceptable

### 6. **Practical Recommendations**

**General Purpose:** Use **Iterative** algorithm
- Simple, fast, memory efficient
- No edge cases or precision issues
- Best balance of simplicity and performance

**Very Large n:** Use **Matrix Exponentiation**
- Best scalability
- Maintains integer precision
- Predictable performance

**Quick Estimates:** Use **Binet's Formula**
- Fastest possible
- Good enough for approximate values
- Beware of precision for very large n

**Educational/Recursive Context:** Use **Memoized Recursive**
- Demonstrates dynamic programming
- Combines elegance with efficiency
- Good teaching example

### 7. **Learning Outcomes**

This laboratory demonstrates:
- **Critical thinking:** Analyzing multiple approaches to same problem
- **Empirical validation:** Theory matches practice
- **Performance awareness:** Algorithm choice has real consequences
- **Engineering judgment:** Understanding trade-offs for different scenarios

---

## 🚀 How to Run

### Prerequisites
```bash
pip install -r requirements.txt
```

Required packages:
- matplotlib (for visualizations)
- numpy (for numerical operations)

### Running the Analysis

**Full Analysis (recommended):**
```bash
python main.py
```
This will:
- Run all algorithms on test inputs
- Generate performance comparison tables
- Create visualization plots
- Save results to JSON

**Quick Verification:**
```bash
python main.py --quick
```
Quick test that all algorithms work correctly.

**Interactive Mode:**
```bash
python main.py --interactive
```
Interactive menu for testing individual algorithms.

### Output Files

After running the full analysis:
- `performance_results.json` - Raw numerical data
- `all_algorithms_comparison.png` - All algorithms (linear scale)
- `algorithms_log_scale.png` - Logarithmic scale view
- `efficient_algorithms.png` - Excluding naive recursive
- `complexity_comparison.png` - By complexity class

### Individual Modules

Test individual components:
```bash
# Test algorithms
python fibonacci_algorithms.py

# Test performance analyzer
python performance_analyzer.py

# Generate visualizations (requires results file)
python visualizer.py
```

---

## 📚 References

1. Fibonacci sequence properties and mathematical foundations
2. Algorithm complexity analysis
3. Dynamic programming techniques
4. Matrix exponentiation method
5. Binet's formula derivation

---

## 👨‍🎓 Author

Laboratory Work 1 - Algorithm Analysis Course

*Completed: February 2026*

---

## 📝 License

This project is for educational purposes.
