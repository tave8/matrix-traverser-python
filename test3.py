from MatrixTraverser import MatrixTraverser, MatrixTraverserCallbackManager, MatrixTraverserStateManager
from Coordinate import Coordinate

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


callbackMap = {
    # "canMove": canMoveCallback,
    # "firstVisit": firstVisitCallback,
    # "pilotCell": pilotCellCallback
}


stateManager = MatrixTraverserStateManager(state)
callbackManager = MatrixTraverserCallbackManager(callbackMap)
startCoordinate = Coordinate(0, 0)

matrixTraverser = MatrixTraverser(
    matrix, 
    startCoordinate,
    callbackManager,
    stateManager
)

matrixTraverser.traverseMatrix()