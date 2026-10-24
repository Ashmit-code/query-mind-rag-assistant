# Python Core Language Features and Idioms

A comprehensive reference for essential Python programming paradigms, syntactic constructs, and memory semantics.

## Python List Comprehensions

List comprehensions provide a concise way to create lists based on existing iterables with optional filtering and transformation.

### Syntax and Implementation

```python
# General syntax: [expression for item in iterable if condition]
squares = [x**2 for x in range(10) if x % 2 == 0]

# Nested list comprehension for matrix flattening
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [val for row in matrix for val in row]
```

### Example Usage and Output

```python
words = ["python", "information", "retrieval", "search", "ranking"]
uppercase_long_words = [w.upper() for w in words if len(w) > 6]
print(uppercase_long_words)
# Output: ['INFORMATION', 'RETRIEVAL', 'RANKING']
```

### Complexity and Best Practices
- **Time Complexity**: $O(N)$ where $N$ is the number of items in the source iterable. The underlying C-level loop optimization makes comprehensions faster than equivalent manual `list.append()` loops in Python.
- **Space Complexity**: $O(N)$ space required to allocate the new list in memory. For large sequences where intermediate storage is unneeded, generator expressions are preferred.

---

## Python Generators and the `yield` Keyword

Generators are functions that produce items lazily on demand instead of computing them all at once and holding them in memory.

### Syntax and Implementation

```python
from typing import Generator

def fibonacci_sequence(limit: int) -> Generator[int, None, None]:
    """
    Generate Fibonacci numbers up to a specified count without storing the full sequence.
    """
    a, b = 0, 1
    count = 0
    while count < limit:
        yield a
        a, b = b, a + b
        count += 1
```

### Example Usage and Output

```python
gen = fibonacci_sequence(6)
for num in gen:
    print(num, end=" ")
# Output: 0 1 1 2 3 5
```

### Complexity Analysis
- **Time Complexity**: $O(1)$ per yielded element; $O(N)$ total to generate $N$ elements.
- **Space Complexity**: $O(1)$ memory consumption because only state variables (`a`, `b`, `count`) are preserved between `yield` calls.

---

## Python Decorators

Decorators allow you to dynamically modify or extend the behavior of a callable (function or method) without directly altering its source code.

### Syntax and Implementation

```python
import time
from functools import wraps
from typing import Callable, Any

def timer_decorator(func: Callable) -> Callable:
    """
    A decorator that measures and prints the execution duration of a function.
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start_time
        print(f"Function '{func.__name__}' executed in {duration:.6f}s")
        return result
    return wrapper

@timer_decorator
def process_data(n: int) -> int:
    return sum(i * i for i in range(n))
```

### Example Usage and Output

```python
val = process_data(100000)
# Output: Function 'process_data' executed in 0.006214s
```

### Key Principles
- Uses closure to encapsulate the original function and wrap execution.
- `@wraps(func)` from `functools` preserves original function metadata such as `__name__` and `__doc__`.
