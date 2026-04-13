from src.components import Coordinate, MatrixTree, Matrix
from src.implementations.incremental_path import makeIncrementalPathMaze

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

# print(
#     incrementalPathMaze.getMovesHistory()
# )



# print(matrixTraverser.getMovesHistory())
# print(matrixTraverser.matrixTree)

# incrementalPathMaze.matrixTree.findAncestorsOf(
#     incrementalPathMaze.matrixTree
# )

(nodeFound, ancestors) = MatrixTree.findOneWhereValue(incrementalPathMaze.matrixTree, "E", incrementalPathMaze.matrix)

# print( 
#     Matrix.getAtCoordinate(incrementalPathMaze.matrix, nodeFound.currCoord) if nodeFound else None
# )

for ancestor in ancestors:
    cellValue = Matrix.getAtCoordinate(incrementalPathMaze.matrix, ancestor.currCoord)
    msg = f"value: {cellValue}, {ancestor.prevCoord} | {ancestor.currCoord}"
    print(msg)