from src.MatrixTraverser import Matrix, MatrixTraverser, Coordinate, Move, StateManager


def makeTraverser(matrix):

    state = {}

    def canMoveToCallback(mt, desiredCoord, prevCoord, currCoord, prevMove):
        if currCoord.isStart:
            return Matrix.getAtCoordinate(mt.matrix, desiredCoord) == "1"
        if Matrix.getAtCoordinate(mt.matrix, desiredCoord) == "S":
            return False
        if Matrix.getAtCoordinate(mt.matrix, desiredCoord) == "E":
            return True
        if Matrix.getAtCoordinate(mt.matrix, currCoord) == "E":
            StateManager.setWasEnded(mt, True)
            return
        nextNum = int(Matrix.getAtCoordinate(mt.matrix, desiredCoord)) # type: ignore
        currNum = int(Matrix.getAtCoordinate(mt.matrix, currCoord)) # type: ignore
        return nextNum == currNum + 1


    callbackMap = {
        "canMoveTo": canMoveToCallback
    }

    mt = MatrixTraverser(matrix, callbackMap, state)
    mt.traverseMatrix(Coordinate(Matrix.getFirstRow(), Matrix.getFirstCol()))
    return mt


# tests whether the first and last values 
# are the start (S) and end (E)
# and whether each cell's value = prev cell value + 1
def test_firstCellIsStartAndLastIsEnd():
    matrix = [
        ["S",  "8",  "9",  "9",  "90"],
        ["1",  "2",  "7",  "8",  "10"],
        ["10", "3",  "6",  "9",  "13"],
        ["12", "4",  "10", "6",  "14"],
        ["5",  "6",  "5",  "16", "E"]
    ]

    mt = makeTraverser(matrix)
    visitedCells = mt.stateManager.state["visitedCellsSoFar"]

    assert len(visitedCells) > 1
    # path must start at S and end at E
    assert visitedCells[0]["currValue"] == "S"
    assert visitedCells[-1]["currValue"] == "E"


def test_allCellsExceptStartOrEndAreIncremental():

    matrix = [
        ["S",  "8",  "9",  "9",  "90"],
        ["1",  "2",  "7",  "8",  "10"],
        ["10", "3",  "6",  "9",  "13"],
        ["12", "4",  "10", "6",  "14"],
        ["5",  "6",  "5",  "16", "E"]
    ]

    mt = makeTraverser(matrix)
    visitedCells = mt.stateManager.state["visitedCellsSoFar"]

    # every step between S and E must increment by exactly 1
    # skip first cell (S) and last cell (E)
    middleCells = visitedCells[1:-1]

    for i in range(1, len(middleCells)):
        currValue = int(middleCells[i]["currValue"])
        prevValue = int(middleCells[i - 1]["currValue"])
        assert currValue == prevValue + 1



def test_hasOnlyStart():
    matrix = [
        ["S",  "8",  "9"],
        ["99", "99", "99"],
        ["5",  "6",  "E"]
    ]

    mt = makeTraverser(matrix)
    visitedCells = mt.stateManager.state["visitedCellsSoFar"]

    # should only contain S, never reaching E
    assert len(visitedCells) == 1 and visitedCells[0]["currValue"] == "S"