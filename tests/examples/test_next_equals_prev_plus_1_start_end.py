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
        nextNum = int(Matrix.getAtCoordinate(mt.matrix, desiredCoord)) # type: ignore
        currNum = int(Matrix.getAtCoordinate(mt.matrix, currCoord)) # type: ignore
        return nextNum == currNum + 1

    callbackMap = {
        "canMoveTo": canMoveToCallback
    }

    callbackMap.update(moreCallbackMap)

    mt = MatrixTraverser(matrix, callbackMap, state)
    mt.traverseMatrix(startCoord)
    return mt


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

    # should only contain S, never reaching E
    assert len(visitedCells) == 1 and visitedCells[0]["currValue"] == "S"


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

    # path must start at S and end at E
    assert visitedCells[0]["currValue"] == "S"
    assert visitedCells[-1]["currValue"] == "E"

    middleCells = visitedCells[1:-1]

    for i in range(1, len(middleCells)):
        cell = middleCells[i]
        # the distance of the move must be 1 cell
        # (they must be adjacent)
        assert Coordinate.areAdjacent(cell["currCoord"], cell["prevCoord"])
        # current value is previous value + 1
        assert int(cell["currValue"]) == int(cell["prevValue"]) + 1


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

    # path must start at S and end at E
    assert visitedCells[0]["currValue"] == "S"
    assert visitedCells[-1]["currValue"] == "E"

    # for visitedCell in visitedCells:
    #     print(visitedCell["prevValue"], visitedCell["currValue"])

    # every step between S and E must increment by exactly 1
    # skip first cell (S) and last cell (E)
    middleCells = visitedCells[1:-1]

    for i in range(1, len(middleCells)):
        cell = middleCells[i]
        # the distance of the move must be 1 cell
        # (they must be adjacent)
        assert Coordinate.areAdjacent(cell["currCoord"], cell["prevCoord"])
        # current value is previous value + 1
        assert int(cell["currValue"]) == int(cell["prevValue"]) + 1
    

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

    # path must start at S and end at E
    assert visitedCells[0]["currValue"] == "S"
    assert visitedCells[-1]["currValue"] == "E"

    # for visitedCell in visitedCells:
    #     print(visitedCell["prevValue"], visitedCell["currValue"])

    # every step between S and E must increment by exactly 1
    # skip first cell (S) and last cell (E)
    middleCells = visitedCells[1:-1]

    for i in range(1, len(middleCells)):
        cell = middleCells[i]
        # the distance of the move must be 1 cell
        # (they must be adjacent)
        assert Coordinate.areAdjacent(cell["currCoord"], cell["prevCoord"])
        # current value is previous value + 1
        assert int(cell["currValue"]) == int(cell["prevValue"]) + 1
    

# def test_path_no_exists():

#     matrix = [
#         ["E",  8,  7,  6,  4,  5],
#         [ 1,  11, 12,  5, 13, 12],
#         [ 2,  11, 15,  4, 11,  7],
#         [ 3,  10, 16,  3,  7,  8],
#         [ 4,   9,  9,  8,  2,  9],
#         [ 7,   8,  4,  9,  1,  2],
#         [ 6,   5,  3,  2,  1, "S"]
#     ]

#     def beforeFirstVisitCallback(mt: MatrixTraverser, 
#                              prevCoordinate: Coordinate, 
#                              currCoordinate: Coordinate,
#                              prevMove: Move):
#         if currCoordinate.isStart:
#             print(f"START: {Matrix.getAtCoordinate(mt.matrix, currCoordinate)} ({prevMove.name})")
#         else:
#             print(f"FROM {Matrix.getAtCoordinate(mt.matrix, prevCoordinate)} TO {Matrix.getAtCoordinate(mt.matrix, currCoordinate)} ({prevMove.name})")


#     mt = makeTraverser(
#         matrix, 
#         Coordinate(Matrix.getLastRow(matrix), Matrix.getLastCol(matrix)),
#         {
#             "beforeFirstVisit": beforeFirstVisitCallback
#         }
#     )


#     visitedCells = mt.stateManager.state["movesFromTo"]

#     # path must start at S and end at E
#     assert visitedCells[0]["currValue"] == "S"
#     assert visitedCells[-1]["currValue"] == "E"

#     # for visitedCell in visitedCells:
#     #     print(visitedCell["prevValue"], visitedCell["currValue"])

#     # every step between S and E must increment by exactly 1
#     # skip first cell (S) and last cell (E)
#     middleCells = visitedCells[1:-1]

#     for i in range(1, len(middleCells)):
#         cell = middleCells[i]
#         # the distance of the move must be 1 cell
#         # (they must be adjacent)
#         assert Coordinate.areAdjacent(cell["currCoord"], cell["prevCoord"])
#         # current value is previous value + 1
#         assert int(cell["currValue"]) == int(cell["prevValue"]) + 1