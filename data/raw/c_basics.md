# C Fundamentals and Core Programming Guide

A comprehensive, production-grade guide covering procedural C programming, data types, format specifiers, pointers, manual memory allocation (`malloc`/`free`), structs, file I/O, linked lists, and fundamental algorithms.

## C Program Structure, Format Specifiers, and Data Types

C is a foundational, statically typed, procedural compiled language that provides direct memory access.

### Syntax and Implementation

```c
#include <stdio.h>
#include <stdbool.h>

int main(void) {
    // Primitive Data Types
    int age = 22;                     // 32-bit signed integer (%d)
    long long bigVal = 9876543210LL;  // 64-bit integer (%lld)
    float price = 19.95f;             // 32-bit single precision float (%f)
    double pi = 3.14159265;           // 64-bit double precision float (%lf)
    char grade = 'A';                 // 8-bit character (%c)
    bool isStudent = true;            // Boolean from <stdbool.h>

    // Formatted output with printf
    printf("Age: %d, Grade: %c, Price: $%.2f, Pi: %.4lf\n", age, grade, price, pi);
    printf("Memory size of double: %zu bytes\n", sizeof(double));

    return 0; // 0 indicates successful execution to the operating system
}
```

### Essential Format Specifiers
- `%d` / `%i`: signed integer
- `%u`: unsigned integer
- `%f`: float
- `%lf`: double
- `%c`: character
- `%s`: null-terminated string
- `%p`: pointer address in hexadecimal
- `%zu`: `size_t` from `sizeof`

---

## C Input and Output (`printf`, `scanf`, `fgets`)

Standard input functions require passing memory addresses to store user values. Always bound buffer reads using `fgets` to prevent buffer overflow vulnerabilities.

### Syntax and Implementation

```c
#include <stdio.h>
#include <string.h>

void readUserInput(void) {
    int id;
    char fullName[50];

    printf("Enter User ID: ");
    if (scanf("%d", &id) != 1) {
        printf("Invalid numeric input!\n");
        return;
    }

    // Flush remaining newline character from stdin buffer
    while (getchar() != '\n');

    printf("Enter Full Name: ");
    if (fgets(fullName, sizeof(fullName), stdin) != NULL) {
        // Strip trailing newline character
        fullName[strcspn(fullName, "\n")] = '\0';
    }

    printf("Recorded: ID=%d, Name='%s'\n", id, fullName);
}
```

---

## C Functions, Parameter Passing, and Recursion

Functions in C are passed by value by default. To modify caller variables, pointers must be passed explicitly.

### Syntax and Implementation

```c
#include <stdio.h>

// Pass by pointer allows modifying variables in the caller's stack frame
void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

// Recursive factorial function
long long factorial(int n) {
    if (n < 0) return -1; // Error condition
    if (n <= 1) return 1; // Base case
    return n * factorial(n - 1); // Recursive case
}

int main(void) {
    int x = 10, y = 20;
    swap(&x, &y);
    printf("Swapped: x=%d, y=%d\n", x, y); // x=20, y=10
    printf("5! = %lld\n", factorial(5));   // 120
    return 0;
}
```

---

## C Pointers and Pointer Arithmetic

A pointer is a variable that stores the memory address of another variable. The address-of operator `&` extracts an address; the dereference operator `*` accesses the value at that address.

### Syntax and Implementation

```c
#include <stdio.h>

int main(void) {
    int value = 50;
    int *ptr = &value; // Pointer holds address of value

    printf("Value: %d\n", value);
    printf("Address (&value): %p\n", (void*)&value);
    printf("Pointer value (ptr): %p\n", (void*)ptr);
    printf("Dereferenced (*ptr): %d\n", *ptr);

    // Modify original variable through pointer
    *ptr = 100;
    printf("Updated value: %d\n", value); // 100

    // Pointer arithmetic on arrays
    int numbers[] = {10, 20, 30, 40, 50};
    int *arrPtr = numbers; // points to numbers[0]

    for (int i = 0; i < 5; i++) {
        // *(arrPtr + i) is mathematically identical to numbers[i]
        printf("Index %d: value = %d (address = %p)\n", i, *(arrPtr + i), (void*)(arrPtr + i));
    }

    return 0;
}
```

---

## C Dynamic Memory Allocation (`malloc`, `calloc`, `realloc`, `free`)

Dynamic memory is requested at runtime from the Heap using `<stdlib.h>`. Unfreed heap memory causes memory leaks.

### Syntax and Implementation

```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int size = 5;

    // 1. malloc: Allocates uninitialized memory of given byte size
    int *arr = (int *)malloc(size * sizeof(int));
    if (arr == NULL) {
        fprintf(stderr, "Heap memory allocation failed!\n");
        return 1;
    }

    for (int i = 0; i < size; i++) {
        arr[i] = (i + 1) * 10;
    }

    // 2. realloc: Resizes previously allocated block
    int newSize = 8;
    int *temp = (int *)realloc(arr, newSize * sizeof(int));
    if (temp == NULL) {
        free(arr); // Free original block if reallocation fails
        return 1;
    }
    arr = temp;

    // Initialize newly added slots
    for (int i = size; i < newSize; i++) {
        arr[i] = (i + 1) * 10;
    }

    // 3. free: Release memory back to OS
    free(arr);
    arr = NULL; // Prevent dangling pointer usage

    return 0;
}
```

