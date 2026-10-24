# Algorithms and Asymptotic Complexity Reference

This reference documents the time and space complexity of fundamental computer science algorithms and data structures.

## Big-O Notation and Growth Rates

Big-O notation describes the upper bound on the time or space complexity of an algorithm as a function of the input size $N$.

- **$O(1)$ Constant Time**: The runtime does not depend on the input size. Example: accessing an array element by index, hash table lookup (average case).
- **$O(\log N)$ Logarithmic Time**: The problem size is divided by a constant factor in each step. Example: Binary Search on a sorted list.
- **$O(N)$ Linear Time**: The runtime scales directly proportional to input size. Example: Linear scan of an array or linked list.
- **$O(N \log N)$ Linearithmic Time**: Common in optimal comparison-based sorting algorithms. Example: Merge Sort, Heapsort, average-case Quicksort.
- **$O(N^2)$ Quadratic Time**: Nested iterations over the input. Example: Bubble Sort, Selection Sort, Insertion Sort.
- **$O(2^N)$ Exponential Time**: The operations double with each additional input element. Example: Naive recursive calculation of Fibonacci numbers.

## Sorting Algorithms Complexity Summary

| Algorithm | Best Time | Average Time | Worst Time | Worst Space | Stable? |
|---|---|---|---|---|---|
| Merge Sort | $O(N \log N)$ | $O(N \log N)$ | $O(N \log N)$ | $O(N)$ | Yes |
| Quick Sort | $O(N \log N)$ | $O(N \log N)$ | $O(N^2)$ | $O(\log N)$ aux | No |
| Heap Sort | $O(N \log N)$ | $O(N \log N)$ | $O(N \log N)$ | $O(1)$ | No |
| Insertion Sort | $O(N)$ | $O(N^2)$ | $O(N^2)$ | $O(1)$ | Yes |
| Bubble Sort | $O(N)$ | $O(N^2)$ | $O(N^2)$ | $O(1)$ | Yes |
| TimSort (Python `sort()`) | $O(N)$ | $O(N \log N)$ | $O(N \log N)$ | $O(N)$ | Yes |

## Graph Traversal and Shortest Path Complexity

### Breadth-First Search (BFS)
- **Data Structure**: Queue (FIFO).
- **Time Complexity**: $O(V + E)$ where $V$ is number of vertices and $E$ is number of edges.
- **Space Complexity**: $O(V)$ for the visited set and queue.
- **Applications**: Shortest path on unweighted graphs, connected components.

### Depth-First Search (DFS)
- **Data Structure**: Stack (LIFO) or system call stack (recursion).
- **Time Complexity**: $O(V + E)$.
- **Space Complexity**: $O(V)$ in the worst case for deep linear graphs.
- **Applications**: Cycle detection, topological sorting, connected components.

### Dijkstra's Shortest Path Algorithm
- **Data Structure**: Min-Heap / Priority Queue.
- **Time Complexity**: $O((V + E) \log V)$ using a binary min-heap; $O(E + V \log V)$ with a Fibonacci heap.
- **Space Complexity**: $O(V)$ for distances and priority queue.
- **Constraint**: Only works for graphs with non-negative edge weights.
