# Java Fundamentals and Core Programming Guide

A comprehensive, production-grade guide covering Java syntax, primitive and reference types, OOP (encapsulation, inheritance, polymorphism, interfaces), Collections Framework, exception handling, file I/O, and foundational algorithms.

## Java Syntax, Structure, and Primitive Data Types

Java is a statically typed, class-based, object-oriented programming language. All execution begins inside the `public static void main(String[] args)` method of a class.

### Syntax and Implementation

```java
public class JavaBasics {
    public static void main(String[] args) {
        // Primitive Data Types
        byte smallNum = 127;             // 8-bit integer (-128 to 127)
        short shortVal = 32000;          // 16-bit integer
        int count = 100000;              // 32-bit signed integer
        long bigNumber = 9876543210L;    // 64-bit integer (note 'L' suffix)
        float price = 19.99f;            // 32-bit floating point (note 'f')
        double pi = 3.14159265359;       // 64-bit double precision float
        char letter = 'A';               // 16-bit Unicode character
        boolean isActive = true;         // true or false

        // Reference Data Types
        String message = "Hello, Java Developer!";

        // Type Casting
        int castedInt = (int) price;     // Explicit narrowing cast (19)
        double castedDouble = count;     // Implicit widening cast (100000.0)

        System.out.println(message + " Status: " + isActive + ", Casted: " + castedInt);
    }
}
```

### Key Rules
- Class names must match the filename (`JavaBasics.java`).
- Primitive types are passed by value; object references are also passed by value (reference copy).

---

## Java Control Flow and Conditional Statements (`if-else` and `switch`)

Java supports standard conditional branching via `if-else` and `switch` statements with pattern matching or constant expressions.

### Syntax and Implementation

```java
public class ControlFlowDemo {
    public static String getDayType(int dayOfWeek) {
        // Switch statement (enhanced modern Java syntax)
        return switch (dayOfWeek) {
            case 1, 7 -> "Weekend";
            case 2, 3, 4, 5, 6 -> "Weekday";
            default -> "Invalid Day";
        };
    }

    public static String evaluateGrade(int marks) {
        if (marks >= 90) {
            return "Grade A";
        } else if (marks >= 80) {
            return "Grade B";
        } else if (marks >= 60) {
            return "Grade C";
        } else {
            return "Grade F";
        }
    }
}
```

---

## Java Loops and Iteration (`for`, enhanced `for-each`, `while`)

Java provides traditional indexed `for` loops, enhanced `for-each` loops for arrays and Collections, `while`, and `do-while`.

### Syntax and Implementation

```java
public class LoopsDemo {
    public static void main(String[] args) {
        int[] numbers = {10, 20, 30, 40, 50};

        // 1. Traditional indexed for loop
        int sum = 0;
        for (int i = 0; i < numbers.length; i++) {
            sum += numbers[i];
        }

        // 2. Enhanced for-each loop
        for (int num : numbers) {
            System.out.println("Item: " + num);
        }

        // 3. While loop with break / continue
        int counter = 0;
        while (counter < 10) {
            counter++;
            if (counter == 5) continue; // skip 5
            if (counter == 8) break;    // exit at 8
        }
    }
}
```

---

## Java Methods and Method Overloading

Methods in Java define reusable subroutines. Java supports method overloading (multiple methods with the same name but different parameter signatures).

### Syntax and Implementation

```java
public class MathOperations {
    // Overloaded method 1: 2 integers
    public static int add(int a, int b) {
        return a + b;
    }

    // Overloaded method 2: 3 integers
    public static int add(int a, int b, int c) {
        return a + b + c;
    }

    // Overloaded method 3: 2 doubles
    public static double add(double a, double b) {
        return a + b;
    }

    // Recursive Factorial
    public static long factorial(int n) {
        if (n < 0) throw new IllegalArgumentException("Negative input not allowed.");
        if (n <= 1) return 1;
        return n * factorial(n - 1);
    }
}
```

### Example Usage and Output

```java
System.out.println(MathOperations.add(10, 20));       // 30
System.out.println(MathOperations.add(5.5, 4.5));     // 10.0
System.out.println(MathOperations.factorial(5));      // 120
```

---

## Java String Manipulation (`String`, `StringBuilder`, Palindrome)

In Java, `String` objects are immutable. For frequent concatenation or mutations, `StringBuilder` must be used to avoid creating excess garbage collection overhead.

### Syntax and Implementation

```java
public class StringOperations {
    // Reverse a string using StringBuilder
    public static String reverseString(String input) {
        if (input == null) return "";
        return new StringBuilder(input).reverse().toString();
    }

    // Palindrome check ignoring case and non-alphanumeric characters
    public static boolean isPalindrome(String s) {
        if (s == null) return false;
        int left = 0;
        int right = s.length() - 1;

        while (left < right) {
            while (left < right && !Character.isLetterOrDigit(s.charAt(left))) left++;
            while (left < right && !Character.isLetterOrDigit(s.charAt(right))) right--;

            if (Character.toLowerCase(s.charAt(left)) != Character.toLowerCase(s.charAt(right))) {
                return false;
            }
            left++;
            right--;
        }
        return true;
    }
}
```

### Example Usage and Output

```java
System.out.println(StringOperations.reverseString("Developer")); // repoleveD
System.out.println(StringOperations.isPalindrome("Radar"));       // true
```

---

## Java Object-Oriented Programming (OOP: Encapsulation, Inheritance, Polymorphism)

