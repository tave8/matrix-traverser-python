from inspect import isfunction
from enum import Enum

class MatrixTraverser:
    """
    Matrix Traverser.
    """

    def __init__(self, 
                 matrix: list[list], 
                 startCoordinate: Coordinate,
                 callbackManager: MatrixTraverserCallbackManager,  # type: ignore
                 stateManager: MatrixTraverserStateManager):
        
        self.matrix = matrix
        self.visited = MatrixTraverser._generateVisitedMatrix(matrix)
        # best to not swap the order of state manager and callback manager
        # maybe the assumption is that some method in callback manager might
        # depend on the state manager 
        self.stateManager: MatrixTraverserStateManager = stateManager
        self.callbackManager: MatrixTraverserCallbackManager = callbackManager
        # set the matrix traverser for the callback manager,
        # so the callback manager knows on which matrix traverser
        # to refer to 
        self.stateManager._setMatrixTraverser(self)
        self.callbackManager._setMatrixTraverser(self)
        self.stateManager._setStartCoordinate(startCoordinate)


    def traverseMatrix(self) -> None:
        """
        Main user-facing method to run the matrix traversal algorithm. 
        """

        startCoordinate = self.stateManager.getStartCoordinate()
        prevCoordinate = self.stateManager.getBeforeStartCoordinate()

        self._traverse(
            startCoordinate,
            prevCoordinate,
            Move._BEFORE_START
        )
    

    def _traverse(self, currCoordinate: Coordinate, prevCoordinate: Coordinate, prevMove: Move) -> None:
        """
        The core algorithm: Traverses the matrix.
        """

        # if this cell does not exist (out of matrix)
        if not self.isInsideMatrix(currCoordinate):
            return

        # if this cell has been visited
        if self._isVisited(currCoordinate):
            # *******************************************+++
            # ****** START: OPERATIONS WHEN CELL IS ALREADY VISITED
            # ...

            # ****** END: OPERATIONS WHEN CELL IS ALREADY VISITED
            # *******************************************+++
            return
        
        self.callbackManager.beforeFirstVisit(prevCoordinate, currCoordinate, prevMove)

        # *******************************************+++
        # ****** START: OPERATIONS BEFORE CELL IS MARKED AS VISITED
        # you can perform more custom operations here, 
        # before marking the cell as visited and then moving
        # to maybe other cells


        # after we've performed custom operations on this cell, 
        # we mark cell as visited right before we go in other directions
        # important: after the cell is marked as visited, we should not
        # perform operations that rely on whether the cell is visited or not
        self._markAsVisited(currCoordinate)

        # ****** END: OPERATIONS BEFORE CELL IS MARKED AS VISITED
        # *******************************************+++

        nextMoves: list[Move]

        # GET THE MOVES OF THIS CELL
        nextMoves = self.callbackManager.getNextMoves(prevCoordinate, currCoordinate, prevMove)

        # MOVE THROUGH THE MOVES
        # move in the order that was specified
        for nextMove in nextMoves:

            if nextMove == Move.UP:
                # up
                if self.callbackManager.canMove(currCoordinate.up(), prevCoordinate, currCoordinate):
                    self._traverse(currCoordinate.up(), currCoordinate, Move.UP)

            elif nextMove == Move.DIAGONAL_UP_RIGHT:
                # diagonal up right
                if self.callbackManager.canMove(currCoordinate.diagonalUpRight(), prevCoordinate, currCoordinate):
                    self._traverse(currCoordinate.diagonalUpRight(), currCoordinate, Move.DIAGONAL_UP_RIGHT)

            elif nextMove == Move.RIGHT:
                # right
                if self.callbackManager.canMove(currCoordinate.right(), prevCoordinate, currCoordinate):
                    self._traverse(currCoordinate.right(), currCoordinate, Move.RIGHT)

            elif nextMove == Move.DIAGONAL_DOWN_RIGHT:
                # diagonal down right
                if self.callbackManager.canMove(currCoordinate.diagonalDownRight(), prevCoordinate, currCoordinate):
                    self._traverse(currCoordinate.diagonalDownRight(), currCoordinate, Move.DIAGONAL_DOWN_RIGHT)

            elif nextMove == Move.DOWN:
                # down
                if self.callbackManager.canMove(currCoordinate.down(), prevCoordinate, currCoordinate):
                    self._traverse(currCoordinate.down(), currCoordinate, Move.DOWN)

            elif nextMove == Move.DIAGONAL_DOWN_LEFT:
                # diagonal down left
                if self.callbackManager.canMove(currCoordinate.diagonalDownLeft(), prevCoordinate, currCoordinate):
                    self._traverse(currCoordinate.diagonalDownLeft(), currCoordinate, Move.DIAGONAL_DOWN_LEFT)

            elif nextMove == Move.LEFT:
                # left
                if self.callbackManager.canMove(currCoordinate.left(), prevCoordinate, currCoordinate):
                    self._traverse(currCoordinate.left(), currCoordinate, Move.LEFT)

            elif nextMove == Move.DIAGONAL_UP_LEFT:
                # diagonal up left 
                if self.callbackManager.canMove(currCoordinate.diagonalUpLeft(), prevCoordinate, currCoordinate):
                    self._traverse(currCoordinate.diagonalUpLeft(), currCoordinate, Move.DIAGONAL_UP_LEFT)
                


    def getAtCoordinate(self, coord: Coordinate):
        """
        Get the cell value in the matrix, at the given coordinate.
        """
        # cannot access the "before to start" coordinate
        if coord.isBeforeStart:
            raise Exception("cannot access 'before to start' coordinate")

        # check if the coordinate exists in the matrix
        if not self.isInsideMatrix(coord):
            raise Exception("the coordinate does not exist in this matrix")
        return self.matrix[coord.row][coord.col]


    def _isVisited(self, coordinate: Coordinate) -> bool:
        """
        Checks if the cell at the given coordinate has been
        visited or not.
        """
        return self.visited[coordinate.row][coordinate.col] > 0


    def _markAsVisited(self, coordinate: Coordinate) -> None:
        """
        Mark the cell at the given coordinates as visited,
        """
        val = self.visited[coordinate.row][coordinate.col]
        if val != 0:
            raise Exception(f"cell value had to be 0 when visiting "
                            +f"cell for the first time, got {val} instead")
        self.visited[coordinate.row][coordinate.col] = 1


    def isInsideMatrix(self, coordinate: Coordinate) -> bool:
        """
        Checks if the given row and column index
        are inside the given matrix. 
        """
        # the coordinate "is before start" is never in the matrix
        if coordinate.isBeforeStart:
            return False
        
        insideRows = coordinate.row >= 0 and coordinate.row < len(self.matrix)
        insideCols = coordinate.col >= 0 and coordinate.col < len(self.matrix[0])
        return insideRows and insideCols


    @staticmethod
    def _generateVisitedMatrix(matrix: list[list]) -> list[list]:
        """
        Generate a "visited matrix" 
        to mark the cells as visited or not.
        """
        return MatrixTraverser._generate0Matrix(matrix)


    @staticmethod
    def _generate0Matrix(matrix: list[list]) -> list[list]:
        """
        Returns a matrix of 0's, with the same number of rows 
        and columns as the given matrix. 
        """
        ret = []
        for i in range(len(matrix)):
            row = []
            for j in range(len(matrix[0])):
                row.append(0)
            ret.append(row)
        return ret





