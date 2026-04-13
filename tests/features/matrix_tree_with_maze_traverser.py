from src.components import Coordinate, MatrixTree, Matrix
from src.implementations.incremental_path import makeIncrementalPathMaze

incrementalPathMaze = makeIncrementalPathMaze([
   ["S", 1,  2,  3],
   [1,   1,  6,  7],
   [2,   5,  3,  8],
   [3,   4,  4,  "E"]
])

incrementalPathMaze.run(
    Coordinate(0,0)
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