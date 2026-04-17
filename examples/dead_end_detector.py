from src.core.MazeTraverser import MazeTraverser
from src.components import Coordinate, Move, Matrix, MatrixTree, MazeTerminationPolicy

matrix = [
    ["S", 1,  2],
    [ 4,  6,  3],
    [ 7,  8,  4],
    [ 7,  8, "E"],
]


# callback specific for this maze problem
def canMoveTo(mt: MazeTraverser,
               currNode: MatrixTree,
               desiredCoord: Coordinate,
               desiredMove: Move) -> bool:

    nextNum = Matrix.getAtCoordinate(mt.matrix, desiredCoord)
    currNum = Matrix.getAtCoordinate(mt.matrix, currNode.coord)

    # this cell can move to the desired/next coordinate
    # only if this condition is met
    return nextNum == currNum + 1  # type: ignore


# callback specific for this maze problem
def canMoveToOnStart(mt: MazeTraverser,
                      currNode: MatrixTree,
                      desiredCoord: Coordinate,
                      desiredMove: Move) -> bool:
    return Matrix.getAtCoordinate(mt.matrix, desiredCoord) == 1


def onEndFound(mt: MazeTraverser,
               currNode: MatrixTree) -> None:

    # print(currNode.getAncestorCellValues(mt.matrix))
    #
    print(currNode.getCellValue(mt.matrix))
    pass

maze = MazeTraverser(
    matrix=matrix,
    canMoveToCallback=canMoveTo,
    canMoveToOnStartCallback=canMoveToOnStart,
    mazeTerminationPolicy=MazeTerminationPolicy.ON_END_FOUND_CONTINUE,
    onEndFoundCallback=onEndFound
)


maze.run(Coordinate(0,0))

# maze.endWasFound()





