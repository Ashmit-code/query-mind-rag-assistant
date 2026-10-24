# Python Data Structures and Algorithms Guide

Comprehensive implementations of foundational DSA in Python with explicit time and space complexity annotations.

## Binary Search in Python

Binary Search finds the position of a target value within a sorted array. It repeatedly divides the search interval in half.

### Syntax and Implementation

```python
def binary_search(arr: list[int], target: int) -> int:
    """
    Perform iterative binary search on a sorted list.
    Returns the index of target if found, otherwise -1.
    """
    left = 0
    right = len(arr) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
            
    return -1
```

### Example Usage and Output

```python
numbers = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
target = 23
result = binary_search(numbers, target)
print(f"Index of {target}: {result}")
# Output: Index of 23: 5
```

### Complexity Analysis
- **Time Complexity**: $O(\log N)$ in both average and worst cases because the search space is halved at each iteration. $O(1)$ best case when the middle element is the target.
- **Space Complexity**: $O(1)$ auxiliary space for iterative approach; $O(\log N)$ call stack space for recursive approach.

---

## Merge Sort in Python

Merge Sort is a classic Divide and Conquer algorithm that divides an input array into two halves, recursively sorts each half, and merges the two sorted halves.

### Syntax and Implementation

```python
def merge_sort(arr: list[int]) -> list[int]:
    """
    Sorts a list of integers using the Merge Sort algorithm.
    Returns a new sorted list.
    """
    if len(arr) <= 1:
        return arr
        
    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])
    
    return merge(left_half, right_half)

def merge(left: list[int], right: list[int]) -> list[int]:
    merged = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
            
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged
```

### Example Usage and Output

```python
data = [38, 27, 43, 3, 9, 82, 10]
sorted_data = merge_sort(data)
print(f"Sorted array: {sorted_data}")
# Output: Sorted array: [3, 9, 10, 27, 38, 43, 82]
```

### Complexity Analysis
- **Time Complexity**: $O(N \log N)$ in all cases (best, average, and worst) because the array is always split in half ($\log N$ levels) and merging takes linear time $O(N)$ at each level.
- **Space Complexity**: $O(N)$ auxiliary space required to hold the temporary sublists during merging.
- **Stability**: Merge Sort is stable; equal elements preserve their relative initial order.

---

## Dijkstra's Shortest Path Algorithm

Dijkstra's algorithm finds the shortest path from a single source vertex to all other vertices in a weighted graph with non-negative edge weights.

### Syntax and Implementation

```python
import heapq

def dijkstra(graph: dict[str, list[tuple[str, int]]], start: str) -> dict[str, float]:
    """
    Computes shortest distances from start vertex using a min-heap priority queue.
    Graph representation: { 'A': [('B', 4), ('C', 2)], ... }
    """
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    pq = [(0, start)]  # (distance, node)
    
    while pq:
        current_dist, current_node = heapq.heappop(pq)
        
        if current_dist > distances[current_node]:
            continue
            
        for neighbor, weight in graph.get(current_node, []):
            distance = current_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
                
    return distances
```

### Example Usage and Output

```python
graph = {
    'A': [('B', 4), ('C', 2)],
    'B': [('A', 4), ('C', 1), ('D', 5)],
    'C': [('A', 2), ('B', 1), ('D', 8), ('E', 10)],
    'D': [('B', 5), ('C', 8), ('E', 2)],
    'E': [('C', 10), ('D', 2)]
}
distances = dijkstra(graph, 'A')
print(distances)
# Output: {'A': 0, 'B': 3, 'C': 2, 'D': 8, 'E': 10}
```

### Complexity Analysis
- **Time Complexity**: $O((V + E) \log V)$ where $V$ is vertices and $E$ is edges, using a binary min-heap (`heapq`). Each vertex is extracted once ($O(V \log V)$) and each edge is relaxed at most once ($O(E \log V)$).
- **Space Complexity**: $O(V)$ for the distance dictionary and priority queue.
