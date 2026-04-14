
from src.components import Coordinate, Matrix, Move
from src.implementations.line import makeLinePattern


linePattern = makeLinePattern([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
], Move.DOWN)

linePattern.run(
    Coordinate(
        Matrix.getFirstRow(),
        Matrix.getFirstCol(),
    )
)

# for cellInfo in linePattern.getMovesHistory():
#     print(cellInfo)


# print(
#     MatrixTree.findOneByValueFrom(
#         linePattern.matrixTree,
#         7,
#         linePattern.matrix
#     )
# )
