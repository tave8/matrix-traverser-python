from src.components import Coordinate
from src.core.MatrixTraverser import MatrixTraverser

matrixTraverser = MatrixTraverser(
    [
        [1, 2]
    ]
)

matrixTraverser.traverseMatrix(
    Coordinate(0,0)
)

# print(matrixTraverser.getMovesHistory())
# print(matrixTraverser.matrixTree)
# matrixTraverser.matrixTree.findAncestorsOf(
#     matrixTraverser.matrixTree
# )