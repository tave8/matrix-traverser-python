# Heat Propagation Labyrinth

## Problem

You are given a 2D matrix of integers representing a grid of rooms, each with a temperature value. One cell is marked `"S"` (start) and one cell is marked `"E"` (end).

A traveler begins at `S` and must reach `E` by moving one cell at a time to any of the 8 adjacent cells (horizontal, vertical, or diagonal).

The traveler has a **temperature tolerance** — the maximum temperature difference they can handle in a single move. If the traveler is in a room with temperature `10` and their tolerance is `3`, they can only move to rooms with temperatures between `7` and `13` inclusive.

The tolerance starts at an initial value and **decreases by 1 every K steps**.

- The first move from `S` is always free — temperature of `S` is undefined.
- The last move to `E` is always free — temperature of `E` is undefined.

---

## Task

Write a function that returns the path from `S` to `E` if one exists, or an empty array if no valid path exists.

---

## Input

| Parameter | Type | Description |
|---|---|---|
| `matrix` | `list[list]` | A 2D array of integers, `"S"`, and `"E"` |
| `startTolerance` | `int` | The initial tolerance value |
| `shrinkEvery` | `int` | Tolerance shrinks by 1 every this many steps |

## Output

A list of cell values along the valid path from `S` to `E` inclusive,
or an empty list if no valid path exists.

---

## Examples

### Example 1 — Valid Path Exists

**Input**

```python
matrix = [
    ["S",  12,   8,   3,   2],
    [ 11,  10,   7,   4,   3],
    [  9,   8,   7,   5,   4],
    [  7,   6,   6,   5,   5],
    [  5,   4,   5,   5,  "E"]
]
startTolerance = 4
shrinkEvery = 3
```

**Output**

```python
["S", 11, 9, 8, 7, 6, 6, 5, 5, "E"]
```

---

### Example 2 — No Valid Path

**Input**

```python
matrix = [
    ["S",  12,   8],
    [ 11,  10,   7],
    [  1,   1,  "E"]
]
startTolerance = 2
shrinkEvery = 2
```

**Output**

```python
[]
```

---

## Constraints

- The matrix is at least `2x2`
- Exactly one `"S"` and one `"E"` exist in the matrix
- All non-`S`, non-`E` values are positive integers
- `startTolerance >= 1`
- `shrinkEvery >= 1`
- Tolerance never goes below `1`
- The traveler cannot revisit a cell

---

## Notes

- A shorter path is not necessarily a valid path — a longer path with gradual temperature changes may succeed where a shorter path with large jumps fails.
- The same cell may be reachable or unreachable depending on how many steps have been taken when the traveler arrives there.
- This is not solvable with standard BFS or Dijkstra — the validity of each move depends on when during the traversal it is taken, not just which cells are involved.