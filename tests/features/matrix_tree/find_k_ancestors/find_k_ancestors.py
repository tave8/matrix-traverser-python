from src.components import Coordinate, Matrix, MatrixTree
from src.implementations.incremental_path import makeIncrementalPathMaze


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