### Critical Rules
- Always verify if allocation returned `NULL` before using the pointer.
- Every `malloc` / `calloc` / `realloc` call MUST have a corresponding `free()`.

---

## C Strings and `<string.h>` Library Functions

Strings in C are one-dimensional character arrays terminated by a null character `'\0'`.

### Syntax and Implementation

```c
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>

// Reverse string in-place
void reverseString(char *str) {
    int i = 0;
    int j = strlen(str) - 1;
    while (i < j) {
        char temp = str[i];
        str[i] = str[j];
        str[j] = temp;
        i++;
        j--;
    }
}

// Palindrome check
bool isPalindrome(const char *str) {
    int i = 0;
    int j = strlen(str) - 1;
    while (i < j) {
        if (tolower(str[i]) != tolower(str[j])) {
            return false;
        }
        i++;
        j--;
    }
    return true;
}

int main(void) {
    char greeting[30] = "Hello";
    strcat(greeting, ", World!");     // Concatenation: "Hello, World!"
    printf("Length: %zu\n", strlen(greeting)); // 13

    char word[] = "level";
    printf("Is 'level' palindrome: %s\n", isPalindrome(word) ? "true" : "false");

    reverseString(greeting);
    printf("Reversed: %s\n", greeting); // "!dlroW ,olleH"
    return 0;
}
```

---

## C Structures (`struct`) and `typedef`

Structures allow grouping heterogeneous data types into a single user-defined record type.

### Syntax and Implementation

```c
#include <stdio.h>
#include <string.h>

// Define a struct using typedef for clean naming
typedef struct {
    int id;
    char name[50];
    float gpa;
} Student;

// Function accepting struct pointer (arrow operator ->)
void printStudent(const Student *s) {
    printf("Student [ID: %d, Name: %s, GPA: %.2f]\n", s->id, s->name, s->gpa);
}

int main(void) {
    Student s1;
    s1.id = 101;
    strncpy(s1.name, "Alice Smith", sizeof(s1.name) - 1);
    s1.gpa = 3.85f;

    printStudent(&s1);
    return 0;
}
```

---

## C File Handling (`fopen`, `fprintf`, `fscanf`, `fclose`)

File operations in C utilize the `FILE` pointer defined in `<stdio.h>`.

### Syntax and Implementation

```c
#include <stdio.h>

// Write data to a text file
int writeLogFile(const char *filename, const char *message) {
    FILE *file = fopen(filename, "w"); // "w" = write mode (overwrites)
    if (file == NULL) {
        perror("Failed to open file for writing");
        return -1;
    }
    fprintf(file, "LOG ENTRY: %s\n", message);
    fclose(file); // Flush and close file handle
    return 0;
}

// Read line-by-line from a text file
int readLogFile(const char *filename) {
    FILE *file = fopen(filename, "r"); // "r" = read mode
    if (file == NULL) {
        perror("Failed to open file for reading");
        return -1;
    }

    char buffer[256];
    while (fgets(buffer, sizeof(buffer), file) != NULL) {
        printf("%s", buffer);
    }

    fclose(file);
    return 0;
}
```

---

## C Singly Linked List Implementation

A linked list is a linear dynamic data structure composed of nodes where each node contains data and a pointer to the next node.

### Syntax and Implementation

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int data;
    struct Node *next;
} Node;

// Insert a new node at the beginning of the list: O(1)
void insertAtHead(Node **headRef, int value) {
    Node *newNode = (Node *)malloc(sizeof(Node));
    if (newNode == NULL) return;
    newNode->data = value;
    newNode->next = *headRef;
    *headRef = newNode;
}

// Print all elements of the linked list
void printList(const Node *head) {
    const Node *curr = head;
    while (curr != NULL) {
        printf("%d -> ", curr->data);
        curr = curr->next;
    }
    printf("NULL\n");
}

// Free all allocated nodes
void freeList(Node *head) {
    Node *curr = head;
    while (curr != NULL) {
        Node *temp = curr;
        curr = curr->next;
        free(temp);
    }
}

int main(void) {
    Node *head = NULL;
    insertAtHead(&head, 30);
    insertAtHead(&head, 20);
    insertAtHead(&head, 10);

    printList(head); // 10 -> 20 -> 30 -> NULL
    freeList(head);
    return 0;
}
```

---

## C Essential Algorithms: Binary Search and Bubble Sort

Fundamental search and sort implementations in C.

### Syntax and Implementation

```c
#include <stdio.h>

// Binary Search in C: O(log N)
int binarySearch(const int arr[], int size, int target) {
    int left = 0;
    int right = size - 1;

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
    return -1; // Element not found
}

// Bubble Sort in C: O(N^2)
void bubbleSort(int arr[], int size) {
    for (int i = 0; i < size - 1; i++) {
        int swapped = 0;
        for (int j = 0; j < size - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
                swapped = 1;
            }
        }
        if (!swapped) break; // Array is sorted
    }
}
```

### Complexity Analysis
- **Binary Search**: $O(\log N)$ time, $O(1)$ space on sorted array.
- **Bubble Sort**: $O(N^2)$ worst/average time, $O(N)$ best case, $O(1)$ space.
