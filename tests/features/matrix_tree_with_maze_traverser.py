from src.components import Coordinate, MatrixTree, Matrix
from src.implementations.incremental_path import makeIncrementalPathMaze

incrementalPathMaze = makeIncrementalPathMaze([
   ["S", 0,  0,  0],
   [0,   1,  0,  0],
   [0,   0,  2,  0],
   [0,   0,  0,  "E"]
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

print( 
    Matrix.getAtCoordinate(incrementalPathMaze.matrix, nodeFound.currCoord) if nodeFound else None
)

# print(ancestors)