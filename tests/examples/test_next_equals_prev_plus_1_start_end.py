from src.MatrixTraverser import Matrix, MatrixTraverser, Coordinate, Move, StateManager


def makeTraverser(matrix, 
                  startCoord: Coordinate,
                  moreCallbackMap={}):

    state = {}

    def canMoveToCallback(mt, desiredCoord, prevCoord, currCoord, prevMove):
        if currCoord.isStart:
            return Matrix.getAtCoordinate(mt.matrix, desiredCoord) == 1
        if Matrix.getAtCoordinate(mt.matrix, desiredCoord) == "S":
            return False
        if Matrix.getAtCoordinate(mt.matrix, desiredCoord) == "E":
            return True
        if Matrix.getAtCoordinate(mt.matrix, currCoord) == "E":
            StateManager.setWasEnded(mt, True)
            return
        nextNum = Matrix.getAtCoordinate(mt.matrix, desiredCoord) # type: ignore
        currNum = Matrix.getAtCoordinate(mt.matrix, currCoord) # type: ignore
        return nextNum == currNum + 1 # type: ignore

    callbackMap = {
        "canMoveTo": canMoveToCallback
    }

    callbackMap.update(moreCallbackMap)

    mt = MatrixTraverser(matrix, callbackMap, state)
    mt.traverseMatrix(startCoord)
    return mt


def assertOnCellInfo(cellInfo: dict):
        assert isinstance(cellInfo["prevCoord"], Coordinate)
        assert isinstance(cellInfo["currCoord"], Coordinate)
        assert Coordinate.areAdjacent(cellInfo["currCoord"], cellInfo["prevCoord"])

        # the previous cell is the start, so 
        # to the next cell must be 1
        if cellInfo["prevValue"] == "S":
            assert isinstance(cellInfo["currValue"], int)
            assert cellInfo["currValue"] == 1
        else:
            assert isinstance(cellInfo["prevValue"], int)
            assert isinstance(cellInfo["currValue"], int)
            # for each cell pair in a move, this property must be satisfied
            assert cellInfo["currValue"] == cellInfo["prevValue"] + 1


def assertStartMustExist(cells: list[dict]):
    assert cells[0]["currValue"] == "S" 

def assertEndMustExist(cells: list[dict]):
    assert cells[-1]["currValue"] == "E" 

def assertEndMustNotExist(cells: list[dict]):
    assert cells[-1]["currValue"] != "E" 


# tests whether the first and last values 
# are the start (S) and end (E)
# and whether each cell's value = prev cell value + 1
def test_first_cell_is_start_and_last_is_end():
    matrix = [
        ["S",  8,  9,  9, 90],
        [ 1,  2,  7,  8, 10],
        [10,  3,  6,  9, 13],
        [12,  4, 10,  6, 14],
        [ 5,  6,  5, 16, "E"]
    ]

    mt = makeTraverser(matrix, Coordinate(Matrix.getFirstRow(), Matrix.getFirstCol()))
    visitedCells = mt.stateManager.state["movesFromTo"]

    assert len(visitedCells) > 1
    # path must start at S and end at E
    assert visitedCells[0]["currValue"] == "S"
    assert visitedCells[-1]["currValue"] == "E"


def test_has_only_start():
    matrix = [
        ["S",  8,  9],
        [ 99, 99, 99],
        [  5,  6, "E"]
    ]

    mt = makeTraverser(matrix, Coordinate(Matrix.getFirstRow(), Matrix.getFirstCol()))

    visitedCells = mt.stateManager.state["movesFromTo"]

    assert len(visitedCells) == 1
    assertStartMustExist(visitedCells)
    assertEndMustNotExist(visitedCells)


def test_non_ambiguous_matrix():

    matrix = [
        ["S",  8,  9,  9, 90],
        [ 1,   2,  7,  8, 10],
        [10,   3,  4,  5, 13],
        [12,   8, 10,  6, 14],
        [ 5,   6,  5, 16, "E"]
    ]

    mt = makeTraverser(matrix, Coordinate(Matrix.getFirstRow(), Matrix.getFirstCol()))

    visitedCells = mt.stateManager.state["movesFromTo"]

    assertStartMustExist(visitedCells)
    assertEndMustExist(visitedCells)

    middleCells = visitedCells[1:-1]

    for i in range(1, len(middleCells)):
        cell = middleCells[i]
        assertOnCellInfo(cell)


def test_many_neighbors_with_incremental_values():

    matrix = [
        ["S",  1,  2,  3,  4,  5],
        [ 1,   1,  2,  4,  5,  6],
        [ 2,   2,  4,  5,  6,  7],
        [ 3,   4,  3,  5,  7,  8],
        [ 4,   5,  6,  8,  6,  9],
        [ 5,   8, 11,  9, 11,  2],
        [ 6,   7, 10, 10,  8, "E"]
    ]

    mt = makeTraverser(matrix, Coordinate(Matrix.getFirstRow(), Matrix.getFirstCol()))


    visitedCells = mt.stateManager.state["movesFromTo"]

    assertStartMustExist(visitedCells)
    assertEndMustExist(visitedCells)

    middleCells = visitedCells[1:-1]

    for i in range(1, len(middleCells)):
        cell = middleCells[i]
        assertOnCellInfo(cell)

    


