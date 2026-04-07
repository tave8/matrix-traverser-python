"""
PROBLEM: find the path where each cell must be exactly +1 from the previous 
"""

from MatrixTraverser import MatrixTraverser, MatrixTraverserCallbackManager, MatrixTraverserStateManager, Coordinate, Move



matrix = [
    ["S",   "8",  "9",  "9",   "90"],
    ["1",   "2",   "7",  "8",   "10"],
    ["10",  "3",  "6",  "11",  "13"],
    ["12",   "4",   "5",  "12",   "14"],
    ["5",    "6",  "12",  "16",   "E"]
]

state = {
    "reachedEnd": False,
    "values": [],
    "path": []
}
 

def onFirstVisitCallback(mt: MatrixTraverser, prevCoordinate: Coordinate, currCoordinate: Coordinate):
    print(f"{mt.getAtCoordinate(prevCoordinate)} --> {mt.getAtCoordinate(currCoordinate)}")
    pass


def canMoveCallback(mt: MatrixTraverser, desiredCoordinate: Coordinate, prevCoordinate: Coordinate, currCoordinate: Coordinate):

    state = mt.stateManager.getState()

    # if cell has arrived to end
    if state["reachedEnd"]:
        return False

    # if the next move brings the cell to end
    if mt.getAtCoordinate(desiredCoordinate) == "E":
        state["reachedEnd"] = True
        return True

    # from the start, you can only move to 
    # a cell with value 1
    if mt.getAtCoordinate(currCoordinate) == "S":
        return mt.getAtCoordinate(desiredCoordinate) == "1"

    # the next move cannot be the start 
    if mt.getAtCoordinate(desiredCoordinate) == "S":
        return False

    return int(mt.getAtCoordinate(currCoordinate))+1 == int(mt.getAtCoordinate(desiredCoordinate))




callbackMap = {
    "canMove": canMoveCallback,
    "onFirstVisit": onFirstVisitCallback
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



