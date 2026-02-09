# ALGORITHM 1: Naive Recursive
def fibonacci_naive_recursive(n):
    if n <= 1:
        return n
    return fibonacci_naive_recursive(n-1) + fibonacci_naive_recursive(n-2)