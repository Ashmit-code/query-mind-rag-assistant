# C++ Fundamentals and Core Programming Guide

A comprehensive, production-grade guide covering modern C++ syntax, I/O streams, pointers and references, manual and dynamic memory management, Object-Oriented Programming, Standard Template Library (STL) containers, templates, and algorithms.

## C++ Syntax, Structure, Namespaces, and Data Types

C++ is a high-performance, statically typed, compiled language offering both low-level hardware control and high-level abstractions.

### Syntax and Implementation

```cpp
#include <iostream>
#include <string>

// Namespace declaration prevents naming collisions
using namespace std;

int main() {
    // Primitive Data Types
    int age = 21;                         // 32-bit signed integer
    long long largeNumber = 9876543210LL; // 64-bit integer
    float temperature = 36.6f;            // 32-bit floating point
    double preciseValue = 3.1415926535;   // 64-bit double precision
    char grade = 'A';                     // Single character
    bool isEngineRunning = true;          // Boolean flag
    string language = "C++20";            // C++ std::string class

    // Console Output and Input
    cout << "Language: " << language << " | Grade: " << grade << endl;
    cout << "Size of double: " << sizeof(preciseValue) << " bytes" << endl;

    return 0; // Return 0 signifies successful execution
}
```

### Key Notes
- Every C++ executable requires a `main()` function returning an integer exit status.
- Uninitialized local variables contain garbage values in C++.

---

## C++ Functions: Pass-by-Value vs Pass-by-Reference

In C++, parameters can be passed by value (copy created), by pointer (`int*`), or by reference (`int&`). Passing by constant reference (`const string&`) avoids expensive copying.

### Syntax and Implementation

```cpp
#include <iostream>
#include <utility>
using namespace std;

// Pass by Value: original variables remain unchanged
void swapByValue(int a, int b) {
    int temp = a;
    a = b;
    b = temp;
}

// Pass by Reference (&): directly modifies callers' variables without copying
void swapByReference(int& a, int& b) {
    int temp = a;
    a = b;
    b = temp;
}

// Recursive Factorial
long long factorial(int n) {
    if (n < 0) return -1;
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

int main() {
    int x = 10, y = 20;
    swapByReference(x, y);
    cout << "Swapped: x=" << x << ", y=" << y << endl; // x=20, y=10
    return 0;
}
```

---

## C++ Pointers, References, and Dynamic Memory Management (`new` and `delete`)

Pointers store memory addresses of variables. Dynamic memory is allocated on the heap using `new` and must be explicitly deallocated using `delete` to prevent memory leaks.

### Syntax and Implementation

```cpp
#include <iostream>
using namespace std;

int main() {
    int val = 42;
    int* ptr = &val;  // ptr holds the memory address of val

    cout << "Value: " << val << endl;
    cout << "Address: " << ptr << endl;
    cout << "Dereferenced: " << *ptr << endl; // 42

    *ptr = 100; // Modifying value via pointer
    cout << "Updated val: " << val << endl;   // 100

    // Dynamic Allocation on Heap
    int* dynamicNum = new int(500);           // Allocate single int
    int* dynamicArr = new int[5]{1, 2, 3, 4, 5}; // Allocate heap array

    cout << "Dynamic array element 2: " << dynamicArr[2] << endl;

    // Deallocation (Mandatory in C++)
    delete dynamicNum;      // Free single memory block
    delete[] dynamicArr;    // Free array memory block
    dynamicNum = nullptr;   // Nullify dangling pointer
    dynamicArr = nullptr;

    return 0;
}
```

### Safety Rules
- Always match `new` with `delete`, and `new[]` with `delete[]`.
- Always set freed pointers to `nullptr` to avoid dangling pointer bugs.

---

## C++ Standard Template Library: `std::vector` and `std::string`

`std::vector` is a contiguous dynamic array offering $O(1)$ random access and $O(1)$ amortized insertion at the back.

### Syntax and Implementation

```cpp
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;

int main() {
    // std::vector operations
    vector<int> nums = {5, 2, 8, 1, 9};
    nums.push_back(10); // Append element O(1)
    nums.pop_back();    // Remove last element O(1)

    // Sort using STL
    sort(nums.begin(), nums.end()); // O(N log N)

    // Range-based for loop
    cout << "Sorted vector: ";
    for (const int& n : nums) {
        cout << n << " ";
    }
    cout << endl; // 1 2 5 8 9

    // std::string operations (reverse, substring)
    string str = "racecar";
    string reversed = str;
    reverse(reversed.begin(), reversed.end());
    bool isPalindrome = (str == reversed);

    cout << "Is palindrome: " << boolalpha << isPalindrome << endl; // true
    return 0;
}
```

---

## C++ STL Associative Containers: `std::map`, `std::unordered_map`, and `std::set`

`std::map` is an ordered associative container backed by Red-Black trees ($O(\log N)$). `std::unordered_map` is a hash table ($O(1)$ average).

### Syntax and Implementation

```cpp
#include <iostream>
#include <map>
#include <unordered_map>
#include <set>
using namespace std;

int main() {
    // 1. std::map (Sorted keys, O(log N) operations)
    map<string, int> wordFrequency;
    wordFrequency["apple"] = 3;
    wordFrequency["banana"] = 5;
    wordFrequency["cherry"] = 2;

    for (const auto& [word, count] : wordFrequency) {
        cout << word << ": " << count << endl; // Alphabetical order
    }

    // 2. std::unordered_map (Hash table, O(1) average operations)
    unordered_map<int, string> studentRecords;
    studentRecords[101] = "Alice";
    studentRecords[102] = "Bob";

    if (studentRecords.find(101) != studentRecords.end()) {
        cout << "Found ID 101: " << studentRecords[101] << endl;
    }

    // 3. std::set (Unique, ordered elements)
    set<int> uniqueIds = {40, 10, 20, 10, 30};
    cout << "Set size: " << uniqueIds.size() << endl; // 4
    return 0;
}
```

