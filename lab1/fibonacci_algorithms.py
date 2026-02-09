"""
Laboratory Work 1: Fibonacci Algorithms Implementation
Study and Empirical Analysis of Algorithms for Determining Fibonacci N-th Term

This module contains different implementations of Fibonacci algorithms.
"""

import sys
from functools import lru_cache


class FibonacciAlgorithms:
    """Collection of different Fibonacci algorithm implementations."""
    
    @staticmethod
    def recursive_naive(n: int) -> int:
        """
        Algorithm 1: Naive Recursive Implementation
        
        Time Complexity: O(2^n) - Exponential
        Space Complexity: O(n) - Due to call stack
        
        This is the most straightforward but inefficient implementation.
        It recalculates the same values multiple times.
        
        Args:
            n: The position in Fibonacci sequence (0-indexed)
            
        Returns:
            The n-th Fibonacci number
        """
        if n <= 1:
            return n
        return FibonacciAlgorithms.recursive_naive(n - 1) + FibonacciAlgorithms.recursive_naive(n - 2)
    
    @staticmethod
    def iterative(n: int) -> int:
        """
        Algorithm 2: Iterative Implementation
        
        Time Complexity: O(n) - Linear
        Space Complexity: O(1) - Constant
        
        This implementation uses iteration to avoid redundant calculations.
        It's much more efficient than naive recursion.
        
        Args:
            n: The position in Fibonacci sequence (0-indexed)
            
        Returns:
            The n-th Fibonacci number
        """
        if n <= 1:
            return n
        
        prev, curr = 0, 1
        for _ in range(2, n + 1):
            prev, curr = curr, prev + curr
        
        return curr
    
    @staticmethod
    @lru_cache(maxsize=None)
    def recursive_memoized(n: int) -> int:
        """
        Algorithm 3: Recursive with Memoization (Dynamic Programming)
        
        Time Complexity: O(n) - Linear
        Space Complexity: O(n) - For cache and call stack
        
        Uses Python's built-in LRU cache to store previously computed values.
        Combines the elegance of recursion with the efficiency of memoization.
        
        Args:
            n: The position in Fibonacci sequence (0-indexed)
            
        Returns:
            The n-th Fibonacci number
        """
        if n <= 1:
            return n
        return FibonacciAlgorithms.recursive_memoized(n - 1) + FibonacciAlgorithms.recursive_memoized(n - 2)
    
    @staticmethod
    def matrix_exponentiation(n: int) -> int:
        """
        Algorithm 4: Matrix Exponentiation
        
        Time Complexity: O(log n) - Logarithmic
        Space Complexity: O(log n) - For recursion stack
        
        Uses matrix multiplication and fast exponentiation.
        This is the most efficient algorithm for very large n.
        
        Based on the matrix formula:
        | F(n+1)  F(n)   |   | 1  1 |^n
        | F(n)    F(n-1) | = | 1  0 |
        
        Args:
            n: The position in Fibonacci sequence (0-indexed)
            
        Returns:
            The n-th Fibonacci number
        """
        if n <= 1:
            return n
        
        def matrix_multiply(a, b):
            """Multiply two 2x2 matrices."""
            return [
                [a[0][0] * b[0][0] + a[0][1] * b[1][0], a[0][0] * b[0][1] + a[0][1] * b[1][1]],
                [a[1][0] * b[0][0] + a[1][1] * b[1][0], a[1][0] * b[0][1] + a[1][1] * b[1][1]]
            ]
        
        def matrix_power(matrix, n):
            """Compute matrix^n using fast exponentiation."""
            if n == 1:
                return matrix
            
            if n % 2 == 0:
                half = matrix_power(matrix, n // 2)
                return matrix_multiply(half, half)
            else:
                return matrix_multiply(matrix, matrix_power(matrix, n - 1))
        
        base_matrix = [[1, 1], [1, 0]]
        result_matrix = matrix_power(base_matrix, n)
        return result_matrix[0][1]
    
    @staticmethod
    def dynamic_programming(n: int) -> int:
        """
        Algorithm 5: Dynamic Programming (Bottom-up with array)
        
        Time Complexity: O(n) - Linear
        Space Complexity: O(n) - Array storage
        
        Builds up the solution from F(0) to F(n) storing all intermediate values.
        
        Args:
            n: The position in Fibonacci sequence (0-indexed)
            
        Returns:
            The n-th Fibonacci number
        """
        if n <= 1:
            return n
        
        dp = [0] * (n + 1)
        dp[1] = 1
        
        for i in range(2, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]
        
        return dp[n]
    
    @staticmethod
    def binet_formula(n: int) -> int:
        """
        Algorithm 6: Binet's Formula (Closed-form expression)
        
        Time Complexity: O(1) - Constant (assuming constant-time arithmetic)
        Space Complexity: O(1) - Constant
        
        Uses the mathematical closed-form formula:
        F(n) = (φ^n - ψ^n) / √5
        where φ = (1 + √5) / 2 (golden ratio)
        and ψ = (1 - √5) / 2
        
        Note: Subject to floating-point precision errors for large n.
        
        Args:
            n: The position in Fibonacci sequence (0-indexed)
            
        Returns:
            The n-th Fibonacci number
        """
        sqrt_5 = 5 ** 0.5
        phi = (1 + sqrt_5) / 2
        psi = (1 - sqrt_5) / 2
        
        return int((phi ** n - psi ** n) / sqrt_5)


# Clear memoization cache function
def clear_memoization_cache():
    """Clear the memoization cache for recursive_memoized function."""
    FibonacciAlgorithms.recursive_memoized.cache_clear()


# Dictionary mapping algorithm names to their functions
ALGORITHMS = {
    'recursive_naive': FibonacciAlgorithms.recursive_naive,
    'iterative': FibonacciAlgorithms.iterative,
    'recursive_memoized': FibonacciAlgorithms.recursive_memoized,
    'matrix_exponentiation': FibonacciAlgorithms.matrix_exponentiation,
    'dynamic_programming': FibonacciAlgorithms.dynamic_programming,
    'binet_formula': FibonacciAlgorithms.binet_formula
}


if __name__ == "__main__":
    # Simple test
    n = 10
    print(f"Testing algorithms for F({n}):")
    print("-" * 50)
    
    for name, func in ALGORITHMS.items():
        if name == 'recursive_memoized':
            clear_memoization_cache()
        
        result = func(n)
        print(f"{name:25s}: {result}")