class MatrixTraverserCallbackManager:
    """
    An instance of this class is associated with 
    a Matrix Traverser instance, and defines the behavior of 
    a cell, at specific points in time.
    For example, if a cell can move in a certain direction,
    the directions that a cell that meets certain criteria should move to etc.
    """

    def __init__(self, callbackMap: dict):
        self.callbackMap = callbackMap
        self.matrixTraverser: MatrixTraverser

    def _setMatrixTraverser(self, matrixTraverser: MatrixTraverser) -> None:
        self.matrixTraverser = matrixTraverser

    def getMatrixTraverser(self) -> MatrixTraverser:
        return self.matrixTraverser


    def canMove(self, desiredCoordinate: Coordinate, prevCoordinate: Coordinate, currCoordinate: Coordinate) -> bool:
        """
        Before moving in a direction, the core traversal 
        algorithm will ask if it can move in a direction.
        The user can therefore specify the criteria 
        based on which a cell can or cannot move in a certain direction.

        Therefore:
            - prevCoordinate: the coordinate of the cell that just moved to this cell,
                so the coordinate of the previous cell
            
            - currCoordinate: the coordinate of where the cell is at right now

            - desiredCoordinate: the desired coordinate, where the cell would like to move next 
                    and therefore has not moved yet. The point of this callback is precisely 
                    to ask whether the cell can move to the desired coordinate, and that may 
                    depend on conditions on the previous or current coordinate, for example
            
        """

        # if the desired coordinate is not even in the matrix,
        # chances are, it won't be of much use and for sure
        # the cell will not be able to move there
        # however this behavior can be customized
        if not self.matrixTraverser.isInsideMatrix(desiredCoordinate):
            # ..custom behavior when the current cell is asking if it can move 
            # to a coordinate that is not in the matrix..
            return False

        # run the user-defined callback, if exists
        if MatrixTraverserCallbackManager._dictHasFunction("canMove", self.callbackMap):
            userSaysCanMove: bool | None = self.callbackMap["canMove"](self.matrixTraverser, desiredCoordinate, prevCoordinate, currCoordinate)
            # if the user did not return, it means 
            # it's happy with this cell moving in the desired direction 
            if userSaysCanMove is None:
                return True
            # check if the returned value is correct
            if not isinstance(userSaysCanMove, bool):
                raise Exception("userSaysCanMove must be of type bool")
            return userSaysCanMove

        # if the user did not specify the callback, 
        # we assume every direction is good to move to
        return True


    def beforeFirstVisit(self, 
                         prevCoordinate: Coordinate, 
                         currCoordinate: Coordinate, 
                         prevMove: Move) -> None:
        """
        Before first visit of a cell, run this callback.
        """
        # run the user-defined callback, if exists
        if MatrixTraverserCallbackManager._dictHasFunction("beforeFirstVisit", self.callbackMap):
            self.callbackMap["beforeFirstVisit"](self.matrixTraverser, 
                                                 prevCoordinate, 
                                                 currCoordinate,
                                                 prevMove)
        # if the user did not specify a callback,
        # we don't have to do anything particular here


    def getNextMoves(self, 
                     prevCoordinate: Coordinate, 
                     currCoordinate: Coordinate, 
                     prevMove: Move) -> list[Move]:
        """
        Get next moves for a cell.
        Order of the moves matters: The cell will try to move through the 
        returned moves, in sequential order.
        
        Note: That does not guarantee that the cell will move
        in that direction.
        """

        # NOTE: prevCoordinate could be "before start"
        #       and currCoordinate could be "start"
        # if you need to perform custom logic on what happens
        # at the very start, when current coordinate is start 
        # and previous coordinate is before start, you could do it here  

        # run the user-defined callback, if exists
        if MatrixTraverserCallbackManager._dictHasFunction("getNextMoves", self.callbackMap):
            nextMoves: list[Move] | None = self.callbackMap["getNextMoves"](self.matrixTraverser, 
                                                                            prevCoordinate, 
                                                                            currCoordinate, 
                                                                            prevMove)
            # if the user did not return, it means 
            # it's happy with the default moves
            if nextMoves is None:
                return MatrixTraverserMoves.getDefaultMoves()
            
            # check if the returned value is correct
            if not isinstance(nextMoves, list):
                raise Exception("next moves must be of type list")
            
            return nextMoves

        # if the user did not provide the getNextMoves callback
        # fall back to the default moves
        return MatrixTraverserMoves.getDefaultMoves()


    @staticmethod
    def _dictHasFunction(key: str, map: dict[str, any]) -> bool: # type: ignore
        return key in map and isfunction(map[key])


    


