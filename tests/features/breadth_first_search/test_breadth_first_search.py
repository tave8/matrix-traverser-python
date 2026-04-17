from typing import List

from src.components import Coordinate, Matrix, MatrixTree, Move
from src.core.MatrixTraverser import MatrixTraverser


def test_lower_diagonal():
    """
    Test the Breadth-First Search algorithm.
    By only moving to DOWN and DIAGONAL DOWN RIGHT
    (in this exact order) we are effectively
    traversing the lower diagonal area of the matrix.

    Area traversed:

    \
    | \
    | | \
    | | | \
    | | | | \

    """

    matrix = [
        [1,    2,    3,  4],
        [5,    6,    7,  8],
        [9,   10,   11,  12],
        [13,  14,   15,  16]
    ]

    # CALLBACK FOR ENGINE
    def getNextMoves(mt: MatrixTraverser,
                     currNode: MatrixTree) -> List[Move]:
        return [
            Move.DOWN,
            Move.DIAGONAL_DOWN_RIGHT
        ]

    startCoord = Coordinate(Matrix.getFirstRow(), Matrix.getFirstCol())

    matrixTraverser = MatrixTraverser(matrix, {
        "getNextMoves": getNextMoves
    })

    matrixTraverser.traverseMatrixBFS(startCoord)

    targetValue = 16
    (nodeFound, ancestors) = MatrixTree.findOneByValueFrom(matrixTraverser.matrixTree,
                                                           targetValue,
                                                           matrix)

    # the cell with value 16 has 3 ancestors: 1 -> 6 -> 11
    assert len(ancestors) == 3

    # count the nodes below the root node
    assert 9 == MatrixTree.countNodesBelow(ancestors[0])
    assert 2 == MatrixTree.countNodesBelow(ancestors[1])
    assert 1 == MatrixTree.countNodesBelow(ancestors[2])

    ancestorValues = [1, 6, 11]
    ancestorChildrenValues = {
        1: [5, 6],
        6: [11],
        11: [16]
    }


    i = 0

    for ancestor in ancestors:
        ancestorActualValue = Matrix.getAtCoordinate(matrix, ancestor.coord)
        ancestorExpectedValue = ancestorValues[i]
        # test the values of the ancestors
        assert ancestorActualValue == ancestorExpectedValue

        j = 0

        # test the values of the ancestor's children
        for child in ancestor.children:
            childExpectedValue = ancestorChildrenValues[ancestorActualValue][j]
            childActualValue = Matrix.getAtCoordinate(matrix, child.coord)
            assert childExpectedValue == childActualValue
            j += 1

        i += 1



def test_inverse_e():
    """
    Test the Breadth-First Search algorithm.
    By only moving to UP and LEFT
    (in this exact order) we are traversing
    a sort of inverse-E area.

    Area traversed:

    ---------
            |
    ---------
            |
    ---------
            |
    ---------

    """

    matrix = [
        [1,    2,   3,    4],
        [5,    6,   7,    8],
        [9,   10,   11,  12],
        [13,  14,   15,   16]
    ]

    # CALLBACK FOR ENGINE
    def getNextMoves(mt: MatrixTraverser,
                     currNode: MatrixTree) -> List[Move]:
        return [
            Move.UP,
            Move.LEFT
        ]

    # start from value 15
    startCoord = Coordinate(3, 2)

    matrixTraverser = MatrixTraverser(matrix, {
        "getNextMoves": getNextMoves
    })

    matrixTraverser.traverseMatrixBFS(startCoord)

    targetValue = 5
    (nodeFound, ancestors) = MatrixTree.findOneByValueFrom(matrixTraverser.matrixTree,
                                                           targetValue,
                                                           matrix)

    assert len(ancestors) == 4

    # # count the nodes below the root node
    assert 11 == MatrixTree.countNodesBelow(ancestors[0])
    assert 8 == MatrixTree.countNodesBelow(ancestors[1])
    assert 5 == MatrixTree.countNodesBelow(ancestors[2])

    assert 12 == MatrixTree.countNodesAt(ancestors[0])
    assert 9 == MatrixTree.countNodesAt(ancestors[1])
    assert 6 == MatrixTree.countNodesAt(ancestors[2])

    # ancestor values of value 5
    ancestorValues = [15, 11, 7, 6]

    ancestorChildrenValues = {
        15: [11, 14],
        11: [7, 10],
        7:  [3, 6],
        6:  [5]
    }

    assert len(ancestors[0].children) == len(ancestorChildrenValues[15])
    assert len(ancestors[1].children) == len(ancestorChildrenValues[11])
    assert len(ancestors[2].children) == len(ancestorChildrenValues[7])
    assert len(ancestors[3].children) == len(ancestorChildrenValues[6])

    assert Matrix.getAtCoordinate(matrix, ancestors[0].children[0].coord) == ancestorChildrenValues[15][0]
    assert Matrix.getAtCoordinate(matrix, ancestors[0].children[1].coord) == ancestorChildrenValues[15][1]
    assert Matrix.getAtCoordinate(matrix, ancestors[1].children[0].coord) == ancestorChildrenValues[11][0]
    assert Matrix.getAtCoordinate(matrix, ancestors[1].children[1].coord) == ancestorChildrenValues[11][1]
    assert Matrix.getAtCoordinate(matrix, ancestors[2].children[0].coord) == ancestorChildrenValues[7][0]
    assert Matrix.getAtCoordinate(matrix, ancestors[2].children[1].coord) == ancestorChildrenValues[7][1]
    assert Matrix.getAtCoordinate(matrix, ancestors[3].children[0].coord) == ancestorChildrenValues[6][0]
