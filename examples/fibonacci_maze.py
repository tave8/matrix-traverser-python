from src.components import Coordinate, Matrix, MatrixTree
from src.implementations.fibonacci_maze import makeFibonacciMaze

fibonacciMaze = makeFibonacciMaze([
        ["S", 1, 4, 2, 7],
        [1, 2, 3, 5, 11],
        [9, 3, 5, 8, 13],
        [2, 5, 8, 13, 4],
        [3, 8, 13, 21, 6],
        [5, 13, 21, 34, 22],
        [8, 21, 34, 55, 35],
        [13, 34, 55, 89, 90],
        [21, 55, 89, 144, 1],
        [34, 89, 144, 233, 2],
        [55, 144, 233, 377, "E"]
])

startCoord = Coordinate(0, 0)

fibonacciMaze.run(startCoord)

targetValue = "E"

(nodeFound, ancestorsFromValue) = MatrixTree.findOneByValueFrom(
    fibonacciMaze.matrixTree,
    targetValue,
    fibonacciMaze.matrix
)

if isinstance(nodeFound, MatrixTree):
    print("NODE FOUND!")
    print("PATH:")
    for i in range(len(ancestorsFromValue)):

        ancestor = ancestorsFromValue[i]

        print(
            Matrix.getAtCoordinate(
                fibonacciMaze.matrix,
                ancestor.coord
            )
        )
else:
    print("NODE NOT FOUND!")



