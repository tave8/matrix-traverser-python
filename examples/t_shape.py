"""
PROBLEM: Traverse the matrix in T shape, 
so first row and the column in the middle.
"""

from core.MatrixTraverser import Matrix, MatrixTraverser, Coordinate, Move


matrix = [
    [1,    2,  3,   4,    5],
    [23,   0,  6,  17,  22],
    [32,   8,  7,  18,  23],
    [4,   11,  8,  19,  24],
    [5,   10,  9,  20,  25]
]

state = {}


def beforeFirstVisitCallback(mt: MatrixTraverser, 
                             prevCoordinate: Coordinate, 
                             currCoordinate: Coordinate,
                             prevMove: Move):
    if currCoordinate.isStart:
        print(f"START: {Matrix.getAtCoordinate(mt.matrix, currCoordinate)} ({prevMove.name})")
    else:
        print(f"FROM {Matrix.getAtCoordinate(mt.matrix, prevCoordinate)} TO {Matrix.getAtCoordinate(mt.matrix, currCoordinate)} ({prevMove.name})")
    pass


def getNextMovesCallback(mt: MatrixTraverser, 
                         prevCoordinate: Coordinate, 
                         currCoordinate: Coordinate,
                         prevMove: Move):
    
    # if this is the cell right 
    # at the intersection in the T shape
    # this cell must move first right, and then down
    if currCoordinate.isFirstRow() and currCoordinate.isCol(2):
        return [
            Move.RIGHT,
            Move.DOWN
        ]
    
    # if this is the cell in a column in the middle,
    # it can only move down
    if currCoordinate.isCol(2):
        return [
            Move.DOWN
        ]

    # if this is the first row, you can only move right
    if currCoordinate.isFirstRow():
        return [
            Move.RIGHT
        ]
    
    # for any other cell, you cannot move anywhere else
    return []


def canMoveCallback(mt: MatrixTraverser, 
                    desiredCoordinate: Coordinate, 
                    prevCoordinate: Coordinate, 
                    currCoordinate: Coordinate,
                    prevMove: Move):
    pass


callbackMap = {
    "canMove": canMoveCallback,
    "getNextMoves": getNextMovesCallback,
    "beforeFirstVisit": beforeFirstVisitCallback,
}



matrixTraverser = MatrixTraverser(
    matrix, 
    callbackMap,
    state
)

# for now you cannot call the method more than once
matrixTraverser.traverseMatrix(
    Coordinate.generateIsStartCoord(0, 0), 
    Coordinate.generateIsBeforeStartCoord()
)