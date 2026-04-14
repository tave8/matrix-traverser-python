Matrix Traverser is a configurable, extensible, DFS-based matrix traversal engine (DFS = depth-first search).




# Examples

From the most straightforward problems, to the more complex.

## Diagonal

![Diagonal](/assets/diagrams/diagonal.png)

## T shape

![T shape](/assets/diagrams/t_shape.png)

## Snake

![Snake](/assets/diagrams/snake.png)

## Spiral

![Spiral](/assets/diagrams/spiral.png)

## Zigzag

![Zigzag](/assets/diagrams/zigzag.png)

## Geometry 1

![Geometry 1](/assets/diagrams/geometry_1.png)

## Next = prev + 1

![Next = prev + 1](/assets/diagrams/next_equals_prev_plus_1.png)

# Configuration & Setup

To tell Python to include the import path as the root directory, I've done the following:

1. Go in the `site-packages` directory, inside the `.venv` directory

2. Create a file with any name, as long as the extension is `.pth`

3. Add the absolute path that points to your root directory, for example

```
c:/Users/giuse/Desktop/projects/matrix-traverser-python
```

4. Now, when you run a script from any place inside the root directory, Python will also know how to scan
   for modules starting from this root directory

5. You can check that the root directory is included in the Python import paths, by running

```py
import sys
for p in sys.path:
    print(p)
```


## Mark root directory as sources root 

You must make sure that your IDE does not imports the same module from different paths.

A strategy to prevent this, is to fully qualify your imports. 

For example, I had a bug where:

```python
from components import Move
```

was different from 

```python
from src.components import Move
```

So the correct one is the latter (fully qualified import).


# Object hierarchy

![Object hierarchy](/assets/object_hierarchy.png)

# Terminology

## Engine

When we refer to Engine, we refer to the Matrix Traverser Engine. 

It is the underlying, configurable algorithm that traverses a matrix.

The Engine can be used as the basis for more specific algorithms.

For example, the Maze Traverser uses the Engine to pilot cells and find whether a path in a labyrinth exists.

The Maze Traverser therefore abstracts the Engine, however we might still want to make life easier for the user,

by providing another abstraction: The Implementation.


## Implementation

You may think of an Implementation as "the actual problem solved", it is therefore very problem-specific.

An Implementation is the end outcome of one of the algorithms. 

It is supposed to provide a user-friendly and intuitive interface, and zero boilerplate, to solve a specific problem: Only the actual input that the problem requires. 

For example, for a maze-based Implementation, we may want to provide at the very least the start of the maze. 

For example, an Implementation is the "Incremental Path", which finds whether a path of incremental values exists (S -> 1 -> 2 -> 3 -> 4 -> ... -> E).

An Implementation, as the name suggests, implements, and more specifically it implements an algorithm.

For example, the Incremental Path implements the Maze Traverser, which in turn implements Matrix Traverser.

The higher up we go in the "implementation chain", the more abstract the logic.

The further down we go, the more user-friendly.


# Algorithm

## The start

When we first call the algorithm to traverse matrix with `traverseMatrix`, we must note a few things:

- The currCoordinate is the start coordinate, which is the actual user-provided start coordinate

- The prevCoordinate is the "before to start" coordinate which, on the other hand, is a dummy coordinate
  whose sole purpose is to comply with the method `traverseMatrix` which requires both currCoordinate
  and prevCoordinate

- This means that, at the very start, trying to access or comparing prevCoordinate, will and should
  result in error, because as we said, prevCoordinate at the very start is a dummy coordinate.
  This edge case is left to the implementation of the user-defined callbacks to handle,
  for example by specifying, as the very first lines of code of the user-defined callback,
  the logic that should apply only to the currCoordinate of the start, which is precisely
  the start coordinate. Example below.

```py

def beforeFirstVisitCallback(mt: MatrixTraverser,
                             prevCoordinate: Coordinate,
                             currCoordinate: Coordinate):
    # print only current coordinate, which is the start coordinate
    if currCoordinate.isStart:
        print(f"{mt.getAtCoordinate(currCoordinate)}")
    # print value of the previous coordinate --> value of the current coordinate
    else:
        print(f"{mt.getAtCoordinate(prevCoordinate)} --> {mt.getAtCoordinate(currCoordinate)}")

```

```py

def canMoveCallback(mt: MatrixTraverser,
                    desiredCoordinate: Coordinate,
                    prevCoordinate: Coordinate,
                    currCoordinate: Coordinate):

    # from the start, you can only move to
    # a cell with value 1
    if currCoordinate.isStart:
        return mt.getAtCoordinate(desiredCoordinate) == "1"

```

- Note that, at the very start, saying currCoordinate.isStart is logically equivalent to
  prevCoordinate.isBeforeStart. I didn't say they are the same things; I only said that they should
  be logically equivalent operations.

- About this dummy "before to start" coordinate: It's a real Coordinate instance (not something like None)

# Callbacks

## canMove

## beforeFirstVisit

## getNextMoves

# Entity design

```
MatrixTraverser
    matrix
    visited
    stateManager
    callbackManager
    traverseMatrix(): public
    traverse(): private
    findOne(): public
    getAtCoordinate(): public
    isVisited(): private
    markAsVisited(): private
    isInsideMatrix(): public
    generateVisitedMatrix(): public, static
    generate0Matrix(): public, static

CallbackManager
    callbackMap
    matrixTraverser
    canMove():
    beforeFirstVisit():
    getNextMoves():
    canVisit():
    onMultipleVisitMustStop():
    canEnd():
    onEnd():
    dictHasFunction(): public, static

StateManager
    userState
    state
    stats
    matrixTraverser
    startCoordinate
    beforeStartCoordinate

Moves
    getDefaultMoves(): public, static
    getAllMoves(): public, static

Coordinate
    row
    col
    isStart
    isBeforeStart
    up()
    down()
    left()
    right()
    diagonalUpRight()
    diagonalDownRight()
    diagonalUpLeft()
    diagonalDownLeft()
    clone()

Move
    _BEFORE_START
    UP
    DIAGONAL_UP_RIGHT
    RIGHT
    DIAGONAL_DOWN_RIGHT
    DOWN
    DIAGONAL_DOWN_LEFT
    LEFT
    DIAGONAL_UP_LEFT

```
