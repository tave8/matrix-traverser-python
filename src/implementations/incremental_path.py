"""
Find the path where each cell must be exactly +1 from the previous,
and you also have start and end.

Properties:
- the start must always be start
- for each pair of move from a cell to a cell [prevCell, currCell],
    the distance of the move is 1 cell
- for each pair of move from a cell to a cell [prevCell, currCell],
    the value of currCell = prevCell value + 1
- the end might not exist
"""

from src.components import Coordinate, Move, Matrix
from src.MazeTraverser import MazeTraverser



def makeIncrementalPathMaze(matrix: list[list]) -> MazeTraverser:
    """
    Makes the Incremental Path Maze, an implementation of the 
    Maze Traverser.

    What it does:
    - search whether a path from start to end exists, with any 
    number of candidate paths for each cell, where the next value 
    must be the previous value + 1.

    Example:  

    ```
    S - 1   5    3
          \\  /  |
    1   1   2    4
               /  
    7   6   5    6
          / 
    7   6   5    6
        |
    8   7 - 8    3
               \\  
    8   5   2    E
    ```

    Rules:
    - start value is "S"
    - end value is "E"
    - all values except start and end must be number types
    - from the start, the next value is exactly 1
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
            
        nextNum = Matrix.getAtCoordinate(mt.matrix, desiredCoord) # type: ignore
        currNum = Matrix.getAtCoordinate(mt.matrix, currCoord) # type: ignore

        # this cell can move to the desired/next coordinate 
        # only if this condition is met
        return nextNum == currNum + 1 # type: ignore


# callback specific for this maze problem
def _canMoveToOnStart(mt: MazeTraverser, 
                    desiredCoord: Coordinate, 
                    prevCoord: Coordinate, 
                    currCoord: Coordinate,
                    prevMove: Move) -> bool:
        
    return Matrix.getAtCoordinate(mt.matrix, desiredCoord) == 1

