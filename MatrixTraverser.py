from Coordinate import Coordinate
# from MatrixTraverserCallbackManager import MatrixTraverserCallbackManager
# from MatrixTraverserStateManager import MatrixTraverserStateManager
from inspect import isfunction

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
        self.startCoordinate: Coordinate = startCoordinate
        # make sure that the start coordinate is actually a start coordinate
        self.startCoordinate.isStart = True
        # best to not swap the order of state manager and callback manager
        # maybe the assumption is that some method in callback manager might
        # depend on the state manager 
        self.stateManager: MatrixTraverserStateManager = stateManager
        self.callbackManager: MatrixTraverserCallbackManager = callbackManager
        # set the matrix traverser for the callback manager,
        # so the callback manager knows on which matrix traverser
        # to refer to 
        self.callbackManager._setMatrixTraverser(self)


    def traverseMatrix(self) -> None:
        """
        Main user-facing method to run the matrix traversal algorithm. 
        """
        
        prevCoordinate = Coordinate(-1, -1, isBeforeStart=True)
        startCoordinate = self.startCoordinate

        self._traverse(
            startCoordinate,
            prevCoordinate
        )
    

    def _traverse(self, currCoordinate: Coordinate, prevCoordinate: Coordinate) -> None:
        """
        The core algorithm: Traverses the matrix.
        """

        # if this cell does not exist (out of matrix)
        if not self._isInsideMatrix(currCoordinate):
            return

        # if this cell has been visited
        if self._isVisited(currCoordinate):
            # *******************************************+++
            # ****** START: OPERATIONS WHEN CELL IS ALREADY VISITED
            # ...

            # ****** END: OPERATIONS WHEN CELL IS ALREADY VISITED
            # *******************************************+++
            return
        
        # cell was not visited; we're visiting it right now
        self.callbackManager.onFirstVisit(prevCoordinate, currCoordinate)

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


        # GET THE MOVES OF THIS CELL
        nextMoves = self.callbackManager.getNextMoves(prevCoordinate, currCoordinate)
    
        # MOVE THROUGH THE MOVES
        # in the order in which they were specified

        # move in the order that was specified
        # for move in moves:
        #     if move == "up":            
        if self.callbackManager.canMove(prevCoordinate, currCoordinate, currCoordinate.rowUp()):
            # up
            self._traverse(currCoordinate.rowUp(), currCoordinate)
    
        # # elif move == "diag-up-right":
        # if callbacks["canMove"](rowIdx-1, colIdx+1, rowIdx, colIdx, matrix, state):
        #     # diag up right
        #     traverse(rowIdx-1, colIdx+1, rowIdx, colIdx, indexInfo, matrix, visited, callbacks, state)
    
        # # elif move == "right":
        # if callbacks["canMove"](rowIdx, colIdx+1, rowIdx, colIdx, matrix, state):
        #     # right
        #     traverse(rowIdx, colIdx+1, rowIdx, colIdx, indexInfo, matrix, visited, callbacks, state)
    
        # # elif move == "diag-down-right":
        # if callbacks["canMove"](rowIdx+1, colIdx+1, rowIdx, colIdx, matrix, state):
        #     # diag down right
        #     traverse(rowIdx+1, colIdx+1, rowIdx, colIdx, indexInfo, matrix, visited, callbacks, state)
    
        # # elif move == "down":
        # if callbacks["canMove"](rowIdx+1, colIdx, rowIdx, colIdx, matrix, state):
        #     # down
        #     traverse(rowIdx+1, colIdx, rowIdx, colIdx, indexInfo, matrix, visited, callbacks, state)
    
        # # elif move == "diag-down-left":
        # if callbacks["canMove"](rowIdx+1, colIdx-1, rowIdx, colIdx, matrix, state):
        #     # diag down left
        #     traverse(rowIdx+1, colIdx-1, rowIdx, colIdx, indexInfo, matrix, visited, callbacks, state)
    
        # # elif move == "left":
        # if callbacks["canMove"](rowIdx, colIdx-1, rowIdx, colIdx, matrix, state):
        #     # left
        #     traverse(rowIdx, colIdx-1, rowIdx, colIdx, indexInfo, matrix, visited, callbacks, state)
    
        # # elif move == "diag-up-left":
        # if callbacks["canMove"](rowIdx-1, colIdx-1, rowIdx, colIdx, matrix, state):
        #     # diag up left
        #     traverse(rowIdx-1, colIdx-1, rowIdx, colIdx, indexInfo, matrix, visited, callbacks, state)
                


    def _isVisited(self, coordinate: Coordinate) -> bool:
        """
        Checks if the cell at the given coordinate has been
        visited or not.
        """
        return self.visited[coordinate.row][coordinate.col] == 1


    def _markAsVisited(self, coordinate: Coordinate) -> None:
        """
        Mark the cell at the given coordinates as visited,
        """
        self.visited[coordinate.row][coordinate.col] = 1


    def _isInsideMatrix(self, coordinate: Coordinate) -> bool:
        """
        Checks if the given row and column index
        are inside the given matrix. 
        """
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


    def canMove(self, prevCoordinate: Coordinate, currCoordinate: Coordinate, desiredCoordinate: Coordinate) -> bool:
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
        if not self.matrixTraverser._isInsideMatrix(desiredCoordinate):
            # ..custom behavior when the current cell is asking if it can move 
            # to a coordinate that is not in the matrix..
            return False

        # run the user-defined callback, if exists
        if MatrixTraverserCallbackManager._dictHasFunction("canMove", self.callbackMap):
            userSaysCanMove: bool | None = self.callbackMap["canMove"](currCoordinate, prevCoordinate, desiredCoordinate)
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


    def onFirstVisit(self, prevCoordinate: Coordinate, currCoordinate: Coordinate) -> None:
        """
        On first visit of a cell, run this callback.
        """
        # run the user-defined callback, if exists
        if MatrixTraverserCallbackManager._dictHasFunction("onFirstVisit", self.callbackMap):
            self.callbackMap["onFirstVisit"](prevCoordinate, currCoordinate)
        # if the user did not specify a callback,
        # we don't have to do anything particular here


    def getNextMoves(self, prevCoordinate: Coordinate, currCoordinate: Coordinate) -> list[str]:
        """
        Get next moves for a cell.
        Order of the moves matters: The cell will try to move through the 
        returned moves, in sequential order.
        
        Note: That does not guarantee that the cell will move
        in that direction.
        """

        # run the user-defined callback, if exists
        if MatrixTraverserCallbackManager._dictHasFunction("getNextMoves", self.callbackMap):
            nextMoves: list[str] | None = self.callbackMap["getNextMoves"](currCoordinate, prevCoordinate)
            # if the user did not return, it means 
            # it's happy with the default moves
            if nextMoves is None:
                return MatrixTraverserMoves.getDefaultMoves()
            # check if the returned value is correct
            if not isinstance(nextMoves, list):
                raise Exception("next moves must be of type list")
            # if not isinstance(nextMoves, MatrixTraverserMoves):
            #     raise Exception("next moves must be of type MatrixTraverserMoves")
            return nextMoves

        # if the user did not provide the getNextMoves callback
        # fall back to the default moves
        return MatrixTraverserMoves.getDefaultMoves()


    @staticmethod
    def _dictHasFunction(key: str, map: dict[str, any]) -> bool: # type: ignore
        return key in map and isfunction(map[key])



class MatrixTraverserMoves:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def getDefaultMoves() -> list[str]:
        return [
            "up",
            "diag-up-right",
            "right",
            "diag-down-right",
            "down",
            "diag-down-left",
            "left",
            "diag-up-left"
        ]

    


class MatrixTraverserStateManager:
    """
    State manager for Matrix Traverser.
    """
    def __init__(self, state: dict):
        self.state = state
    
    def getState(self):
        """
        Returns the user-provided state.
        """
        return self.state