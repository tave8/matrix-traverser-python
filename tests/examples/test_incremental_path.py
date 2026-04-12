from src.components import Matrix, Coordinate, Move
from tests.examples.prework.incremental_path import makeAndRunIncrementalPathMaze
from tests.examples.assertions.incremental_path import *


def test_one_row_one_col_matrix():
    matrix = [
        ["S"]
    ]

    startCoord = Coordinate(
        Matrix.getFirstRow(),
        Matrix.getFirstCol()
    )

    dataToTest = makeAndRunIncrementalPathMaze(matrix, startCoord)

    assertStartMustExist(dataToTest.movesHistory)
    assertEndMustNotExist(dataToTest.movesHistory)
    assert len(dataToTest.movesHistory) == 1


def test_only_start_and_end():
    """
    Because in this problem, the algorithm must always start 
    with the first value (after start) being 1, this should not be allowed.
    """
    matrix = [
        ["S", "E"]
    ]

    startCoord = Coordinate(
        Matrix.getFirstRow(),
        Matrix.getFirstCol()
    )

    dataToTest = makeAndRunIncrementalPathMaze(matrix, startCoord)

    assert len(dataToTest.movesHistory) == 1
    assertStartMustExist(dataToTest.movesHistory)
    assertEndMustNotExist(dataToTest.movesHistory)



def test_only_one_between_start_and_end():
    matrix = [
        ["S", 1, "E"]
    ]

    startCoord = Coordinate(
        Matrix.getFirstRow(),
        Matrix.getFirstCol()
    )

    dataToTest = makeAndRunIncrementalPathMaze(matrix, startCoord)

    assertStartMustExist(dataToTest.movesHistory)
    assertEndMustExist(dataToTest.movesHistory)

    middleCells = dataToTest.movesHistory[1:-1]

    for i in range(1, len(middleCells)):
        cell = middleCells[i]
        assertOnCellInfo(cell)



def test_one_row_matrix_no_path():
    matrix = [
        ["S",  8,  9]
    ]

    startCoord = Coordinate(
        Matrix.getFirstRow(),
        Matrix.getFirstCol()
    )

    dataToTest = makeAndRunIncrementalPathMaze(matrix, startCoord)

    assert len(dataToTest.movesHistory) == 1
    assertStartMustExist(dataToTest.movesHistory)
    assertEndMustNotExist(dataToTest.movesHistory)


def test_one_row_matrix_path_exists():
    matrix = [
        ["S",  1,  2, "E"]
    ]

    startCoord = Coordinate(
        Matrix.getFirstRow(),
        Matrix.getFirstCol()
    )

    dataToTest = makeAndRunIncrementalPathMaze(matrix, startCoord)

    assertStartMustExist(dataToTest.movesHistory)
    assertEndMustExist(dataToTest.movesHistory)


def test_two_cols_zigzag_path_exists():
    matrix = [
        ["S",  90],
        [  1,   2],
        [ 90,   3],
        [  5,   4],
        [  6,  90],
        [  7,   8],
        [ 90,   9],
        [ 11,  10],
        [ 12,  90],
        [ 13,  14],
        [ 90,  15],
        [ 17,  16],
        [ 18,  90],
        [ 19,  20],
        [ 90,  21],
        [ 23,  22],
        [ 24,  90],
        [ 90,  25],
        [ 90,  26],
        [ 90, "E"]
    ]

    startCoord = Coordinate(
        Matrix.getFirstRow(),
        Matrix.getFirstCol()
    )

    dataToTest = makeAndRunIncrementalPathMaze(matrix, startCoord)

    assertStartMustExist(dataToTest.movesHistory)
    assertEndMustExist(dataToTest.movesHistory)

    middleCells = dataToTest.movesHistory[1:-1]

    for i in range(1, len(middleCells)):
        cell = middleCells[i]
        assertOnCellInfo(cell)


