from src.components import Coordinate, Matrix, MatrixTree
from src.implementations.fibonacci_maze import makeFibonacciMaze

def test_one_path_exists():

    fibonacciMaze = makeFibonacciMaze([
        ["S",    13,  0,  "E"],
        [1,      8,   0,   34],
        [1,      5,   21,  13],
        [2,      3,   8,   8],
    ])

    startCoord = Coordinate(0, 0)

    fibonacciMaze.run(startCoord)

    (nodeFound, ancestorsFromValue) = MatrixTree.findOneByValueFrom(
        fibonacciMaze.matrixTree,
        "E",
        fibonacciMaze.matrix
    )

    ancestorsFromFound = MatrixTree.findAllAncestorsOf(nodeFound)

    ancestorsFromFoundUpToK = MatrixTree.findKAncestorsOf(nodeFound, 10)

    assert len(ancestorsFromValue) == len(ancestorsFromFound)
    assert len(ancestorsFromValue) == len(ancestorsFromFoundUpToK)

    for i in range(len(ancestorsFromValue)):
        # assert the ancestors found starting from the value,
        # are the same as the ancestors you get when
        # you start from a node you already know
        assert ancestorsFromValue[i] == ancestorsFromFound[i]
        assert ancestorsFromValue[i] == ancestorsFromFoundUpToK[i]

        ancestor  = ancestorsFromValue[i]
        #
        # print(
        #     Matrix.getAtCoordinate(
        #         fibonacciMaze.matrix,
        #         ancestor.coord
        #     )
        # )


