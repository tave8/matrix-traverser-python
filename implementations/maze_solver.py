"""
Find the path.

"""

from inspect import isfunction
from collections.abc import Callable
from src.MatrixTraverser import Matrix, MatrixTraverser, Coordinate, Move, StateManager
from src.exceptions.ExpectedUserCallbackError import ExpectedUserCallbackError


class MazeTraverser(MatrixTraverser):
    """
    The Maze Traverser allows you to easily create 
    custom maze-solving algorithms in a few lines of code, 
    so you can focus on the core maze logic.

    It's based on the Matrix Traverser Engine.
    """

    def __init__(self, 
                 matrix: list[list], 
                 canMoveToCallback: Callable[[MazeTraverser, Coordinate, Coordinate, Coordinate, Move], bool],
                 userState: dict = {},
                 startName = "S",
                 endName = "E") -> None:
        """
        canMoveCallback is the user-defined, maze-specific callback.
        It will be used in the specific steps of the maze traversal,
        where the user will be able to pilot the traversal.
        """
        
        # configure the Matrix Traverser Engine to use 
        # these callbacks. by callbacks we assume
        # it's one callback (canMoveTo) which has been proven
        # to solve maze-related problems
        mazeCallbackMap = MazeTraverser._getMazeCallbackMap(self)
        # print(mazeCallbackMap)

        # call MatrixTraverser constructor
        super().__init__(
            matrix,
            mazeCallbackMap,
            userState
        )

        # callback must be a function
        if not isfunction(canMoveToCallback):
            raise ExpectedUserCallbackError(canMoveToCallback)

        # user-defined, maze-specific callback
        # in this callback, the user will define the exact logic
        # of how they want their maze logic to play out
        self.canMoveToCallback = canMoveToCallback
        
        self.startName = startName
        self.endName = endName


    def run(self, startCoord: Coordinate) -> None:
        """
        Run the maze.
        """
        self.traverseMatrix(startCoord)


    @staticmethod
    def _canMoveTo(mazeTraverser: MazeTraverser) -> Callable[[MatrixTraverser, Coordinate, Coordinate, Coordinate, Move], bool]:
        """
        This is the Maze Traverser internal callback that gets called
        directly by the Matrix Traverser engine, and includes the 
        default/boilerplate maze logic, as well as user-defined logic.
        
        This callback helps reduce boilerplate and allows abstraction
        from the user perspective. Of course, being only a wrapper,
        it does not run the actual matrix engine. This is one of the many 
        callbacks that the Matrix Traverser engine makes available.

        This callback therefore
        lets the user define only the exact
        logic that they want, without worrying about additional
        maze logic.

        NOTE: the mechanism of function closure is being used. 
        this is because I want the actual Maze Traverser Instance.
        """


    
        def _canMoveToWrapper(_matrixTraverser: MatrixTraverser, 
                                desiredCoord: Coordinate, 
                                prevCoord: Coordinate, 
                                currCoord: Coordinate,
                                prevMove: Move) -> bool:
            """
            Finally, this is the actual callback that the Matrix Traversal Engine
            will call directly. Therefore its signature must match exactly what the
            engine will expect.
            """

            # from the start, you can only move to 
            # a cell with value 1
            if currCoord.isStart:
                # return MazeTraverser._canMoveToOnStart(mazeTraverser)
            
                return Matrix.getAtCoordinate(mazeTraverser.matrix, desiredCoord) == 1

            # the cells around S might try to go to S, but they must not
            # because of how the engine works and the nature of its recursive calls,
            # even though the start is already visited,
            # some start paths might still be asking if i can move to start
            if Matrix.getAtCoordinate(mazeTraverser.matrix, desiredCoord) == mazeTraverser.startName:
                return False
            
            # if the next move is the end, you can move
            if Matrix.getAtCoordinate(mazeTraverser.matrix, desiredCoord) == mazeTraverser.endName:
                return True
            
            # if the curr coordinate is the end itself,
            # end the algorithm
            if Matrix.getAtCoordinate(mazeTraverser.matrix, currCoord) == mazeTraverser.endName:
                # end the algorithm at 
                StateManager.setWasEnded(mazeTraverser, True)
                return False

            # user-defined canMoveToCallback. this is where the user
            # has full control over traversal logic and where the actual 
            # magic happens. the previous steps
            # in this callback where just boilerplate code to handle
            # start, end and edge cases
            return mazeTraverser.canMoveToCallback(mazeTraverser, 
                                                    desiredCoord, 
                                                    prevCoord, 
                                                    currCoord, 
                                                    prevMove)
        
        return _canMoveToWrapper 

    

    # def getStartName():
    #     return "S"

    # def getEndName():
    #     return "E"

    # def getFirstNextValueAtStart():
    #     return "1"


    @staticmethod
    def _getMazeCallbackMap(mazeTraverser: MazeTraverser) -> dict[str, Callable]:
        """
        Returns the callback map that will be used by the 
        Matrix Traverser. The maze algorithm therefore uses 
        Matrix Traverser as the engine, reduces boilerplate
        code and standardizes the maze algorithm. 
        """

        return {
            # this is the final callback that will be 
            # fed to the Matrix Traverser Engine, and
            # includes the default/boilerplate maze logic, 
            # as well as user-specific logic
            "canMoveTo": MazeTraverser._canMoveTo(mazeTraverser)
        }
    


# user-defined cell movement
def canMoveTo(mt: MazeTraverser, 
                desiredCoord: Coordinate, 
                prevCoord: Coordinate, 
                currCoord: Coordinate,
                prevMove: Move) -> bool:
            
        nextNum = int(Matrix.getAtCoordinate(mt.matrix, desiredCoord)) # type: ignore
        currNum = int(Matrix.getAtCoordinate(mt.matrix, currCoord)) # type: ignore

        # this cell can move to the desired/next coordinate 
        # only if this condition is met
        return nextNum == currNum + 1
        # return False



def canMoveToOnStart(mt: MazeTraverser, 
                    desiredCoord: Coordinate, 
                    prevCoord: Coordinate, 
                    currCoord: Coordinate,
                    prevMove: Move) -> bool:
        
    return Matrix.getAtCoordinate(mt.matrix, desiredCoord) == 1
                


# matrix = [
#         ["S",  "1",  "2",   "3",   "4",  "5"],
#         ["1",  "1",  "2",   "4",   "5",  "6"],
#         ["2",  "2",  "4",   "5",   "6",  "7"],
#         ["3",  "4",  "3",   "5",   "7",  "8"],
#         ["4",  "5",  "6",   "8",   "6",  "9"],
#         ["5",  "8",  "11",  "9",   "11", "2"],
#         ["6",  "7",  "10",  "10",  "8",  "E"]
# ]

matrix = [
        ["S",  1,  2,  3,  4,  5],
        [ 1,   1,  2,  4,  5,  6],
        [ 2,   2,  4,  5,  6,  7],
        [ 3,   4,  3,  5,  7,  8],
        [ 4,   5,  6,  8,  6,  9],
        [ 5,   8, 11,  9, 11,  2],
        [ 6,   7, 10, 10,  8, "E"]
]


mazeTraverser = MazeTraverser(matrix, canMoveTo)


startCoord = Coordinate(
    Matrix.getFirstRow(),
    Matrix.getFirstCol()
)

mazeTraverser.run(startCoord)

for cellInfo in mazeTraverser.stateManager.state["movesFromTo"]:
    print(cellInfo)