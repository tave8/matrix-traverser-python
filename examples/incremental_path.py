from src.components import Coordinate, Matrix
from src.implementations.incremental_path import makeIncrementalPathMaze

incrementalPathMaze = makeIncrementalPathMaze([
    ["S", 1, 1, "E"],
    [1, 1, 1, 1],
    [1, 1, 1, 1],
    [1, 1, 1, 1],
])

incrementalPathMaze.run(Coordinate(
    0,0
))

for cellInfo in incrementalPathMaze.getMovesHistory():
    print(cellInfo)
