# JavaScript Fundamentals and Core Programming Guide

A comprehensive, production-grade guide covering modern JavaScript (ES6+) syntax, variables, data structures, functional array methods, object-oriented classes, DOM manipulation, error handling, and algorithms.

## JavaScript Syntax, Variables (`let`, `const`, `var`), and Data Types

JavaScript is a dynamically typed, multi-paradigm language. Modern JavaScript uses `let` for reassignable variables and `const` for immutable bindings. `var` is legacy function-scoped.

### Syntax and Implementation

```javascript
// Variable declarations
const pi = 3.14159;               // Constant number
let userScore = 95;               // Mutable number
const username = "Alex Developer";// String
const isVerified = true;          // Boolean
const notFound = null;            // Intentional absence of value
let unassigned;                   // undefined

// Checking types
console.log(typeof pi);           // "number"
console.log(typeof username);     // "string"
console.log(typeof notFound);     // "object" (historical JS quirk)
console.log(typeof unassigned);   // "undefined"

// String interpolation with template literals
const greeting = `Welcome, ${username}! Your current score is ${userScore}.`;
```

### Key Differences: `let` vs `const` vs `var`
- `const`: Block-scoped, cannot be reassigned (though internal properties of objects/arrays can be mutated).
- `let`: Block-scoped, reassignable.
- `var`: Function-scoped, hoisted with `undefined`, subject to leakage outside `if`/`for` blocks.

---

## JavaScript Conditionals and Equality Operators (`===` vs `==`)

JavaScript provides `if`, `else if`, `else`, `switch`, and ternary operators. Always prefer strict equality `===` over loose equality `==` to avoid automatic type coercion bugs.

### Syntax and Implementation

```javascript
function evaluateStatus(score, isPremium) {
  // Strict equality check: both value and type must match
  if (score === 100 && isPremium) {
    return "Diamond Champion";
  } else if (score >= 80) {
    return "Gold Performer";
  } else if (score >= 50) {
    return "Silver Participant";
  } else {
    return "Needs Improvement";
  }
}

// Ternary operator: condition ? exprIfTrue : exprIfFalse
const membershipTier = isVerified ? "Verified Member" : "Guest";

// Strict vs Loose Equality
console.log(5 === "5"); // false (number !== string)
console.log(5 == "5");  // true (string "5" is coerced to number 5)
```

---

## JavaScript Loops and Iteration (`for`, `for...of`, `for...in`, `while`)

JavaScript supports standard `for` loops, `while`, `do...while`, `for...of` (for iterables like Arrays and Sets), and `for...in` (for object enumerable keys).

### Syntax and Implementation

```javascript
const frameworkList = ["React", "Vue", "Angular", "Svelte"];

// Standard index loop
for (let i = 0; i < frameworkList.length; i++) {
  console.log(`Index ${i}: ${frameworkList[i]}`);
}

// Modern for...of loop (iterates directly over values)
for (const framework of frameworkList) {
  console.log(`Framework: ${framework}`);
}

// While loop
let counter = 0;
let total = 0;
while (counter < 5) {
  total += counter;
  counter++;
}

// for...in loop (iterates over object keys)
const config = { host: "localhost", port: 8080, secure: true };
for (const key in config) {
  console.log(`${key} => ${config[key]}`);
}
```

---

## JavaScript Functions: Declarations, Expressions, and Arrow Functions

Functions in JavaScript are first-class citizens. They can be stored in variables, passed as arguments, and returned from other functions.

### Syntax and Implementation

```javascript
// 1. Function Declaration (hoisted)
function calculateArea(width, height = 1) {
  return width * height;
}

// 2. Arrow Function (ES6, lexical 'this' binding)
const multiply = (a, b) => a * b;

// 3. Multi-line Arrow Function with Rest parameters (...args)
const sumAll = (...numbers) => {
  return numbers.reduce((accum, curr) => accum + curr, 0);
};

// 4. Recursive Factorial implementation
const factorial = (n) => {
  if (n < 0) throw new Error("Factorial undefined for negative numbers.");
  if (n <= 1) return 1;
  return n * factorial(n - 1);
};
```

### Example Usage and Output

```javascript
console.log(calculateArea(5, 4)); // Output: 20
console.log(sumAll(1, 2, 3, 4, 5)); // Output: 15
console.log(factorial(5));          // Output: 120
```

---

## JavaScript Functional Array Methods (`map`, `filter`, `reduce`, `find`)

Arrays in JavaScript feature powerful higher-order methods for declarative, immutable data transformations.

### Syntax and Implementation

```javascript
const products = [
  { id: 1, name: "Laptop", price: 1200, category: "Tech", inStock: true },
  { id: 2, name: "Mouse", price: 25, category: "Tech", inStock: false },
  { id: 3, name: "Desk Chair", price: 250, category: "Furniture", inStock: true },
  { id: 4, name: "Monitor", price: 400, category: "Tech", inStock: true },
];

// 1. filter: Select items matching predicate
const availableTech = products.filter(p => p.category === "Tech" && p.inStock);

// 2. map: Transform each element
const productLabels = products.map(p => `${p.name} ($${p.price})`);

// 3. reduce: Aggregate elements into single value
const totalInventoryValue = products
  .filter(p => p.inStock)
  .reduce((sum, item) => sum + item.price, 0);

// 4. find: Returns first element satisfying condition
const laptop = products.find(p => p.name === "Laptop");

// 5. some and every: Boolean validation
const hasExpensiveItems = products.some(p => p.price > 1000); // true
const allInStock = products.every(p => p.inStock);             // false
```

### Complexity
- `filter`, `map`, `reduce`, `forEach`: $O(N)$ linear time complexity.

---

## JavaScript Objects, Destructuring, and Spread Operator

