# Modern JavaScript Asynchronous Programming

A reference guide for Promises, async/await syntax, event loop mechanics, and closures in modern JavaScript and TypeScript.

## JavaScript Promises and Promise Chaining

A `Promise` is an object representing the eventual completion (or failure) of an asynchronous operation and its resulting value.

### Syntax and Implementation

```javascript
function fetchUserData(userId) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (userId > 0) {
        resolve({ id: userId, username: "dev_expert", status: "active" });
      } else {
        reject(new Error("Invalid user ID"));
      }
    }, 100);
  });
}

// Chaining with .then() and .catch()
fetchUserData(42)
  .then(user => {
    console.log(`Fetched user: ${user.username}`);
    return user.status;
  })
  .then(status => {
    console.log(`Status confirmed: ${status}`);
  })
  .catch(err => {
    console.error("Error occurred:", err.message);
  });
```

### Example Usage and Output
```
Fetched user: dev_expert
Status confirmed: active
```

### Key Concepts
- States: A Promise is in one of three states: `pending`, `fulfilled`, or `rejected`.
- Error Propagation: Any unhandled rejection in the chain flows down to the nearest `.catch()` block.

---

## JavaScript `async` / `await` Syntax

The `async` and `await` keywords provide syntactic sugar over Promises, allowing asynchronous code to be written and read like synchronous sequential code.

### Syntax and Implementation

```javascript
async function getUserProfile(userId) {
  try {
    const user = await fetchUserData(userId);
    console.log("User details retrieved successfully");
    return user;
  } catch (error) {
    console.error("Failed to load user profile:", error.message);
    throw error;
  } finally {
    console.log("Profile request completed");
  }
}
```

### Example Usage and Output

```javascript
(async () => {
  const profile = await getUserProfile(101);
  console.log("Result:", profile.username);
})();
// Output:
// User details retrieved successfully
// Profile request completed
// Result: dev_expert
```

### Concurrency with `Promise.all`
When multiple independent asynchronous tasks need to be executed in parallel:
```javascript
const [userRes, repoRes] = await Promise.all([
  fetchUserData(1),
  fetchUserRepositories(1)
]);
```

---

## JavaScript Closures

A closure is the combination of a function bundled together with references to its surrounding state (the lexical environment).

### Syntax and Implementation

```javascript
function createCounter(initialValue = 0) {
  let count = initialValue; // Private variable encapsulated in lexical scope
  
  return {
    increment: () => ++count,
    decrement: () => --count,
    getValue: () => count
  };
}

const counter = createCounter(10);
console.log(counter.increment()); // 11
console.log(counter.increment()); // 12
console.log(counter.getValue());  // 12
```

### Space & Memory Characteristics
- Variables captured in closures remain allocated in the heap as long as the referencing inner function exists, preventing garbage collection.
- Used extensively for data encapsulation, function factories, and memoization.
