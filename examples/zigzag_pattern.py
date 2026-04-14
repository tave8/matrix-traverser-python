
from src.components import Coordinate, Matrix, Move, MatrixTree
from src.implementations.zigzag_pattern import makeZigzagPattern


zigzagPattern = makeZigzagPattern([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
])

zigzagPattern.run(
    Coordinate(
        Matrix.getFirstRow(),
        Matrix.getFirstCol(),
    )
)



targetValue = 9

(nodeFound, ancestorsFromValue) = MatrixTree.findOneByValueFrom(
    zigzagPattern.matrixTree,
    targetValue,
    zigzagPattern.matrix
)

if isinstance(nodeFound, MatrixTree):
    print("NODE FOUND!")
    print("PATH:")
    for i in range(len(ancestorsFromValue)):

        ancestor = ancestorsFromValue[i]

        print(
            Matrix.getAtCoordinate(
                zigzagPattern.matrix,
                ancestor.coord
            )
        )
else:
    print("NODE NOT FOUND!")