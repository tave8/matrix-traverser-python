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


    # MatrixTree.findAllAncestorsOf(root)


    # targetValue = 12
    # (nodeFound, ancestors) = MatrixTree.findOneByValueFrom(matrixTraverser.matrixTree, targetValue, matrix)
    #
    # print()
    # # for each ancestor, see its children
    # print("******** ANCESTORS FOR VALUE: ", targetValue)
    # print("NODE FOUND: ", nodeFound)
    #
    # print()
    # for ancestor in ancestors:
    #     ancestorValue = Matrix.getAtCoordinate(matrix, ancestor.coord)
    #     print("ancestor: ", ancestorValue)
    #     for child in ancestor.children:
    #         childValue = Matrix.getAtCoordinate(matrix, child.coord)
    #         print("  > child: ", childValue)
    #




#
# targetValue = 13
# (nodeFound, ancestors) = MatrixTree.findOneByValueFrom(matrixTraverser.matrixTree, targetValue, matrix)
#
# print()
# # for each ancestor, see its children
# print("******** ANCESTORS FOR VALUE: ", targetValue)
# print("NODE FOUND: ", nodeFound)
#
# print()
# for ancestor in ancestors:
#     ancestorValue = Matrix.getAtCoordinate(matrix, ancestor.coord)
#     print("ancestor: ", ancestorValue)
#     for child in ancestor.children:
#         childValue = Matrix.getAtCoordinate(matrix, child.coord)
#         print("  > child: ", childValue)