def test_all_ones_no_path():
    matrix = [
        ["S", 1,  1,  "E"],
        [1,   1,  1,   1],
        [1,   1,  1,   1],
        [1,   1,  1,   1],
    ]

    startCoord = Coordinate(
        Matrix.getFirstRow(),
        Matrix.getFirstCol()
    )

    dataToTest = makeAndRunIncrementalPathMaze(matrix, startCoord)

    assertStartMustExist(dataToTest.movesHistory)
    assertEndMustNotExist(dataToTest.movesHistory)



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

    dataToTest = makeAndRunIncrementalPathMaze(matrix, startCoord)

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

    dataToTest = makeAndRunIncrementalPathMaze(matrix, startCoord)

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

    dataToTest = makeAndRunIncrementalPathMaze(matrix, startCoord)

    assertStartMustExist(dataToTest.movesHistory)
    assertEndMustExist(dataToTest.movesHistory)

    middleCells = dataToTest.movesHistory[1:-1]

    for i in range(1, len(middleCells)):
        cell = middleCells[i]
        assertOnCellInfo(cell)


def test_many_candidate_neighbors_path_exists_1():

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

    dataToTest = makeAndRunIncrementalPathMaze(matrix, startCoord)

    assertStartMustExist(dataToTest.movesHistory)
    assertEndMustExist(dataToTest.movesHistory)

    middleCells = dataToTest.movesHistory[1:-1]

    for i in range(1, len(middleCells)):
        cell = middleCells[i]
        assertOnCellInfo(cell)

    


def test_many_candidate_neighbors_path_exists_2():

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

    dataToTest = makeAndRunIncrementalPathMaze(matrix, startCoord)

    assertStartMustExist(dataToTest.movesHistory)
    assertEndMustExist(dataToTest.movesHistory)

    middleCells = dataToTest.movesHistory[1:-1]

    for i in range(1, len(middleCells)):
        cell = middleCells[i]
        assertOnCellInfo(cell)


def test_many_candidate_neighbors_path_exists_3():
    matrix = [
        [  7,   8,   9,  10,  11,  12,  99,  99,  99,  99,  45,  46,  47,  48,  49],
        [  6,   9,  10,  11,  12,  13,  99,  99,  99,  99,  44,  47,  48,  49,  50],
        [  5,  10,  11,  12,  13,  14,  99,  99,  99,  99,  43,  48,  49,  50,  "E"],
        [  4,   5,   6,  13,  14,  15,  99,  99,  99,  99,  42,  99,  99,  99,  99],
        [  3,   4,   7,  14,  15,  16,  99,  99,  99,  99,  41,  99,  99,  99,  99],
        [  2,   3,   8,  15,  16,  17,  99,  99,  99,  99,  40,  99,  99,  99,  99],
        [  1,   2,   9,  16,  17,  18,  99,  99,  99,  99,  39,  99,  99,  99,  99],
        ["S",   1,  10,  17,  18,  19,  99,  99,  99,  99,  38,  99,  99,  99,  99],
        [ 99,   2,  11,  18,  19,  20,  99,  99,  99,  99,  37,  99,  99,  99,  99],
        [ 99,   3,  12,  19,  20,  21,  99,  99,  99,  99,  36,  99,  99,  99,  99],
        [ 99,   4,  13,  20,  21,  22,  99,  99,  99,  99,  35,  99,  99,  99,  99],
        [ 99,   5,  14,  21,  22,  23,  99,  99,  99,  99,  34,  99,  99,  99,  99],
        [ 99,   6,  15,  22,  23,  24,  99,  99,  99,  99,  33,  99,  99,  99,  99],
        [ 99,   7,  16,  23,  24,  25,  99,  99,  99,  99,  32,  99,  99,  99,  99],
        [ 99,   8,  17,  24,  25,  26,  27,  28,  29,  30,  31,  99,  99,  99,  99],
    ]

    startCoord = Coordinate(7, 0)

    dataToTest = makeAndRunIncrementalPathMaze(matrix, startCoord)

    assertStartMustExist(dataToTest.movesHistory)
    assertEndMustExist(dataToTest.movesHistory)

    middleCells = dataToTest.movesHistory[1:-1]

    for i in range(1, len(middleCells)):
        cell = middleCells[i]
        assertOnCellInfo(cell)




