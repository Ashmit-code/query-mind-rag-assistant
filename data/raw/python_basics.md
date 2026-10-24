# Python Fundamentals and Core Programming Guide

A comprehensive, production-grade guide covering Python syntax, data types, control flow, functions, built-in data structures, OOP, file handling, and algorithms.

## Python Syntax, Variables, and Data Types

Python is a dynamically typed, interpreted language. Variables do not require explicit type declaration; the type is inferred at runtime.

### Syntax and Implementation

```python
# Variable declarations and basic types
name: str = "Alice"              # String
age: int = 25                    # Integer
pi: float = 3.14159              # Float
is_active: bool = True           # Boolean
data: None = None                # NoneType (absence of value)

# Type conversion (casting)
str_to_int = int("42")
int_to_float = float(10)
num_to_str = str(123)

# Formatted string output (f-strings)
print(f"User: {name}, Age: {age}, Active: {is_active}")
```

### Example Usage and Output

```python
print(f"Casting: {type(str_to_int)} -> {str_to_int}")
# Output:
# User: Alice, Age: 25, Active: True
# Casting: <class 'int'> -> 42
```

### Key Rules
- Python uses indentation (4 spaces) rather than braces `{}` to define code blocks.
- Primitive types are immutable in Python (`int`, `float`, `str`, `tuple`, `bool`).

---

## Python Conditional Statements and Control Flow

Conditionals control execution flow using `if`, `elif`, and `else` blocks with boolean operators (`and`, `or`, `not`).

### Syntax and Implementation

```python
def check_grade(score: float) -> str:
    """Classifies student grade based on percentage score."""
    if score >= 90:
        return "Grade A"
    elif score >= 80:
        return "Grade B"
    elif score >= 70:
        return "Grade C"
    elif score >= 60:
        return "Grade D"
    else:
        return "Grade F"

# Ternary operator (conditional expression)
status = "Adult" if age >= 18 else "Minor"
```

### Example Usage and Output

```python
print(check_grade(85.5))  # Output: Grade B
print(check_grade(52.0))  # Output: Grade F
```

---

## Python Loops and Iteration (`for` and `while`)

Python supports `for` loops (iterating over iterables) and `while` loops (conditional iteration) along with `break`, `continue`, and `else` clauses.

### Syntax and Implementation

```python
# For loop with range
sum_even = 0
for i in range(1, 11):
    if i % 2 == 0:
        sum_even += i

# While loop with break and continue
counter = 0
while counter < 10:
    counter += 1
    if counter == 3:
        continue  # skip 3
    if counter == 7:
        break     # terminate at 7

# Enumerate for index-value pairs
languages = ["Python", "JavaScript", "Java", "C++", "C"]
for index, lang in enumerate(languages, start=1):
    print(f"{index}. {lang}")
```

### Complexity Analysis
- Iterating through an iterable of length $N$ takes $O(N)$ time.

---

## Python Functions, Scope, and Recursion

Functions are declared with `def`. Python supports positional arguments, keyword arguments, default parameters, variable-length arguments (`*args`, `**kwargs`), and recursion.

### Syntax and Implementation

```python
def calculate_factorial(n: int) -> int:
    """
    Computes factorial of non-negative integer n using recursion.
    Base case: n <= 1 -> 1
    Recursive case: n * factorial(n - 1)
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    if n <= 1:
        return 1
    return n * calculate_factorial(n - 1)

def greet(name: str, greeting: str = "Hello", *tags, **metadata) -> str:
    tags_str = ", ".join(tags)
    return f"{greeting}, {name}! Tags: [{tags_str}] Meta: {metadata}"
```

### Example Usage and Output

```python
print(calculate_factorial(5))  # Output: 120
print(greet("Bob", "Welcome", "dev", "python", role="admin"))
# Output: Welcome, Bob! Tags: [dev, python] Meta: {'role': 'admin'}
```

### Complexity Analysis
- **Time Complexity**: $O(N)$ for recursive factorial.
- **Space Complexity**: $O(N)$ call stack space.

---

## Python Lists and Tuples (Sequential Data Structures)

Lists are mutable ordered collections. Tuples are immutable ordered collections.

### Syntax and Implementation

```python
# List operations
fruits = ["apple", "banana", "cherry"]
fruits.append("date")        # Append to end O(1)
fruits.insert(1, "blueberry")# Insert at index O(N)
fruits.pop()                 # Remove from end O(1)
fruits.sort()                # In-place sort O(N log N)

# Slicing syntax: list[start:stop:step]
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
evens = numbers[0::2]        # [0, 2, 4, 6, 8]
reversed_nums = numbers[::-1]# [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

# Tuples (immutable)
point = (10, 20)
x, y = point  # Tuple unpacking
```

### Key Operations & Complexities
- Access by index: $O(1)$
- Append / Pop end: $O(1)$
- Search / Remove by value: $O(N)$

---

## Python Dictionaries and Sets (Hash-Based Data Structures)

Dictionaries store key-value pairs with $O(1)$ average lookup. Sets store unique elements with $O(1)$ membership testing.

### Syntax and Implementation

