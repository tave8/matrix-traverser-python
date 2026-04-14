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
               prevMove: Move,
               currNode: MatrixTree) -> bool:
    nextNum = Matrix.getAtCoordinate(mt.matrix, desiredCoord)  # type: ignore
    currNum = Matrix.getAtCoordinate(mt.matrix, currCoord)  # type: ignore

    # why do i use the k ancestors logic instead
    # of simply accessing the previous coordinate?
    # simply to experiment with a more powerful and
    # generic tool, which is the "k ancestors of"
    ancestors = MatrixTree.findKAncestorsOf(currNode, 1)

    prevNum = 0
    for ancestor in ancestors:
        # all ancestors except root
        if not ancestor.coord.isStart:
            prevNum += Matrix.getAtCoordinate(mt.matrix, ancestor.coord)

    # this is the fibonacci sequence
    # this cell can move to the desired/next coordinate
    # only if this condition is met
    cond = nextNum == currNum + prevNum # type: ignore
    if cond:
        # print(Matrix.getAtCoordinate(mt.matrix, currCoord), Matrix.getAtCoordinate(mt.matrix, currNode.coord), nextNum)
        # print(ancestors)
        return True

    return False




# callback specific for this maze problem
def _canMoveToOnStart(mt: MazeTraverser,
                      desiredCoord: Coordinate,
                      prevCoord: Coordinate,
                      currCoord: Coordinate,
                      prevMove: Move,
                      currNode: MatrixTree) -> bool:

    return Matrix.getAtCoordinate(mt.matrix, desiredCoord) == 1

