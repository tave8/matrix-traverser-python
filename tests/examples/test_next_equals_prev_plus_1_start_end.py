from src.components import Matrix, Coordinate, Move
from tests.examples.prework.next_equals_prev_plus_1 import *
from tests.examples.assertions.next_equals_prev_plus_1 import *




# tests whether the first and last values 
# are the start (S) and end (E)
# and whether each cell's value = prev cell value + 1
def test_first_cell_is_start_and_last_is_end():

    matrix = [
            ["S",  2,  2,  3,  4,  5],
            [ 1,   3,  2,  4,  5,  6],
            [ 2,   2,  4,  5,  6,  7],
            [ 3,   4,  3,  5,  7,  8],
            [ 4,   5,  6,  8,  6,  9],
            [ 5,   8, 11,  9, 11,  2],
            [ 6,   7, 10, 10,  8, "E"]
    ]


    startCoord = Coordinate(
        Matrix.getFirstRow(),
        Matrix.getFirstCol()
    )

    dataToTest = makeAndRunMazeTraverser(matrix, startCoord)

    # for cellInfo in mazeTraverser.getMovesHistory():
    #     print(cellInfo)

    assert len(dataToTest.movesHistory) > 1
    assertStartMustExist(dataToTest.movesHistory)
    assertEndMustExist(dataToTest.movesHistory)



def test_has_only_start():
    matrix = [
        ["S",  8,  9],
        [ 99, 99, 99],
        [  5,  6, "E"]
    ]

    startCoord = Coordinate(
        Matrix.getFirstRow(),
        Matrix.getFirstCol()
    )

    dataToTest = makeAndRunMazeTraverser(matrix, startCoord)

    assert len(dataToTest.movesHistory) == 1
    assertStartMustExist(dataToTest.movesHistory)
    assertEndMustNotExist(dataToTest.movesHistory)


def test_non_ambiguous_matrix():

    matrix = [
        ["S",  8,  9,  9, 90],
        [ 1,   2,  7,  8, 10],
        [10,   3,  4,  5, 13],
        [12,   8, 10,  6, 14],
        [ 5,   6,  5, 16, "E"]
    ]

    startCoord = Coordinate(
        Matrix.getFirstRow(),
        Matrix.getFirstCol()
    )

    dataToTest = makeAndRunMazeTraverser(matrix, startCoord)

    assertStartMustExist(dataToTest.movesHistory)
    assertEndMustExist(dataToTest.movesHistory)

    middleCells = dataToTest.movesHistory[1:-1]

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

    startCoord = Coordinate(
        Matrix.getFirstRow(),
        Matrix.getFirstCol()
    )

    dataToTest = makeAndRunMazeTraverser(matrix, startCoord)

    assertStartMustExist(dataToTest.movesHistory)
    assertEndMustExist(dataToTest.movesHistory)

    middleCells = dataToTest.movesHistory[1:-1]

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


    startCoord = Coordinate(
        Matrix.getLastRow(matrix),
        Matrix.getLastCol(matrix)
    )

    dataToTest = makeAndRunMazeTraverser(matrix, startCoord)

    assertStartMustExist(dataToTest.movesHistory)
    assertEndMustExist(dataToTest.movesHistory)

    middleCells = dataToTest.movesHistory[1:-1]

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

    startCoord = Coordinate(
        Matrix.getLastRow(matrix),
        Matrix.getLastCol(matrix)
    )

    dataToTest = makeAndRunMazeTraverser(matrix, startCoord)

    assertStartMustExist(dataToTest.movesHistory)
    assertEndMustNotExist(dataToTest.movesHistory)




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

    startCoord = Coordinate(
        Matrix.getMiddleRow(matrix),
        Matrix.getMiddleCol(matrix)
    )

    dataToTest = makeAndRunMazeTraverser(matrix, startCoord)

    assertStartMustExist(dataToTest.movesHistory)
    assertEndMustExist(dataToTest.movesHistory)

    middleCells = dataToTest.movesHistory[1:-1]

    for i in range(1, len(middleCells)):
        cell = middleCells[i]
        assertOnCellInfo(cell)

