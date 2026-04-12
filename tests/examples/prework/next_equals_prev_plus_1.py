from src.components import Coordinate, Matrix, Move
from src.MazeTraverser import MazeTraverser


class DataToTest:
    def __init__(self, 
                 mazeTraverser: MazeTraverser, 
                 movesHistory: list[dict]) -> None:
        
        self.mazeTraverser = mazeTraverser
        self.movesHistory = movesHistory



def makeAndRunMazeTraverser(matrix: list[list], 
                            startCoord: Coordinate) -> DataToTest:

    mazeTraverser = MazeTraverser(
        matrix, 
        canMoveToCallback=canMoveTo, 
        canMoveToOnStartCallback=canMoveToOnStart
    )

    mazeTraverser.run(startCoord)

    movesHistory = mazeTraverser.getMovesHistory()

    return DataToTest(
         mazeTraverser, 
         movesHistory
    )


# callback specific for this maze
def canMoveTo(mt: MazeTraverser, 
                desiredCoord: Coordinate, 
                prevCoord: Coordinate, 
                currCoord: Coordinate,
                prevMove: Move) -> bool:
            
        nextNum = Matrix.getAtCoordinate(mt.matrix, desiredCoord) # type: ignore
        currNum = Matrix.getAtCoordinate(mt.matrix, currCoord) # type: ignore

        # this cell can move to the desired/next coordinate 
        # only if this condition is met
        return nextNum == currNum + 1 # type: ignore


# callback specific for this maze
def canMoveToOnStart(mt: MazeTraverser, 
                    desiredCoord: Coordinate, 
                    prevCoord: Coordinate, 
                    currCoord: Coordinate,
                    prevMove: Move) -> bool:
        
    return Matrix.getAtCoordinate(mt.matrix, desiredCoord) == 1