class MatrixTraverserStateManager:
    """
    State manager for Matrix Traverser.

    1 instance of MatrixTraverserStateManager <-> 1 instance of MatrixTraverser
    """

    def __init__(self, state: dict):
        # user-defined state
        self.state = state
        self.matrixTraverser: MatrixTraverser
        # internal state of the matrix traverser
        self._startCoordinate: Coordinate 
        self._beforeStartCoordinate: Coordinate = Coordinate(-1, -1, isBeforeStart=True)


    def _setMatrixTraverser(self, matrixTraverser: MatrixTraverser) -> None:
        # you cannot set the matrix traversed if it was already set
        self.matrixTraverser = matrixTraverser

    def getMatrixTraverser(self) -> MatrixTraverser:
        # check whether the matrix traverser is None, 
        # it must not be none
        return self.matrixTraverser
    
    def getStartCoordinate(self) -> Coordinate:
        return self._startCoordinate

    def _setStartCoordinate(self, startCoordinate: Coordinate) -> None:
        startCoordinate.isStart = True
        self._startCoordinate = startCoordinate
    
    def getBeforeStartCoordinate(self) -> Coordinate:
        return self._beforeStartCoordinate
    
    def getState(self) -> dict:
        """
        Returns the user-provided state.
        """
        return self.state
    


