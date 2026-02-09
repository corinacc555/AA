"""
Test Suite for Fibonacci Algorithms
Verifies correctness of all implementations
"""

from fibonacci_algorithms import FibonacciAlgorithms, clear_memoization_cache


def test_fibonacci_correctness():
    """Test that all algorithms produce correct results."""
    
    # Known Fibonacci values for verification
    # F(0)=0, F(1)=1, F(2)=1, F(3)=2, F(4)=3, F(5)=5, F(6)=8, F(7)=13, 
    # F(8)=21, F(9)=34, F(10)=55, F(15)=610, F(20)=6765
    test_cases = [
        (0, 0),
        (1, 1),
        (2, 1),
        (3, 2),
        (4, 3),
        (5, 5),
        (6, 8),
        (7, 13),
        (8, 21),
        (9, 34),
        (10, 55),
        (15, 610),
        (20, 6765),
    ]
    
    algorithms = {
        'Naive Recursive': FibonacciAlgorithms.recursive_naive,
        'Iterative': FibonacciAlgorithms.iterative,
        'Memoized Recursive': FibonacciAlgorithms.recursive_memoized,
        'Matrix Exponentiation': FibonacciAlgorithms.matrix_exponentiation,
        'Dynamic Programming': FibonacciAlgorithms.dynamic_programming,
        'Binet Formula': FibonacciAlgorithms.binet_formula,
    }
    
    print("=" * 80)
    print("TESTING FIBONACCI ALGORITHMS CORRECTNESS")
    print("=" * 80)
    
    all_passed = True
    
    for algo_name, algo_func in algorithms.items():
        print(f"\nTesting {algo_name}...")
        passed = 0
        failed = 0
        
        for n, expected in test_cases:
            # Clear cache for memoized version
            if algo_name == 'Memoized Recursive':
                clear_memoization_cache()
            
            try:
                result = algo_func(n)
                
                if result == expected:
                    passed += 1
                else:
                    failed += 1
                    print(f"  ✗ FAIL: F({n}) = {result}, expected {expected}")
                    all_passed = False
            except Exception as e:
                failed += 1
                print(f"  ✗ ERROR: F({n}) raised {type(e).__name__}: {e}")
                all_passed = False
        
        if failed == 0:
            print(f"  ✓ All {passed} tests passed!")
        else:
            print(f"  Results: {passed} passed, {failed} failed")
    
    print("\n" + "=" * 80)
    if all_passed:
        print("ALL TESTS PASSED! ✓")
    else:
        print("SOME TESTS FAILED! ✗")
    print("=" * 80)
    
    return all_passed


def test_edge_cases():
    """Test edge cases and special values."""
    
    print("\n" + "=" * 80)
    print("TESTING EDGE CASES")
    print("=" * 80)
    
    # Test F(0) and F(1)
    print("\nBase cases:")
    print(f"F(0) = {FibonacciAlgorithms.iterative(0)} (expected: 0)")
    print(f"F(1) = {FibonacciAlgorithms.iterative(1)} (expected: 1)")
    
    # Test larger values
    print("\nLarger values:")
    n = 50
    result = FibonacciAlgorithms.iterative(n)
    print(f"F({n}) = {result} (using iterative)")
    
    n = 100
    result = FibonacciAlgorithms.matrix_exponentiation(n)
    print(f"F({n}) = {result} (using matrix exponentiation)")
    
    print("=" * 80)


def compare_efficiency_small():
    """Quick efficiency comparison for small input."""
    import time
    
    print("\n" + "=" * 80)
    print("QUICK EFFICIENCY COMPARISON (n=25)")
    print("=" * 80)
    
    n = 25
    
    algorithms = [
        ('Iterative', FibonacciAlgorithms.iterative),
        ('Memoized', FibonacciAlgorithms.recursive_memoized),
        ('Matrix', FibonacciAlgorithms.matrix_exponentiation),
        ('Binet', FibonacciAlgorithms.binet_formula),
    ]
    
    for name, func in algorithms:
        if name == 'Memoized':
            clear_memoization_cache()
        
        start = time.perf_counter()
        result = func(n)
        end = time.perf_counter()
        
        print(f"{name:15s}: {result:12d}  ({(end-start)*1000:.4f} ms)")
    
    print("=" * 80)


if __name__ == "__main__":
    # Run all tests
    test_fibonacci_correctness()
    test_edge_cases()
    compare_efficiency_small()
    
    print("\n" + "=" * 80)
    print("TEST SUITE COMPLETED")
    print("=" * 80)
    print("\nTo run the full analysis, execute: python main.py")
    print("=" * 80 + "\n")
