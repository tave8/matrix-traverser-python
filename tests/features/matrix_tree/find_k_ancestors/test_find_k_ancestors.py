from src.components import Coordinate, Matrix, MatrixTree
from src.implementations.incremental_path_maze import makeIncrementalPathMaze
from src.implementations.zigzag_pattern import makeZigzagPattern
from tests.features.matrix_tree.find_k_ancestors.prep.helpers import makeAndRunTShapePattern


def test_on_t_shape():

    matrix = [
        [ 1,    2,  3],
        [ 4,    4,  6],
        [ 7,    5,  3],
        [ 6,    6,  3],
        [ 5,    7,  3],
        [ 9,    8,  3],
    ]

    startCoord = Coordinate(
        Matrix.getFirstRow(),
        Matrix.getFirstCol()
    )

    dataToTest = makeAndRunTShapePattern(matrix, startCoord)

    (nodeFound, ancestorsFromValue) = MatrixTree.findOneByValueFrom(
       dataToTest.patternTraverser.matrixTree,
        8,
        matrix
    )

    ancestorsFromFound = MatrixTree.findAllAncestorsOf(nodeFound)

    ancestorsFromFoundUpToK = MatrixTree.findKAncestorsOf(nodeFound, 5)

    assert len(ancestorsFromValue) == 6
    assert len(ancestorsFromFound) == 6
    assert len(ancestorsFromFoundUpToK) == 5






def test_ancestors_of_node_by_value_same_k_ancestors():

    # path:
    #   S -> 1 -> 2 -> 3 -> 4 -> 5 -> E
    # ancestors from E:
    #   S -> 1 -> 2 -> 3 -> 4 -> 5
    matrix = [
        ["S",   1,  3],
        [ 4,    2,  6],
        [ 7,    8,  3],
        [ 6,    4,  3],
        [ 5,    8,  3],
        ["E",   8,  3],
    ]

    startCoord = Coordinate(
        Matrix.getFirstRow(),
        Matrix.getFirstCol()
    )

    maze = makeIncrementalPathMaze(matrix)

    maze.run(startCoord)

    # find the ancestors of a node, given the value of the node
    # this will give us back its ancestors as well
    (nodeFound, ancestorsFromValue) = MatrixTree.findOneByValueFrom(
       maze.matrixTree,
        "E",
        matrix
    )

    # given the node we've just found (which exists)
    # find all its ancestors
    ancestorsFromFound = MatrixTree.findAllAncestorsOf(nodeFound)

    # now get exactly the 6 ancestors (because we know they are 6)
    # using the method that gets up to k ancestors of a node
    ancestorsFromFoundUpToK = MatrixTree.findKAncestorsOf(nodeFound, 6)


    # print(nodeFound)
    #

    assert len(ancestorsFromValue) == len(ancestorsFromFound)
    assert len(ancestorsFromValue) == len(ancestorsFromFoundUpToK)

    # test whether they are exactly the same nodes in memory (pointers)
    for i in range(len(ancestorsFromValue)):
        # assert the ancestors found starting from the value,
        # are the same as the ancestors you get when
        # you start from a node you already know
        assert ancestorsFromValue[i] == ancestorsFromFound[i]
        assert ancestorsFromValue[i] == ancestorsFromFoundUpToK[i]


    # for ancestor in ancestorsFromFound:
    #     ancestorValue = Matrix.getAtCoordinate(matrix, ancestor.coord)
    #     print(ancestorValue)
    #
    # print()
    #
    # for ancestor in ancestorsFromFoundUpToK:
    #     ancestorValue = Matrix.getAtCoordinate(matrix, ancestor.coord)
    #     print(ancestorValue)



def test_on_zigzag():

    matrix = [
        [ 1,    2,   6],
        [ 3,    5,   7],
        [ 4,    8,  12],
        [ 9,   11,  13],
        [10,   14,  17],
        [15,   16,  18],
    ]

    startCoord = Coordinate(
        Matrix.getFirstRow(),
        Matrix.getFirstCol()
    )

    zigzag = makeZigzagPattern(matrix)

    zigzag.run(startCoord)

    # find the ancestors of a node, given the value of the node
    # this will give us back its ancestors as well
    (nodeFound, ancestorsFromValue) = MatrixTree.findOneByValueFrom(
       zigzag.matrixTree,
        18,
        matrix
    )

    ancestorsFromFound = MatrixTree.findAllAncestorsOf(nodeFound)
    ancestorsFromFoundUpToK = MatrixTree.findKAncestorsOf(nodeFound, 16)

    assert len(ancestorsFromFoundUpToK) == 16
    assert len(ancestorsFromValue) == 17
    assert len(ancestorsFromFound) == len(ancestorsFromValue)
    assert ancestorsFromFoundUpToK[0] == ancestorsFromValue[1]


