"""
Maze Traverser, built on top of the Matrix Traverser Engine.

"""

from inspect import isfunction
from collections.abc import Callable
from src.core.MatrixTraverser import MatrixTraverser, StateManager
from src.components import Coordinate, Matrix, Move, MatrixTree
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
                 canMoveToCallback: Callable[[MazeTraverser, Coordinate, Coordinate, Coordinate, Move, MatrixTree], bool],
                 canMoveToOnStartCallback: Callable[[MazeTraverser, Coordinate, Coordinate, Coordinate, Move, MatrixTree], bool],
                 userState: dict = {},
                 startName = "S",
                 endName = "E") -> None:
        """
        canMoveCallback is the user-defined, maze-specific callback.
        It will be used in the specific steps of the maze traversal,
        where the user will be able to pilot the traversal.

        :param startName: the value of the start cell
        :param endName: the value of the end cell
        """
        
        # callback must be a function
        if not isfunction(canMoveToCallback):
            raise ExpectedUserCallbackError(canMoveToCallback)

            # callback must be a function
        if not isfunction(canMoveToOnStartCallback):
            raise ExpectedUserCallbackError(canMoveToOnStartCallback)

        # ************ START *********************
        # these logical block must go together

        # call MatrixTraverser constructor
        super().__init__(
            matrix,
            # because the Maze Traverser instance has not been
            # initialized yet, and we need it to find its callbacks,
            # we pass an empty dict for now. after this initialization,
            # you MUST immediately set the callback manager manually
            {},
            userState
        )
        # configure the Matrix Traverser Engine to use 
        # these callbacks. by callbacks we assume
        # it's one callback (canMoveTo) which has been proven
        # to solve maze-related problems
        mazeCallbackMap = MazeTraverser._getMazeCallbackMap(self)
        # print(mazeCallbackMap)
        self._setCallbackManager(mazeCallbackMap)

        # ********************END *************************

        # user-defined, maze-specific callback
        # in this callback, the user will define the exact logic
        # of how they want their maze logic to play out
        self.canMoveToCallback = canMoveToCallback
        self.canMoveToOnStartCallback = canMoveToOnStartCallback

        self.startName = startName
        self.endName = endName


    def run(self, startCoord: Coordinate) -> None:
        """
        Run the maze.
        """

        startNameOnInstantiation = self.startName
        startNameOnRun = Matrix.getAtCoordinate(self.matrix, startCoord)

        # add exception: if start coordinate value
        # does not match the user-provided or default
        # start name, throw exception
        if startNameOnInstantiation != startNameOnRun:
            raise Exception("error during run of maze traverser."
                            +f" mismatch between the initial start name of the maze "
                            +f"({startNameOnInstantiation}) and the value at the provided start"
                            +f" coordinate ({startNameOnRun})")

        self.traverseMatrix(startCoord)


    @staticmethod
    def _canMoveTo(mazeTraverser: MazeTraverser) -> Callable[[MatrixTraverser, Coordinate, Coordinate, Coordinate, Move, MatrixTree], bool]:
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


        # CLOSURE FUNCTION: this will be run directly 
        # by the Matrix Traversal Engine
        def _canMoveToWrapper(_matrixTraverser: MatrixTraverser, 
                                desiredCoord: Coordinate, 
                                prevCoord: Coordinate, 
                                currCoord: Coordinate,
                                prevMove: Move,
                                currNode: MatrixTree) -> bool:
            """
            Finally, this is the actual callback that the Matrix Traversal Engine
            will call directly. Therefore its signature must match exactly what the
            engine will expect.
            """

            # at the very start, the user defines where to move
            if currCoord.isStart:

                return mazeTraverser.canMoveToOnStartCallback(mazeTraverser, 
                                                              desiredCoord, 
                                                              prevCoord, 
                                                              currCoord, 
                                                              prevMove,
                                                              currNode)
            # EDGE CASE (example)
            # when 3 asks whether it can go to S
            # or even 2 if it can go to S?
            # S  3
            # 1  2

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
                                                    prevMove,
                                                    currNode)
        
        return _canMoveToWrapper 

    
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
    
