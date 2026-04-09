"""
PROBLEM: Traverse the matrix in a line.


"""

from MatrixTraverser import Matrix, MatrixTraverser, Coordinate, Move, StateManager


matrix = [
    [11,   10,    9,   8,   7],
    [12,    8,    7,  2,    6],
    [1,    2,    3,  4,    5],
    [10,   6,    8,  4,    23],
    [11,   19,   9,   24,  25]
]

state = {

}


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
                         prevCoord: Coordinate, 
                         currCoord: Coordinate,
                         prevMove: Move):

    if currCoord.isStart:
        return [
            Move.RIGHT
        ]
    
    if currCoord.hasSameCoordinate(StateManager.getStartCoordinate(mt)):
        return [
            Move.DOWN
        ]

    # the most specific instruction first
    if currCoord.isMiddleRow(mt.matrix) and currCoord.isLastCol(mt.matrix):
        return [
            Move.UP
        ]
    
    if currCoord.isFirstRow() and currCoord.isFirstCol():
        return [
            Move.DOWN
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
    


callbackMap = {
    "canMove": canMoveCallback,
    "getNextMoves": getNextMovesCallback,
    "beforeFirstVisit": beforeFirstVisitCallback,
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
