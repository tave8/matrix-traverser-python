
from src.components import Coordinate, Matrix, Move, MatrixTree
from src.implementations.spiral_pattern import makeSpiralPattern


spiralPattern = makeSpiralPattern([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
])

spiralPattern.run(
    Coordinate(
        Matrix.getFirstRow(),
        Matrix.getFirstCol(),
    )
)



targetValue = 5

(nodeFound, ancestorsFromValue) = MatrixTree.findOneByValueFrom(
    spiralPattern.matrixTree,
    targetValue,
    spiralPattern.matrix
)

if isinstance(nodeFound, MatrixTree):
    print("NODE FOUND!")
    print("PATH:")
    for i in range(len(ancestorsFromValue)):

        ancestor = ancestorsFromValue[i]

        print(
            Matrix.getAtCoordinate(
                spiralPattern.matrix,
                ancestor.coord
            )
        )
else:
    print("NODE NOT FOUND!")