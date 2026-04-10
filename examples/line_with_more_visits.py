"""
PROBLEM: Traverse the matrix in a custom line.

(must update drawing)
    < -------- ^
    |         / | 
    |       /   |
    v --------> |
    |    /      |
    | /         |
    v -----------

"""

from src.MatrixTraverser import Matrix, MatrixTraverser, Coordinate, Move, StateManager


matrix = [
    [11,   10,    9,   8,   7],
    [12,    8,    7,  2,    6],
    [1,    2,    3,  4,     5],
    [10,   19,    8,  4,    23],
    [18,   90,   9,   24,   25],
]

state = {

}


def beforeVisitCallback(mt: MatrixTraverser, 
                             prevCoordinate: Coordinate, 
                             currCoordinate: Coordinate,
                             prevMove: Move):
    if currCoordinate.isStart:
        print(f"START: {Matrix.getAtCoordinate(mt.matrix, currCoordinate)} ({prevMove.name})")
    else:
        print(f"FROM {Matrix.getAtCoordinate(mt.matrix, prevCoordinate)} TO {Matrix.getAtCoordinate(mt.matrix, currCoordinate)} ({prevMove.name})")
    pass




def getNextMovesCallback(mt: MatrixTraverser, 
                         prevCoord: Coordinate, 
                         currCoord: Coordinate,
                         prevMove: Move):
    
    # the most specific instruction first
    if currCoord.isStart:
        return [
            Move.RIGHT
        ]
    
    if prevMove == Move.DIAGONAL_UP_RIGHT and currCoord.isTopRight(matrix):
        return [
            Move.DOWN
        ]
    

    if prevMove == Move.DOWN and currCoord.isLastCol(mt.matrix):
        return [
            Move.DOWN
        ]
    
    if prevMove == Move.DIAGONAL_UP_RIGHT:
        return [
            Move.DIAGONAL_UP_RIGHT
        ]
    
    
    if currCoord.hasSameCoordinate(StateManager.getStartCoordinate(mt)):
        return [
            Move.DOWN
        ]

    if currCoord.isMiddleRow(mt.matrix) and currCoord.isLastCol(mt.matrix):
        return [
            Move.UP
        ]
    
    if currCoord.isTopLeft():
        return [
            Move.DOWN
        ]

    if currCoord.isBottomLeft(matrix):
        return [
            Move.DIAGONAL_UP_RIGHT
        ] 
    
 

    if currCoord.isMiddleRow(mt.matrix):
        return [
            Move.RIGHT
        ]

    if currCoord.isFirstRow():
        return [
            Move.LEFT
        ]
    
    if currCoord.isLastCol(mt.matrix):
        return [
            Move.UP
        ]

    if currCoord.isFirstCol():
        return [
            Move.DOWN
        ]
    
    return []


   


def canMoveCallback(mt: MatrixTraverser, 
                    desiredCoordinate: Coordinate, 
                    prevCoordinate: Coordinate, 
                    currCoordinate: Coordinate,
                    prevMove: Move):
    pass


def onMultipleVisitMustStopCallback(mt: MatrixTraverser, 
                                    prevCoordinate: Coordinate, 
                                    currCoordinate: Coordinate,
                                    prevMove: Move):


    # print("about to explore multiple times", currCoordinate)
    if currCoordinate.isFirstCol():
        return False
    
    if currCoordinate.isMiddleRow(mt.matrix):
        return False
    
    if currCoordinate.isLastCol(mt.matrix):
        return False


callbackMap = {
    "canMove": canMoveCallback,
    "getNextMoves": getNextMovesCallback,
    "beforeVisit": beforeVisitCallback,
    "onMultipleVisitMustStop": onMultipleVisitMustStopCallback
}



matrixTraverser = MatrixTraverser(
    matrix, 
    callbackMap,
    state
)



# for now you cannot call the method more than once
matrixTraverser.traverseMatrix(
    Coordinate.generateIsStartCoord(2, 0), 
    Coordinate.generateIsBeforeStartCoord()
)
