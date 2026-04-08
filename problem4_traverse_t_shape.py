"""
PROBLEM: Traverse the matrix in T shape, 
so first row and the column in the middle.
"""

from MatrixTraverser import MatrixTraverser, MatrixTraverserCallbackManager, MatrixTraverserStateManager, Coordinate, Move


matrix = [
    [1,   6,   11,  16,  21],
    [2,   7,   12,  17,  22],
    [3,   8,   13,  18,  23],
    [4,   9,   14,  19,  24],
    [5,   10,  15,  20,  25]
]

state = {}


def beforeFirstVisitCallback(mt: MatrixTraverser, prevCoordinate: Coordinate, currCoordinate: Coordinate):
    if currCoordinate.isStart:
        print(f"{mt.getAtCoordinate(currCoordinate)}")
    else:
        print(f"{mt.getAtCoordinate(prevCoordinate)} --> {mt.getAtCoordinate(currCoordinate)}")
    


def getNextMovesCallback(mt: MatrixTraverser, prevCoordinate: Coordinate, currCoordinate: Coordinate):
    # if this is the cell right 
    # at the intersection in the T shape
    # this cell must move first right, and then down
    if currCoordinate.getRow() == 0 and currCoordinate.getCol() == 2:
        return [
            Move.RIGHT,
            Move.DOWN
        ]
    
    # if this is the cell in a column in the middle,
    # it can only move down
    if currCoordinate.getCol() == 2:
        return [
            Move.DOWN
        ]

    # if this is the first row, you can only move right
    if currCoordinate.getRow() == 0:
        return [
            Move.RIGHT
        ]
    
    # for any other cell, you cannot move anywhere else
    return []


def canMoveCallback(mt: MatrixTraverser, desiredCoordinate: Coordinate, prevCoordinate: Coordinate, currCoordinate: Coordinate):
    pass    


callbackMap = {
    "canMove": canMoveCallback,
    "getNextMoves": getNextMovesCallback,
    "beforeFirstVisit": beforeFirstVisitCallback,
}


stateManager = MatrixTraverserStateManager(state)
callbackManager = MatrixTraverserCallbackManager(callbackMap)

matrixTraverser = MatrixTraverser(
    matrix, 
    Coordinate(0, 0),
    callbackManager,
    stateManager
)

# for now you cannot call the method more than once
matrixTraverser.traverseMatrix()