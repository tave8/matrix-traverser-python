from typing import List

from src.components import Coordinate, Matrix, MatrixTree, Move
from src.core.MatrixTraverser import MatrixTraverser
from src.core.PatternTraverser import PatternTraverser
from src.implementations.line_pattern import makeLinePattern
from src.implementations.t_shape_pattern import makeTShapePattern
from src.implementations.zigzag_pattern import makeZigzagPattern
from src.implementations.incremental_path_maze import makeIncrementalPathMaze
from src.core.MatrixTraverser import MatrixTraverser




def test_count_nodes_in_incremental_path_maze():

    matrix = [
        ["S",    1,    2,     3],
        [8,      6,    5,     4],
        [9,      7,   10,     9],
        [10,    11,   12,    "E"]
    ]


    startCoord = Coordinate(Matrix.getFirstRow(), Matrix.getFirstCol())

    incrementalPathMaze = makeIncrementalPathMaze(matrix)

    incrementalPathMaze.run(startCoord)

    targetValue = "E"
    (nodeFound, ancestors) = MatrixTree.findOneByValueFrom(incrementalPathMaze.matrixTree,
                                                           targetValue,
                                                           matrix)


    # how many ancestors does the end have?
    assert 13 == len(ancestors)

    assert 14 == MatrixTree.countNodesAt(incrementalPathMaze.matrixTree)

    assert 1 == MatrixTree.countNodesAt(nodeFound)
    assert 2 == MatrixTree.countNodesAt(ancestors[-1])
    assert 3 == MatrixTree.countNodesAt(ancestors[-2])
    assert 4 == MatrixTree.countNodesAt(ancestors[-3])
    assert 5 == MatrixTree.countNodesAt(ancestors[-4])
    assert 6 == MatrixTree.countNodesAt(ancestors[-5])
    assert 7 == MatrixTree.countNodesAt(ancestors[-6])
    assert 8 == MatrixTree.countNodesAt(ancestors[-7])
    assert 9 == MatrixTree.countNodesAt(ancestors[-8])
    assert 10 == MatrixTree.countNodesAt(ancestors[-9])
    assert 11 == MatrixTree.countNodesAt(ancestors[-10])
    assert 12 == MatrixTree.countNodesAt(ancestors[-11])
    assert 13 == MatrixTree.countNodesAt(ancestors[-12])
    assert 14 == MatrixTree.countNodesAt(ancestors[-13])

    assert 0 == MatrixTree.countNodesBelow(nodeFound)
    assert 1 == MatrixTree.countNodesBelow(ancestors[-1])
    assert 2 == MatrixTree.countNodesBelow(ancestors[-2])
    assert 3 == MatrixTree.countNodesBelow(ancestors[-3])
    assert 4 == MatrixTree.countNodesBelow(ancestors[-4])
    assert 5 == MatrixTree.countNodesBelow(ancestors[-5])
    assert 6 == MatrixTree.countNodesBelow(ancestors[-6])
    assert 7 == MatrixTree.countNodesBelow(ancestors[-7])
    assert 8 == MatrixTree.countNodesBelow(ancestors[-8])
    assert 9 == MatrixTree.countNodesBelow(ancestors[-9])
    assert 10 == MatrixTree.countNodesBelow(ancestors[-10])
    assert 11 == MatrixTree.countNodesBelow(ancestors[-11])
    assert 12 == MatrixTree.countNodesBelow(ancestors[-12])
    assert 13 == MatrixTree.countNodesBelow(ancestors[-13])







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

    assert 8 == MatrixTree.countNodesBelow(ancestors[0])
    assert 6 == MatrixTree.countNodesBelow(ancestors[1])
    assert 5 == MatrixTree.countNodesBelow(ancestors[2])
    assert 3 == MatrixTree.countNodesBelow(ancestors[3])
    assert 2 == MatrixTree.countNodesBelow(ancestors[4])

    # test ancestor values
    assert Matrix.getAtCoordinate(matrix, ancestors[0].coord) == 2
    assert Matrix.getAtCoordinate(matrix, ancestors[1].coord) == 4
    assert Matrix.getAtCoordinate(matrix, ancestors[2].coord) == 8
    assert Matrix.getAtCoordinate(matrix, ancestors[3].coord) == 20
    assert Matrix.getAtCoordinate(matrix, ancestors[4].coord) == 11