Java is an object-oriented language featuring encapsulation, inheritance via `extends`, and runtime polymorphism via method overriding (`@Override`).

### Syntax and Implementation

```java
// Base class demonstrating encapsulation
class BankAccount {
    private String accountNumber;
    protected double balance; // Accessible to derived classes

    public BankAccount(String accountNumber, double initialBalance) {
        this.accountNumber = accountNumber;
        this.balance = initialBalance;
    }

    public double getBalance() {
        return balance;
    }

    public void deposit(double amount) {
        if (amount > 0) balance += amount;
    }

    // Virtual method subject to runtime polymorphism
    public void printAccountDetails() {
        System.out.println("Account: " + accountNumber + " | Balance: $" + balance);
    }
}

// Derived class demonstrating Inheritance and Method Overriding
class SavingsAccount extends BankAccount {
    private double interestRate;

    public SavingsAccount(String accountNumber, double balance, double interestRate) {
        super(accountNumber, balance); // Calls parent constructor
        this.interestRate = interestRate;
    }

    public void applyInterest() {
        balance += (balance * interestRate / 100);
    }

    @Override
    public void printAccountDetails() {
        super.printAccountDetails();
        System.out.println("Account Type: Savings | Interest Rate: " + interestRate + "%");
    }
}
```

### Polymorphism Demonstration
```java
BankAccount acc = new SavingsAccount("SA-901", 1000.0, 5.0);
acc.printAccountDetails(); // Dynamic dispatch invokes SavingsAccount's method
```

---

## Java Abstraction and Interfaces

An `interface` specifies a contract that implementing classes must satisfy. Java allows multiple interface implementation.

### Syntax and Implementation

```java
// Interface definition
interface Playable {
    void play();
    void pause();
    void stop();
}

interface Recordable {
    void record();
}

// Concrete class implementing multiple interfaces
class AudioPlayer implements Playable, Recordable {
    private String track;

    public AudioPlayer(String track) {
        this.track = track;
    }

    @Override
    public void play() {
        System.out.println("Playing audio track: " + track);
    }

    @Override
    public void pause() {
        System.out.println("Paused audio track: " + track);
    }

    @Override
    public void stop() {
        System.out.println("Stopped audio playback.");
    }

    @Override
    public void record() {
        System.out.println("Recording new audio stream...");
    }
}
```

---

## Java Collections Framework (`ArrayList`, `HashMap`, `HashSet`)

The Java Collections Framework provides core generic data structures under `java.util`.

### Syntax and Implementation

```java
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;

public class CollectionsDemo {
    public static void main(String[] args) {
        // 1. ArrayList (Dynamic Array, O(1) indexed access, O(1) amortized append)
        ArrayList<String> list = new ArrayList<>();
        list.add("Java");
        list.add("Python");
        list.add("C++");
        list.remove("Python");
        System.out.println("First element: " + list.get(0)); // "Java"

        // 2. HashMap (Key-Value hash table, O(1) average lookup/put)
        HashMap<String, Integer> scores = new HashMap<>();
        scores.put("Alice", 95);
        scores.put("Bob", 88);
        int aliceScore = scores.getOrDefault("Alice", 0);

        for (Map.Entry<String, Integer> entry : scores.entrySet()) {
            System.out.println(entry.getKey() + " -> " + entry.getValue());
        }

        // 3. HashSet (Unique elements, O(1) average contains)
        HashSet<Integer> uniqueNums = new HashSet<>();
        uniqueNums.add(10);
        uniqueNums.add(20);
        uniqueNums.add(10); // Duplicate ignored
        System.out.println("Set size: " + uniqueNums.size()); // 2
    }
}
```

---

## Java Exception Handling (`try`, `catch`, `finally`, `throw`, Custom Exceptions)

Java distinguishes between checked exceptions (enforced at compile time) and unchecked runtime exceptions (`RuntimeException`).

### Syntax and Implementation

```java
// Custom checked exception
class InsufficientBalanceException extends Exception {
    public InsufficientBalanceException(String message) {
        super(message);
    }
}

public class ExceptionDemo {
    public static void withdraw(double balance, double amount) throws InsufficientBalanceException {
        if (amount > balance) {
            throw new InsufficientBalanceException("Withdrawal of $" + amount + " exceeds balance $" + balance);
        }
        System.out.println("Withdrawal successful! Remaining: $" + (balance - amount));
    }

    public static void main(String[] args) {
        try {
            withdraw(100.0, 150.0);
        } catch (InsufficientBalanceException e) {
            System.err.println("Transaction Error: " + e.getMessage());
        } finally {
            System.out.println("Banking operation finalized.");
        }
    }
}
```

---

## Java Essential Algorithms: Binary Search and Bubble Sort

Standard search and sort implementations in Java.

### Syntax and Implementation

```java
public class AlgorithmDemo {
    // Binary Search: returns index if found, or -1
    public static int binarySearch(int[] arr, int target) {
        int left = 0;
        int right = arr.length - 1;

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

    // Bubble Sort with early termination
    public static void bubbleSort(int[] arr) {
        int n = arr.length;
        for (int i = 0; i < n - 1; i++) {
            boolean swapped = false;
            for (int j = 0; j < n - i - 1; j++) {
                if (arr[j] > arr[j + 1]) {
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                    swapped = true;
                }
            }
            if (!swapped) break;
        }
    }
}
```

### Complexity Analysis
- **Binary Search**: $O(\log N)$ time, $O(1)$ space.
- **Bubble Sort**: $O(N^2)$ time, $O(1)$ space.
