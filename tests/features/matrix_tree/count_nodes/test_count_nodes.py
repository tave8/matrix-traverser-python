from typing import List

from src.components import Coordinate, Matrix, MatrixTree, Move
from src.core.MatrixTraverser import MatrixTraverser
from src.core.PatternTraverser import PatternTraverser
from src.implementations.line_pattern import makeLinePattern
from src.implementations.t_shape_pattern import makeTShapePattern
from src.implementations.zigzag_pattern import makeZigzagPattern
from src.core.MatrixTraverser import MatrixTraverser


def test_count_nodes_in_line():

    matrix = [
        [1,    2,    3,  4],
        [5,    6,    7,  8],
        [9,   10,   11,  12],
        [13,  14,   15,  16]
    ]


    startCoord = Coordinate(Matrix.getFirstRow(), Matrix.getFirstCol())

    linePattern = makeLinePattern(matrix, Move.DIAGONAL_DOWN_RIGHT)

    linePattern.run(startCoord)

    targetValue = 16
    (nodeFound, ancestors) = MatrixTree.findOneByValueFrom(linePattern.matrixTree,
                                                           targetValue,
                                                           matrix)

    totalNodesCount = MatrixTree.countNodesAt(linePattern.matrixTree)

    # the ancestors are 3:
    # ancestors of 16:   1 -> 6 -> 11
    assert len(ancestors) == 3
    #
    # however the total count of nodes (ancestors + the node itself) is 4
    assert totalNodesCount == 4

    assert Matrix.getAtCoordinate(matrix, ancestors[0].coord) == 1
    assert Matrix.getAtCoordinate(matrix, ancestors[1].coord) == 6
    assert Matrix.getAtCoordinate(matrix, ancestors[2].coord) == 11



def test_count_nodes_in_t_shape():

    matrix = [
        [1,    2,    3,  4,   7],
        [5,    6,    7,  8,   7],
        [9,   10,   11,  12,  7],
        [13,  14,   15,  16,  7]
    ]


    startCoord = Coordinate(Matrix.getFirstRow(), Matrix.getFirstCol())

    tShapePattern = makeTShapePattern(matrix)

    tShapePattern.run(startCoord)

    targetValue = 15
    (nodeFound, ancestors) = MatrixTree.findOneByValueFrom(tShapePattern.matrixTree,
                                                           targetValue,
                                                           matrix)

    totalNodesCount = MatrixTree.countNodesAt(tShapePattern.matrixTree)

    # the ancestors are 5:
    # ancestors of 15:   1 -> 2 -> 3 -> 7 -> 11
    assert len(ancestors) == 5

    assert totalNodesCount == 8

    assert Matrix.getAtCoordinate(matrix, ancestors[0].coord) == 1
    assert Matrix.getAtCoordinate(matrix, ancestors[1].coord) == 2
    assert Matrix.getAtCoordinate(matrix, ancestors[2].coord) == 3
    assert Matrix.getAtCoordinate(matrix, ancestors[3].coord) == 7
    assert Matrix.getAtCoordinate(matrix, ancestors[4].coord) == 11




def test_count_nodes_in_zigzag():

    matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]


    startCoord = Coordinate(Matrix.getFirstRow(), Matrix.getFirstCol())

    zigzagPattern = makeZigzagPattern(matrix)

    zigzagPattern.run(startCoord)

    targetValue = 9
    (nodeFound, ancestors) = MatrixTree.findOneByValueFrom(zigzagPattern.matrixTree,
                                                           targetValue,
                                                           matrix)

    totalNodesCount = MatrixTree.countNodesAt(zigzagPattern.matrixTree)

    assert len(ancestors) == 8

    assert totalNodesCount == 9

    # for ancestor in ancestors:
    # print(Matrix.getAtCoordinate(matrix, ancestor.coord))

    assert Matrix.getAtCoordinate(matrix, ancestors[0].coord) == 1
    assert Matrix.getAtCoordinate(matrix, ancestors[1].coord) == 4
    assert Matrix.getAtCoordinate(matrix, ancestors[2].coord) == 2
    assert Matrix.getAtCoordinate(matrix, ancestors[3].coord) == 3
    assert Matrix.getAtCoordinate(matrix, ancestors[4].coord) == 5
    assert Matrix.getAtCoordinate(matrix, ancestors[5].coord) == 7
    assert Matrix.getAtCoordinate(matrix, ancestors[6].coord) == 8
    assert Matrix.getAtCoordinate(matrix, ancestors[7].coord) == 6



def test_count_nodes_christmas_tree_BFS():
    """
    The path forms a sort of christmas tree.
    Like so:

    1     2    3
       /     \
    4     5    6
       \
    7     8    9
       /    \
    20   10   19
       \
    30   11   29
       /    \
    40   12   39

    """

    matrix = [
        [1,   2,  3],
        [4,   5,  6],
        [7,   8,  9],
        [20, 10,  19],
        [30, 11,  29],
        [40, 12,  39],
    ]

    # callback for the engine
    def getNextMoves(mt: MatrixTraverser, currNode: MatrixTree) -> List[Move]:
        return [
            Move.DIAGONAL_DOWN_LEFT,
            Move.DIAGONAL_DOWN_RIGHT
        ]

    startCoord = Coordinate(0, 1)

    matrixTraverser = MatrixTraverser(matrix, {
        "getNextMoves": getNextMoves
    })

    matrixTraverser.traverseMatrixBFS(startCoord)

    targetValue = 40
    (nodeFound, ancestors) = MatrixTree.findOneByValueFrom(matrixTraverser.matrixTree,
                                                           targetValue,
                                                           matrix)

    assert 5 == len(ancestors)

    # test nodes count
    assert 9 == MatrixTree.countNodesAt(ancestors[0])
    assert 7 == MatrixTree.countNodesAt(ancestors[1])
    assert 6 == MatrixTree.countNodesAt(ancestors[2])
    assert 4 == MatrixTree.countNodesAt(ancestors[3])
    assert 3 == MatrixTree.countNodesAt(ancestors[4])

    # test ancestor values
    assert Matrix.getAtCoordinate(matrix, ancestors[0].coord) == 2
    assert Matrix.getAtCoordinate(matrix, ancestors[1].coord) == 4
    assert Matrix.getAtCoordinate(matrix, ancestors[2].coord) == 8
    assert Matrix.getAtCoordinate(matrix, ancestors[3].coord) == 20
    assert Matrix.getAtCoordinate(matrix, ancestors[4].coord) == 11


