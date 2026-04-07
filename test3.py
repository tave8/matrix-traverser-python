from MatrixTraverser import MatrixTraverser, MatrixTraverserCallbackManager, MatrixTraverserStateManager, Coordinate, Move

# matrix = [
#     ["S",   "8",  "9",  "9",   "90"],
#     ["1",   "2",   "7",  "8",   "10"],
#     ["3",   "43",  "6",  "11",  "13"],
#     ["3",   "4",   "5",  "12",   "14"],
#     ["5",   "6",  "12",  "16",   "E"]
# ]

matrix = [
    [1,   6,   11,  16,  21],
    [2,   7,   12,  17,  22],
    [3,   8,   13,  18,  23],
    [4,   9,   14,  19,  24],
    [5,   10,  15,  20,  25]
]

state = {
    "reachedEnd": False,
    "values": [],
    "path": []
}


def onFirstVisitCallback(mt: MatrixTraverser, prevCoordinate: Coordinate, currCoordinate: Coordinate):
    print(f"{mt.getAtCoordinate(prevCoordinate)} --> {mt.getAtCoordinate(currCoordinate)}")


def getNextMovesCallback(mt: MatrixTraverser, prevCoordinate: Coordinate, currCoordinate: Coordinate):
    # if mt.getAtCoordinate(currCoordinate) > 5:
    #     return [
    #         # Move.UP,
    #         Move.DIAGONAL_UP_RIGHT
    #     ]
    state = mt.stateManager.getState()


    # return [
    #     Move.DIAGONAL_DOWN_RIGHT
    # ]
    # pass 


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
    "onFirstVisit": onFirstVisitCallback,
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