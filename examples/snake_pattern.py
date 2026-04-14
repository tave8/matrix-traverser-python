
from src.components import Coordinate, Matrix, Move, MatrixTree
from src.implementations.snake_pattern import makeSnakePattern


snakePattern = makeSnakePattern([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
])

snakePattern.run(
    Coordinate(
        Matrix.getFirstRow(),
        Matrix.getFirstCol(),
    )
)



targetValue = 9

(nodeFound, ancestorsFromValue) = MatrixTree.findOneByValueFrom(
    snakePattern.matrixTree,
    targetValue,
    snakePattern.matrix
)

if isinstance(nodeFound, MatrixTree):
    print("NODE FOUND!")
    print("PATH:")
    for i in range(len(ancestorsFromValue)):

        ancestor = ancestorsFromValue[i]

        print(
            Matrix.getAtCoordinate(
                snakePattern.matrix,
                ancestor.coord
            )
        )
else:
    print("NODE NOT FOUND!")