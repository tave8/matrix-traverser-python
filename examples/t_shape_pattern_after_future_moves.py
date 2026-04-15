from src.core.PatternTraverser import PatternTraverser
from src.components import Coordinate, Matrix, Move, MatrixTree
from src.implementations.t_shape_pattern import makeTShapePattern


def afterAllFutureMovesCallback(pt: PatternTraverser, currNode: MatrixTree) -> None:
    cellValue = Matrix.getAtCoordinate(pt.matrix, currNode.coord)
    print(cellValue)


tShapePattern = makeTShapePattern([
    [1,   2,  3, 4, 5],
    [6,   7,  8, 9, 10],
    [11, 12, 13, 14, 15],
    [16, 17, 18, 19, 20],
    [21, 22, 23, 24, 25],
], afterAllFutureMovesCallback)

tShapePattern.run(
    Coordinate(
        Matrix.getFirstRow(),
        Matrix.getFirstCol(),
    )
)



targetValue = 23

(nodeFound, ancestorsFromValue) = MatrixTree.findOneByValueFrom(
    tShapePattern.matrixTree,
    targetValue,
    tShapePattern.matrix
)

# if isinstance(nodeFound, MatrixTree):
#     print("NODE FOUND!")
#     print("PATH:")
#     for i in range(len(ancestorsFromValue)):
#
#         ancestor = ancestorsFromValue[i]
#
#         print(
#             Matrix.getAtCoordinate(
#                 tShapePattern.matrix,
#                 ancestor.coord
#             )
#         )
# else:
#     print("NODE NOT FOUND!")