Objects store key-value mappings. Modern JavaScript includes object destructuring and spread syntax for clean copying and merging.

### Syntax and Implementation

```javascript
const developer = {
  id: 404,
  name: "Jordan",
  skills: ["JavaScript", "TypeScript", "Python"],
  contact: {
    email: "jordan@example.com",
    city: "San Francisco"
  }
};

// Object Destructuring with default values
const { name, skills, contact: { city } } = developer;

// Spread Operator for shallow clone and merging
const updatedDeveloper = {
  ...developer,
  role: "Senior Full Stack Architect",
  skills: [...developer.skills, "Rust"]
};

// Object methods
const keys = Object.keys(developer);     // ['id', 'name', 'skills', 'contact']
const values = Object.values(developer);
const entries = Object.entries(developer);
```

---

## JavaScript String Operations and Algorithms (Reverse, Palindrome)

Strings are primitive values and indexed like character sequences.

### Syntax and Implementation

```javascript
// Reverse a string
function reverseString(str) {
  return str.split("").reverse().join("");
}

// Check if string is a palindrome
function isPalindrome(str) {
  const clean = str.toLowerCase().replace(/[^a-z0-9]/g, "");
  const reversed = clean.split("").reverse().join("");
  return clean === reversed;
}

// Common string methods
const text = "  JavaScript Retrieval Engine  ";
console.log(text.trim());                  // "JavaScript Retrieval Engine"
console.log(text.includes("Retrieval"));   // true
console.log(text.replace("Engine", "AI")); // "  JavaScript Retrieval AI  "
```

### Example Usage and Output

```javascript
console.log(reverseString("Frontend"));      // Output: dnetnorF
console.log(isPalindrome("Race a car"));     // Output: false
console.log(isPalindrome("Was it a car or a cat I saw?")); // Output: true
```

---

## JavaScript Object-Oriented Programming (ES6 Classes, Inheritance)

ES6 introduced class syntax built upon JavaScript's prototypal inheritance model. Classes support constructors, methods, inheritance (`extends`), and `super`.

### Syntax and Implementation

```javascript
class Vehicle {
  constructor(make, model, year) {
    this.make = make;
    this.model = model;
    this.year = year;
    this._speed = 0; // Conventionally private/protected
  }

  accelerate(amount) {
    this._speed += amount;
    return `${this.make} ${this.model} is now moving at ${this._speed} km/h.`;
  }

  getDetails() {
    return `${this.year} ${this.make} ${this.model}`;
  }
}

// Inheritance with extends and super
class ElectricCar extends Vehicle {
  constructor(make, model, year, batteryCapacityKWh) {
    super(make, model, year); // Calls parent constructor
    this.batteryCapacityKWh = batteryCapacityKWh;
    this.chargeLevel = 100;
  }

  charge() {
    this.chargeLevel = 100;
    return `${this.model} is fully charged.`;
  }

  // Method overriding (Polymorphism)
  getDetails() {
    return `${super.getDetails()} [EV - ${this.batteryCapacityKWh} kWh]`;
  }
}
```

### Example Usage and Output

```javascript
const tesla = new ElectricCar("Tesla", "Model 3", 2024, 75);
console.log(tesla.getDetails());        // Output: 2024 Tesla Model 3 [EV - 75 kWh]
console.log(tesla.accelerate(60));       // Output: Tesla Model 3 is now moving at 60 km/h.
```

---

## JavaScript Exception Handling (`try`, `catch`, `finally`, Custom Errors)

Error handling in JavaScript protects applications from crashing on unhandled exceptions.

### Syntax and Implementation

```javascript
class ValidationError extends Error {
  constructor(message) {
    super(message);
    this.name = "ValidationError";
  }
}

function parseUserData(jsonString) {
  try {
    const user = JSON.parse(jsonString);
    if (!user.name || typeof user.name !== "string") {
      throw new ValidationError("User must have a valid string 'name' property.");
    }
    return user;
  } catch (err) {
    if (err instanceof ValidationError) {
      console.error(`Validation Failed: ${err.message}`);
    } else if (err instanceof SyntaxError) {
      console.error(`Malformed JSON input: ${err.message}`);
    } else {
      console.error(`Unexpected Exception: ${err.message}`);
    }
    return null;
  } finally {
    console.log("parseUserData execution completed.");
  }
}
```

---

## JavaScript Essential Algorithms: Binary Search and Bubble Sort

Fundamental algorithms implemented cleanly in JavaScript.

### Syntax and Implementation

```javascript
// Binary Search (Iterative)
function binarySearch(arr, target) {
  let left = 0;
  let right = arr.length - 1;

  while (left <= right) {
    const mid = Math.floor(left + (right - left) / 2);
    if (arr[mid] === target) {
      return mid;
    } else if (arr[mid] < target) {
      left = mid + 1;
    } else {
      right = mid - 1;
    }
  }
  return -1;
}

// Bubble Sort (with early exit)
function bubbleSort(arr) {
  const a = [...arr];
  const n = a.length;
  for (let i = 0; i < n; i++) {
    let swapped = false;
    for (let j = 0; j < n - i - 1; j++) {
      if (a[j] > a[j + 1]) {
        [a[j], a[j + 1]] = [a[j + 1], a[j]]; // Array destructuring swap
        swapped = true;
      }
    }
    if (!swapped) break;
  }
  return a;
}
```

### Example Usage and Output

```javascript
const sorted = [10, 20, 30, 40, 50, 60, 70];
console.log(binarySearch(sorted, 40)); // Output: 3
console.log(binarySearch(sorted, 99)); // Output: -1

const unsorted = [64, 25, 12, 22, 11];
console.log(bubbleSort(unsorted));     // Output: [11, 12, 22, 25, 64]
```