```python
# Dictionary operations
student = {
    "id": 101,
    "name": "Sarah",
    "gpa": 3.8,
    "courses": ["Algorithms", "Databases"]
}

student["email"] = "sarah@example.com"  # Insert / Update O(1)
val = student.get("age", 20)             # Safe get with default fallback

# Iteration
for key, value in student.items():
    print(f"{key}: {value}")

# Sets (unique elements, set algebra)
set_a = {1, 2, 3, 4, 5}
set_b = {4, 5, 6, 7, 8}

union_set = set_a | set_b         # {1, 2, 3, 4, 5, 6, 7, 8}
intersect_set = set_a & set_b     # {4, 5}
diff_set = set_a - set_b          # {1, 2, 3}
```

### Complexity Analysis
- Lookup, Insert, Delete: $O(1)$ average time complexity using hash tables.

---

## Python String Manipulation and Common Algorithms

Strings in Python are immutable sequences of Unicode characters.

### Syntax and Implementation

```python
def is_palindrome(s: str) -> bool:
    """Checks if a string is a palindrome ignoring case and non-alphanumeric chars."""
    cleaned = "".join(char.lower() for char in s if char.isalnum())
    return cleaned == cleaned[::-1]

def reverse_string(s: str) -> str:
    """Reverses a string using slicing."""
    return s[::-1]

# Common string methods
raw_text = "  python,javascript,java  "
cleaned = raw_text.strip()                # "python,javascript,java"
tokens = cleaned.split(",")               # ['python', 'javascript', 'java']
joined = " | ".join(tokens)               # "python | javascript | java"
```

### Example Usage and Output

```python
print(is_palindrome("A man, a plan, a canal: Panama"))  # Output: True
print(reverse_string("OpenAI"))                         # Output: IAnepO
```

---

## Python Object-Oriented Programming (OOP)

Python supports classes, constructors (`__init__`), encapsulation, inheritance, method overriding, and polymorphism.

### Syntax and Implementation

```python
class Animal:
    """Base class demonstrating encapsulation and inheritance."""
    def __init__(self, name: str, species: str):
        self.name = name           # Public attribute
        self._species = species    # Protected attribute convention

    def speak(self) -> str:
        return "Generic animal sound"

    def describe(self) -> str:
        return f"{self.name} is a {self._species}"

class Dog(Animal):
    """Derived class demonstrating method overriding and super()."""
    def __init__(self, name: str, breed: str):
        super().__init__(name, species="Canine")
        self.breed = breed

    def speak(self) -> str:
        return "Woof! Woof!"

class Cat(Animal):
    def __init__(self, name: str):
        super().__init__(name, species="Feline")

    def speak(self) -> str:
        return "Meow!"

# Polymorphism demonstration
def play_sound(animal: Animal):
    print(f"{animal.name} says: {animal.speak()}")
```

### Example Usage and Output

```python
dog = Dog("Buddy", "Golden Retriever")
cat = Cat("Whiskers")
play_sound(dog)  # Output: Buddy says: Woof! Woof!
play_sound(cat)  # Output: Whiskers says: Meow!
```

---

## Python Exception Handling (`try`, `except`, `finally`)

Robust error handling using `try`, `except`, `else`, `finally`, and custom exceptions.

### Syntax and Implementation

```python
class InsufficientFundsError(Exception):
    """Custom application exception."""
    pass

class BankAccount:
    def __init__(self, balance: float):
        self.balance = balance

    def withdraw(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be strictly positive.")
        if amount > self.balance:
            raise InsufficientFundsError(f"Cannot withdraw ${amount}. Current balance: ${self.balance}.")
        self.balance -= amount
        return self.balance

# Safe execution with try-except-finally
try:
    account = BankAccount(100.0)
    account.withdraw(150.0)
except InsufficientFundsError as e:
    print(f"Transaction Denied: {e}")
except ValueError as e:
    print(f"Invalid Input: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    print("Banking session closed.")
```

### Output
```
Transaction Denied: Cannot withdraw $150.0. Current balance: $100.0.
Banking session closed.
```

---

## Python File I/O (Reading and Writing Files)

Python provides the `open()` function. Using the `with` context manager guarantees automatic file closing even if errors occur.

### Syntax and Implementation

```python
# Writing to a text file
def write_sample_file(filepath: str, lines: list[str]):
    with open(filepath, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")

# Reading from a text file line-by-line
def read_sample_file(filepath: str) -> list[str]:
    records = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            records.append(line.strip())
    return records
```

### Complexity & Best Practices
- `with open(...)` automatically handles file resource cleanup (implements context management protocol `__enter__` and `__exit__`).
- $O(N)$ time to read $N$ lines, $O(N)$ memory if read into a list, or $O(1)$ memory if iterated line by line.

---

## Python Essential Algorithms: Linear Search and Bubble Sort

Fundamental searching and sorting algorithms implemented in Python.

### Syntax and Implementation

```python
def linear_search(arr: list[int], target: int) -> int:
    """Finds index of target in arr using linear search. Returns -1 if not found."""
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1

def bubble_sort(arr: list[int]) -> list[int]:
    """Sorts list in ascending order using Bubble Sort with early stopping optimization."""
    a = arr.copy()
    n = len(a)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]  # Pythonic swap
                swapped = True
        if not swapped:
            break
    return a
```

### Example Usage and Output

```python
nums = [64, 34, 25, 12, 22, 11, 90]
print(linear_search(nums, 22))    # Output: 4
print(bubble_sort(nums))          # Output: [11, 12, 22, 25, 34, 64, 90]
```

### Complexity Analysis
- **Linear Search**: $O(N)$ time, $O(1)$ space.
- **Bubble Sort**: $O(N^2)$ worst/average time, $O(N)$ best case (already sorted), $O(1)$ auxiliary space.
