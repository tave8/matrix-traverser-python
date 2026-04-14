from src.components import Coordinate, Matrix, Move
from src.implementations.incremental_path_maze import makeIncrementalPathMaze
from src.core.MazeTraverser import MazeTraverser


class DataToTest:
    def __init__(self, 
                 mazeTraverser: MazeTraverser, 
                 movesHistory: list[dict]) -> None:
        
        self.mazeTraverser = mazeTraverser
        self.movesHistory = movesHistory



def makeAndRunIncrementalPathMaze(matrix: list[list], 
                                    startCoord: Coordinate) -> DataToTest:

    mazeTraverser = makeIncrementalPathMaze(matrix)

    mazeTraverser.run(startCoord)

    movesHistory = mazeTraverser.getMovesHistory()

    return DataToTest(
         mazeTraverser, 
         movesHistory
    )
