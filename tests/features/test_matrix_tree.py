from src.components import Coordinate, MatrixTree, Matrix
from src.implementations.incremental_path import makeIncrementalPathMaze



def test_matrix_tree_correct_path_exists():

    matrix = [
            [  2,  22,   4,    3,     4,    5,  8],
            [  1,  20,   5,    2,     13,   12,  2],
            [  8,  7,    6,    1,     11,   7,  9],
            [  3,  18,   3,    "S",    7,   8,  10],
            [  4,  "E",  9,     1,     6,   9,  11],
            [  7,   8,   4,     2,    11,   2,  12],
            [  6,   5,   3,     2,     1,   5,  12],
    ]

    incrementalPathMaze = makeIncrementalPathMaze(matrix)

    incrementalPathMaze.run(
    Coordinate(
            Matrix.getMiddleRow(matrix),
            Matrix.getMiddleCol(matrix)
        )
    )


    (nodeFound, ancestors) = MatrixTree.findOneWhereValueStartingFrom(incrementalPathMaze.matrixTree, "E", incrementalPathMaze.matrix)

    # print( 
    #     Matrix.getAtCoordinate(incrementalPathMaze.matrix, nodeFound.currCoord) if nodeFound else None
    # )

    # the first ancestor must always be root and have value S
    assert ancestors[0].isRoot 
    assert Matrix.getAtCoordinate(matrix, ancestors[0].currCoord) == "S" 

    # last node must not have the value we are searching for 
    assert Matrix.getAtCoordinate(matrix, ancestors[-1].currCoord) != "E"

    # every value, apart from the root which has value S, to the last ancestor, 
    # must have +1 from previous value
    prevAncestor = ancestors[1]
    for currAncestor in ancestors[2:]:
        prevValue = Matrix.getAtCoordinate(matrix, prevAncestor.currCoord)
        currValue = Matrix.getAtCoordinate(matrix, currAncestor.currCoord)
        # they must be integer types
        assert isinstance(prevValue, int)
        assert isinstance(currValue, int)
        assert currValue == prevValue + 1
        # curr ancestor will be prev ancestor 
        # in the next loop round
        prevAncestor = currAncestor