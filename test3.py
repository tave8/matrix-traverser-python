from MatrixTraverser import MatrixTraverser, MatrixTraverserCallbackManager, MatrixTraverserStateManager, Coordinate

matrix = [
    ["S",   "8",  "9",  "9",   "90"],
    ["1",   "2",   "7",  "8",   "10"],
    ["3",   "43",  "6",  "11",  "13"],
    ["3",   "4",   "5",  "12",   "14"],
    ["5",   "6",  "12",  "16",   "E"]
]

state = {
    "reachedEnd": False,
    "values": [],
    "path": []
}


def onFirstVisitCallback(mt: MatrixTraverser, prevCoordinate: Coordinate, currCoordinate: Coordinate):
    print(f"{mt.getAtCoordinate(prevCoordinate)} --> {mt.getAtCoordinate(currCoordinate)}")


callbackMap = {
    # "canMove": canMoveCallback,
    "onFirstVisit": onFirstVisitCallback,
    # "pilotCell": pilotCellCallback
}


stateManager = MatrixTraverserStateManager(state)
callbackManager = MatrixTraverserCallbackManager(callbackMap)
startCoordinate = Coordinate(2, 0)

matrixTraverser = MatrixTraverser(
    matrix, 
    startCoordinate,
    callbackManager,
    stateManager
)

matrixTraverser.traverseMatrix()