def test_only_one_candidate_neighbor_path_exists_1():
    matrix = [
        ["S",  1,  90,  90,  90,  90],
        [ 90,  2,  90,   7,   8,  90],
        [ 90,  3,  90,   6,   9,  90],
        [ 90,  4,   5,   5,  10,  90],
        [ 90, 90,  90,  90,  11,  90],
        [ 90, 90,  90,  90,  12, "E"]
    ]

    startCoord = Coordinate(
        Matrix.getFirstRow(),
        Matrix.getFirstCol()
    )

    dataToTest = makeAndRunIncrementalPathMaze(matrix, startCoord)

    assertStartMustExist(dataToTest.movesHistory)
    assertEndMustExist(dataToTest.movesHistory)

    middleCells = dataToTest.movesHistory[1:-1]

    for i in range(1, len(middleCells)):
        cell = middleCells[i]
        assertOnCellInfo(cell)



def test_only_one_candidate_neighbor_path_exists_2():
    matrix = [
        ["S",  1,  99,  99,  99,  99,  99,  99,  99,  99],
        [ 99,  2,  99,  99,  99,  99,  99,  99,  99,  99],
        [ 99,  3,   4,   5,   6,   7,   8,   9,  99,  99],
        [ 99,  99,  99,  99,  99,  99,  99,  10,  99,  99],
        [ 99,  99,  16,  15,  14,  13,  12,  11,  99,  99],
        [ 99,  99,  17,  99,  99,  99,  99,  99,  99,  99],
        [ 99,  99,  18,  99,  99,  99,  99,  99,  99,  99],
        [ 99,  99,  19,  20,  21,  22,  23,  24,  99,  99],
        [ 99,  99,  99,  99,  99,  99,  99,  25,  99,  99],
        [ 99,  99,  99,  99,  99,  99,  99,  26,  27, "E"]
    ]

    startCoord = Coordinate(
        Matrix.getFirstRow(),
        Matrix.getFirstCol()
    )

    dataToTest = makeAndRunIncrementalPathMaze(matrix, startCoord)

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

    dataToTest = makeAndRunIncrementalPathMaze(matrix, startCoord)

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

    dataToTest = makeAndRunIncrementalPathMaze(matrix, startCoord)

    assertStartMustExist(dataToTest.movesHistory)
    assertEndMustExist(dataToTest.movesHistory)

    middleCells = dataToTest.movesHistory[1:-1]

    for i in range(1, len(middleCells)):
        cell = middleCells[i]
        assertOnCellInfo(cell)



def test_start_end_bottom():
    matrix = [
        [ 10,   9,   8,   7,   6],
        [  9,   8,   7,   6,   5],
        [  2,   3,   4,   5,   4],
        [  1,   2,   3,   4,   3],
        ["S",  90,  90,  90, "E"]
    ]

    startCoord = Coordinate(
        Matrix.getLastRow(matrix),
        Matrix.getFirstCol()
    )

    dataToTest = makeAndRunIncrementalPathMaze(matrix, startCoord)

    assertStartMustExist(dataToTest.movesHistory)
    assertEndMustExist(dataToTest.movesHistory)

    middleCells = dataToTest.movesHistory[1:-1]

    for i in range(1, len(middleCells)):
        cell = middleCells[i]
        assertOnCellInfo(cell)


def test_only_one_of_multiple_paths():
    matrix = [
        [ 90,   7,  "E"],
        [ 90,   6,   7 ],
        [ 90,   5,   6 ],
        [ 90,   4,   5 ],
        [ 90,   3,   4 ],
        [  1,   2,   3 ],
        ["S",   1,   2 ]
    ]

    startCoord = Coordinate(
        Matrix.getLastRow(matrix),
        Matrix.getFirstCol()
    )

    dataToTest = makeAndRunIncrementalPathMaze(matrix, startCoord)

    assertStartMustExist(dataToTest.movesHistory)
    assertEndMustExist(dataToTest.movesHistory)

    middleCells = dataToTest.movesHistory[1:-1]

    for i in range(1, len(middleCells)):
        cell = middleCells[i]
        assertOnCellInfo(cell)