def test_many_neighbors_with_incremental_values_and_swapped_start():

    matrix = [
        ["E", 22, 21,  3,  4,   5],
        [  1, 20,  2,  4, 13,  12],
        [  2, 19, 15, 14, 11,   7],
        [  3, 18, 16, 10,  7,   8],
        [  4, 17,  9,  8,  6,   9],
        [  7,  8,  4,  9, 11,   2],
        [  6,  5,  3,  2,  1, "S"]
    ]

    def beforeFirstVisitCallback(mt: MatrixTraverser, 
                             prevCoordinate: Coordinate, 
                             currCoordinate: Coordinate,
                             prevMove: Move):
        if currCoordinate.isStart:
            print(f"START: {Matrix.getAtCoordinate(mt.matrix, currCoordinate)} ({prevMove.name})")
        else:
            print(f"FROM {Matrix.getAtCoordinate(mt.matrix, prevCoordinate)} TO {Matrix.getAtCoordinate(mt.matrix, currCoordinate)} ({prevMove.name})")


    mt = makeTraverser(
        matrix, 
        Coordinate(Matrix.getLastRow(matrix), Matrix.getLastCol(matrix)),
        {
            "beforeFirstVisit": beforeFirstVisitCallback
        }
    )


    visitedCells = mt.stateManager.state["movesFromTo"]

    assertStartMustExist(visitedCells)
    assertEndMustExist(visitedCells)

    middleCells = visitedCells[1:-1]

    for i in range(1, len(middleCells)):
        cell = middleCells[i]
        assertOnCellInfo(cell)

    

def test_path_no_exists():

    matrix = [
        ["E",  9,  9,  8,  7,  6],
        [ 1,  11, 12,  5, 13,  5],
        [ 2,  11, 15,  4, 11,  4],
        [ 3,  10, 16,  3,  7,  3],
        [ 4,   9,  9,  8,  2,  2],
        [ 7,   8,  4,  9,  1,  1],
        [ 6,   5,  3,  2,  1, "S"]
    ]

    def beforeFirstVisitCallback(mt: MatrixTraverser, 
                             prevCoordinate: Coordinate, 
                             currCoordinate: Coordinate,
                             prevMove: Move):
        if currCoordinate.isStart:
            print(f"START: {Matrix.getAtCoordinate(mt.matrix, currCoordinate)} ({prevMove.name})")
        else:
            print(f"FROM {Matrix.getAtCoordinate(mt.matrix, prevCoordinate)} TO {Matrix.getAtCoordinate(mt.matrix, currCoordinate)} ({prevMove.name})")


    mt = makeTraverser(
        matrix, 
        Coordinate(Matrix.getLastRow(matrix), Matrix.getLastCol(matrix)),
        {
            "beforeFirstVisit": beforeFirstVisitCallback
        }
    )


    visitedCells = mt.stateManager.state["movesFromTo"]

    assertStartMustExist(visitedCells)
    assertEndMustNotExist(visitedCells)




def test_start_from_center():

    matrix = [
        [  2,  22,   4,    3,     4,    5,  8],
        [  1,  20,   5,    2,     13,   12,  2],
        [  8,  7,    6,    1,     11,   7,  9],
        [  3,  18,   3,    "S",    7,   8,  10],
        [  4,  "E",  9,     1,     6,   9,  11],
        [  7,   8,   4,     2,    11,   2,  12],
        [  6,   5,   3,     2,     1,   5,  12],
    ]

    def beforeFirstVisitCallback(mt: MatrixTraverser, 
                             prevCoordinate: Coordinate, 
                             currCoordinate: Coordinate,
                             prevMove: Move):
        if currCoordinate.isStart:
            print(f"START: {Matrix.getAtCoordinate(mt.matrix, currCoordinate)} ({prevMove.name})")
        else:
            print(f"FROM {Matrix.getAtCoordinate(mt.matrix, prevCoordinate)} TO {Matrix.getAtCoordinate(mt.matrix, currCoordinate)} ({prevMove.name})")


    mt = makeTraverser(
        matrix, 
        Coordinate(Matrix.getMiddleRow(matrix), Matrix.getMiddleCol(matrix)),
        {
            "beforeFirstVisit": beforeFirstVisitCallback
        }
    )


    visitedCells = mt.stateManager.state["movesFromTo"]

    assertStartMustExist(visitedCells)
    assertEndMustExist(visitedCells)
    
    middleCells = visitedCells[1:-1]

    for i in range(1, len(middleCells)):
        cell = middleCells[i]
        assertOnCellInfo(cell)
