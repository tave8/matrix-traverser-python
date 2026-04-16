from typing import List

from src.components import Coordinate, Matrix, MatrixTree, Move
from src.core.MatrixTraverser import MatrixTraverser
from src.core.PatternTraverser import PatternTraverser
from src.implementations.line_pattern import makeLinePattern
from src.implementations.t_shape_pattern import makeTShapePattern


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

    (totalNodesCount, _nodesStats) = MatrixTree.countNodesFrom(linePattern.matrixTree)

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

    (totalNodesCount, _nodesStats) = MatrixTree.countNodesFrom(tShapePattern.matrixTree)

    # the ancestors are 5:
    # ancestors of 15:   1 -> 2 -> 3 -> 7 -> 11
    assert len(ancestors) == 5

    assert totalNodesCount == 8

    assert Matrix.getAtCoordinate(matrix, ancestors[0].coord) == 1
    assert Matrix.getAtCoordinate(matrix, ancestors[1].coord) == 2
    assert Matrix.getAtCoordinate(matrix, ancestors[2].coord) == 3
    assert Matrix.getAtCoordinate(matrix, ancestors[3].coord) == 7
    assert Matrix.getAtCoordinate(matrix, ancestors[4].coord) == 11
