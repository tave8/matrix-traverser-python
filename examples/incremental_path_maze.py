from src.components import Coordinate, Matrix
from src.implementations.incremental_path_maze import makeIncrementalPathMaze

incrementalPathMaze = makeIncrementalPathMaze([
    [1,    1,  1, "E"],
    [1,    2,  1,  4],
    [1,    1,  3,  1],
    ["S",  1,  1,  1],
])

incrementalPathMaze.run(Coordinate(
    3,0
))

# for cellInfo in incrementalPathMaze.getMovesHistory():
#     print(cellInfo)
