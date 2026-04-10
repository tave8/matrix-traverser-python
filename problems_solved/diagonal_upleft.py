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
    return [
        Move.DIAGONAL_UP_LEFT
    ]



def canMoveCallback(mt: MatrixTraverser, desiredCoordinate: Coordinate, prevCoordinate: Coordinate, currCoordinate: Coordinate):
    # return [
    #     Move.DOWN,
    #     Move.UP
    # ]
    # if mt.getAtCoordinate(desiredCoordinate) > 5:
    #     return False
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
    Coordinate(4, 4),
    callbackManager,
    stateManager
)

# for now you cannot call the method more than once
matrixTraverser.traverseMatrix()