---

## C++ Object-Oriented Programming (Classes, Constructors, Encapsulation)

C++ classes encapsulate member variables and methods with access specifiers `public`, `private`, and `protected`.

### Syntax and Implementation

```cpp
#include <iostream>
#include <string>
using namespace std;

class Rectangle {
private:
    double width;
    double height;

public:
    // Parameterized constructor with member initializer list
    Rectangle(double w, double h) : width(w), height(h) {}

    // Default constructor
    Rectangle() : width(1.0), height(1.0) {}

    // Getter methods
    double getWidth() const { return width; }
    double getHeight() const { return height; }

    // Area calculation
    double getArea() const {
        return width * height;
    }

    // Perimeter calculation
    double getPerimeter() const {
        return 2 * (width + height);
    }
};

int main() {
    Rectangle rect(10.0, 5.0);
    cout << "Area: " << rect.getArea() << " | Perimeter: " << rect.getPerimeter() << endl;
    return 0;
}
```

---

## C++ Inheritance, Virtual Functions, and Polymorphism

Inheritance allows derived classes to inherit fields and methods from base classes. Virtual functions (`virtual`) enable dynamic dispatch (runtime polymorphism).

### Syntax and Implementation

```cpp
#include <iostream>
#include <string>
#include <vector>
using namespace std;

// Abstract Base Class
class Shape {
public:
    // Pure virtual function (creates an abstract class)
    virtual double calculateArea() const = 0;
    virtual void printName() const {
        cout << "Shape" << endl;
    }

    // Virtual destructor is mandatory when using base pointers for deletion
    virtual ~Shape() = default;
};

class Circle : public Shape {
private:
    double radius;
public:
    Circle(double r) : radius(r) {}

    double calculateArea() const override {
        return 3.1415926535 * radius * radius;
    }

    void printName() const override {
        cout << "Circle (r=" << radius << ")" << endl;
    }
};

class Square : public Shape {
private:
    double side;
public:
    Square(double s) : side(s) {}

    double calculateArea() const override {
        return side * side;
    }

    void printName() const override {
        cout << "Square (side=" << side << ")" << endl;
    }
};

int main() {
    // Polymorphic array of base class pointers
    vector<Shape*> shapes;
    shapes.push_back(new Circle(5.0));
    shapes.push_back(new Square(4.0));

    for (const Shape* s : shapes) {
        s->printName();
        cout << "Area: " << s->calculateArea() << endl;
    }

    // Cleanup
    for (Shape* s : shapes) delete s;
    return 0;
}
```

---

## C++ Templates (Generic Programming)

Templates enable functions and classes to operate with generic types without code duplication.

### Syntax and Implementation

```cpp
#include <iostream>
using namespace std;

// Generic Function Template
template <typename T>
T findMax(T a, T b) {
    return (a > b) ? a : b;
}

// Generic Class Template (e.g. Pair)
template <typename T1, typename T2>
class KeyValuePair {
private:
    T1 key;
    T2 value;
public:
    KeyValuePair(T1 k, T2 v) : key(k), value(v) {}

    void display() const {
        cout << "[" << key << " => " << value << "]" << endl;
    }
};

int main() {
    cout << findMax(10, 25) << endl;         // int specialization: 25
    cout << findMax(3.14, 2.71) << endl;     // double specialization: 3.14

    KeyValuePair<string, int> pair("score", 99);
    pair.display(); // [score => 99]
    return 0;
}
```

---

## C++ Exception Handling (`try`, `catch`, `throw`)

C++ provides structured exception handling using `try`, `catch`, and standard library exceptions from `<stdexcept>`.

### Syntax and Implementation

```cpp
#include <iostream>
#include <stdexcept>
using namespace std;

double divide(double numerator, double denominator) {
    if (denominator == 0.0) {
        throw invalid_argument("Division by zero error.");
    }
    return numerator / denominator;
}

int main() {
    try {
        double result = divide(10.0, 0.0);
        cout << "Result: " << result << endl;
    } catch (const invalid_argument& e) {
        cerr << "Caught Exception: " << e.what() << endl;
    } catch (const exception& e) {
        cerr << "Standard Exception: " << e.what() << endl;
    }
    return 0;
}
```

---

## C++ Essential Algorithms: Binary Search and Bubble Sort

Algorithmic implementations in standard C++.

### Syntax and Implementation

```cpp
#include <iostream>
#include <vector>
using namespace std;

// Iterative Binary Search: O(log N)
int binarySearch(const vector<int>& arr, int target) {
    int left = 0;
    int right = arr.size() - 1;

    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (arr[mid] == target) {
            return mid;
        } else if (arr[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    return -1;
}

// Bubble Sort: O(N^2)
void bubbleSort(vector<int>& arr) {
    int n = arr.size();
    for (int i = 0; i < n - 1; i++) {
        bool swapped = false;
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                swap(arr[j], arr[j + 1]);
                swapped = true;
            }
        }
        if (!swapped) break;
    }
}
```
