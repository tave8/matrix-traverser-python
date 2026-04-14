
from src.components import Matrix, Move, Coordinate, MatrixTree
from tests.examples.line.prep.helpers import makeAndRunLinePattern
from tests.examples.line.prep.assertions import *


def test_down():

    startCoord = Coordinate(
        Matrix.getFirstRow(),
        Matrix.getFirstCol(),
    )

    matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]

    targetValue = 7
    move = Move.DOWN

    dataToTest = makeAndRunLinePattern(matrix, startCoord, move)

    (nodeFound, ancestors) = MatrixTree.findOneByValueFrom(
        dataToTest.patternTraverser.matrixTree,
        targetValue,
        matrix
    )

    # assert that the node found has
    # the value we were looking for
    assert isinstance(nodeFound, MatrixTree)
    # assert that the number of ancestors is 2 (they are 1 and 4)
    assert len(ancestors) == 2
    # the target value is equal to the value
    # at the coordinate in the node that was found
    assert targetValue == Matrix.getAtCoordinate(matrix, nodeFound.coord)
    # the first ancestor is 1
    assert Matrix.getAtCoordinate(matrix, ancestors[0].coord) == 1
    # the second ancestor is 4
    assert Matrix.getAtCoordinate(matrix, ancestors[1].coord) == 4



def test_diagonal_down_right():

    startCoord = Coordinate(
        Matrix.getFirstRow(),
        Matrix.getFirstCol(),
    )

    matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]

    targetValue = 9
    move = Move.DIAGONAL_DOWN_RIGHT

    dataToTest = makeAndRunLinePattern(matrix, startCoord, move)

    (nodeFound, ancestors) = MatrixTree.findOneByValueFrom(
        dataToTest.patternTraverser.matrixTree,
        targetValue,
        matrix
    )

    # assert that the node found has
    # the value we were looking for
    assert isinstance(nodeFound, MatrixTree)
    # assert that the number of ancestors is 2 (they are 1 and 5)
    assert len(ancestors) == 2
    # the target value is equal to the value
    # at the coordinate in the node that was found
    assert targetValue == Matrix.getAtCoordinate(matrix, nodeFound.coord)
    # the first ancestor is 1
    assert Matrix.getAtCoordinate(matrix, ancestors[0].coord) == 1
    # the second ancestor is 5
    assert Matrix.getAtCoordinate(matrix, ancestors[1].coord) == 5


def test_up():

    matrix = [
        [1, 7],
        [4, 6],
        [9, 5],
        [2, 4],
        [3, 3],
        [4, 2],
        [0, 1],
    ]

    startCoord = Coordinate(
        Matrix.getLastRow(matrix),
        Matrix.getLastCol(matrix),
    )


    # remember: the target value is only in the
    # moves that the algorithm is allowed to move,
    # which in this case is only UP
    targetValue = 7
    move = Move.UP

    dataToTest = makeAndRunLinePattern(matrix, startCoord, move)

    (nodeFound, ancestors) = MatrixTree.findOneByValueFrom(
        dataToTest.patternTraverser.matrixTree,
        targetValue,
        matrix
    )



    # assert that the node found has
    # the value we were looking for
    assert isinstance(nodeFound, MatrixTree)
    # assert that the number of ancestors is correct
    # print(ancestors)
    assert len(ancestors) == 6
    # # the target value is equal to the value
    # # at the coordinate in the node that was found
    # assert targetValue == Matrix.getAtCoordinate(matrix, nodeFound.coord)
    # # assert equality for each ancestor's value
    assert Matrix.getAtCoordinate(matrix, ancestors[0].coord) == 1
    assert Matrix.getAtCoordinate(matrix, ancestors[1].coord) == 2
    assert Matrix.getAtCoordinate(matrix, ancestors[2].coord) == 3
    assert Matrix.getAtCoordinate(matrix, ancestors[3].coord) == 4
    assert Matrix.getAtCoordinate(matrix, ancestors[4].coord) == 5
    assert Matrix.getAtCoordinate(matrix, ancestors[5].coord) == 6