class MatrixTraverserMoves:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def getDefaultMoves() -> list[Move]:
        return [
            Move.UP,
            Move.DIAGONAL_UP_RIGHT,
            Move.RIGHT,
            Move.DIAGONAL_DOWN_RIGHT,
            Move.DOWN,
            Move.DIAGONAL_DOWN_LEFT, 
            Move.LEFT,
            Move.DIAGONAL_UP_LEFT
        ]


class Coordinate:
    """
    A cell coordinate, so row and column.
    """
    def __init__(self, row: int, col: int, isStart: bool=False, isBeforeStart: bool=False):
        self.row = row
        self.col = col
        self.isStart = isStart
        self.isBeforeStart = isBeforeStart
    
    def getRow(self) -> int:
        return self.row

    def getCol(self) -> int:
        return self.col

    # DIRECTIONS/MOVES 
    def up(self) -> Coordinate:
        return Coordinate(self.row-1, self.col)

    def down(self) -> Coordinate:
        return Coordinate(self.row+1, self.col)
    
    def diagonalUpRight(self) -> Coordinate:
        return Coordinate(self.row-1, self.col+1)

    def diagonalUpLeft(self) -> Coordinate:
        return Coordinate(self.row-1, self.col-1)

    def right(self) -> Coordinate:
        return Coordinate(self.row, self.col+1)

    def left(self) -> Coordinate:
        return Coordinate(self.row, self.col-1)
    
    def diagonalDownRight(self) -> Coordinate:
        return Coordinate(self.row+1, self.col+1)
    
    def diagonalDownLeft(self) -> Coordinate:
        return Coordinate(self.row+1, self.col-1)

    def __str__(self) -> str:
        flags = []
        if self.isStart:
            flags.append("isStart")
        if self.isBeforeStart:
            flags.append("isBeforeStart")
        
        flag_str = f", {', '.join(flags)}" if flags else ""
        return f"[Coordinate: [{self.row}, {self.col}]{flag_str}]"


class Move(Enum):
    # the initial move
    _BEFORE_START = "_before_start"
    UP = "up"
    DIAGONAL_UP_RIGHT = "diagonal-up-right"
    RIGHT = "right"
    DIAGONAL_DOWN_RIGHT = "diagonal-down-right"
    DOWN = "down"
    DIAGONAL_DOWN_LEFT = "diagonal-down-left"
    LEFT = "left"
    DIAGONAL_UP_LEFT = "diagonal-up-left"