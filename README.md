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


# Problem diagrams

## Traverse diagonal 

![alt text](image.png)


## Zigzag traverse

## Snake traverse




[sds](/assets/example_problems.png)