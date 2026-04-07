from Coordinate import Coordinate
# from MatrixTraverserCallbackManager import MatrixTraverserCallbackManager
# from MatrixTraverserStateManager import MatrixTraverserStateManager

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
        self.startCoordinate.isStart = True
        # best to not swap the order of state manager and callback manager
        # maybe the assumption is that some method in callback manager might
        # depend on the state manager 
        self.stateManager: MatrixTraverserStateManager = stateManager
        self.callbackManager: MatrixTraverserCallbackManager = callbackManager
        self.callbackManager.setMatrixTraverser(self)


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
            return
        
        # cell was not visited; we're visiting it right now
        # print(matrix[rowIdx][colIdx])
        # self.callbacks["firstVisit"](rowIdx, colIdx, matrix) 

        # now we mark cell as visited
        self._markAsVisited(currCoordinate)

        # moves = callbacks["pilotCell"](rowIdx, colIdx, prevRowIdx, prevColIdx, matrix, state)

        # move in the order that was specified
        # for move in moves:
        #     if move == "up":            
        if self.callbackManager.canMove(currCoordinate.rowUp(), currCoordinate):
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
    def __init__(self, callbackMap: dict):
        self.callbackMap = callbackMap
        self.matrixTraverser: MatrixTraverser

    def setMatrixTraverser(self, matrixTraverser: MatrixTraverser) -> None:
        self.matrixTraverser = matrixTraverser

    def getMatrixTraverser(self) -> MatrixTraverser:
        return self.matrixTraverser

    def canMove(self, currCoordinate: Coordinate, nextCoordinate: Coordinate) -> bool:
        """
        Callback that manages whether a cell 
        can move in the next move.
        """
        # if not self.matrixTraverser._isInsideMatrix(nextCoordinate):
        #     return False

        # if state["reachedEnd"]:
        #     return False

        # if matrix[nextRowIdx][nextColIdx] == "E":
        #     state["reachedEnd"] = True
        #     return True

        # # from the start, you can only move to 
        # # a cell with value 1
        # if matrix[currRowIdx][currColIdx] == "S":
        #     return matrix[nextRowIdx][nextColIdx] == "1"

        # # the next move cannot be the start 
        # if matrix[nextRowIdx][nextColIdx] == "S":
        #     return False

        # return int(matrix[currRowIdx][currColIdx])+1 == int(matrix[nextRowIdx][nextColIdx])
        return True
    


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