"""
Fibonacci Maze.

"""

from src.components import Coordinate, Move, Matrix, MatrixTree
from src.core.MazeTraverser import MazeTraverser


def makeFibonacciMaze(matrix: list[list]) -> MazeTraverser:
    """
    Make the Fibonacci Maze.

    Find the path where each cell value must be
    the sum of the previous two cells,
    with multiple candidate paths at each cell.


    # Example

    ```
    S - 1    5    2
          \\   /  |
    34  21   1    3
               /
    21  13   5    55
          /
    13  8   21    34
        |
    21  13 - 21   3
               \\
    55  34   2    E
    ```

    # Rules
    - Start is S
    - The next value from start is 1
    - For every other cell after 1, whose number of ancestors is less than 2,
      the missing ancestor is simply calculated as 0. In practice,
      this should only occur to the next number of 1, which must be another 1.
      Therefore, after two 1's, we are certain that cells will have
      2 ancestors.

    """

    mazeTraverser = MazeTraverser(
        matrix,
        canMoveToCallback=_canMoveTo,
        canMoveToOnStartCallback=_canMoveToOnStart
    )

    return mazeTraverser


# callback specific for this maze problem
def _canMoveTo(mt: MazeTraverser,
               desiredCoord: Coordinate,
               prevCoord: Coordinate,
               currCoord: Coordinate,
               prevMove: Move) -> bool:
    # nextNum = Matrix.getAtCoordinate(mt.matrix, desiredCoord)  # type: ignore
    # currNum = Matrix.getAtCoordinate(mt.matrix, currCoord)  # type: ignore

    # FIX

    # this cell can move to the desired/next coordinate
    # only if this condition is met
    return nextNum == prevNum + prevPrevNum  # type: ignore


# callback specific for this maze problem
def _canMoveToOnStart(mt: MazeTraverser,
                      desiredCoord: Coordinate,
                      prevCoord: Coordinate,
                      currCoord: Coordinate,
                      prevMove: Move) -> bool:

    return Matrix.getAtCoordinate(mt.matrix, desiredCoord) == 1

