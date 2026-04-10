from inspect import isfunction
from enum import Enum

class MatrixTraverser:
    """
    Matrix Traverser.
    """

    def __init__(self, 
                 matrix: list[list], 
                 userCallbackMap: dict = {}, 
                 userState: dict = {}):
        
        self.matrix = matrix
        self.visited = Matrix.generateVisitedMatrixFrom(matrix)
        self.stateManager = StateManager(userState)
        self.callbackManager = CallbackManager(userCallbackMap)


    def traverseMatrix(self, 
                       startCoord: Coordinate,
                       beforeStartCoord: Coordinate) -> None:
        """
        Main user-facing method to run the matrix traversal algorithm. 
        """

        StateManager._setStartCoordinate(self, startCoord)

        self.__traverse(
            currCoord=startCoord,
            prevCoord=beforeStartCoord,
            prevMove=Move._BEFORE_START
        )
    

    def __traverse(self, 
                  currCoord: Coordinate, 
                  prevCoord: Coordinate, 
                  prevMove: Move) -> None:
        """
        The core algorithm: Traverses the matrix.
        """

        # if you can end the algorithm now
        # if self.callbackManager.canEnd(prevCoordinate, currCoordinate, prevMove):
        #     self.callbackManager.onEnd()
        #     return 

        # if this cell does not exist (out of matrix)
        if not Matrix.isInsideMatrix(self.matrix, currCoord):
            return

        CallbackManager.beforeVisit(self, prevCoord, currCoord, prevMove)

        # if this cell has been visited
        if Matrix.isVisited(self.visited, currCoord):

            if CallbackManager.onMultipleVisitMustStop(self, prevCoord, currCoord, prevMove):
                # ... operations when cell is already visited...
                return 
        
        # because skipping a visited cell is left to the user,
        # we don't know if, when we get here, that cell will have 
        # been visited for the first time or not. so we must do a check
        if not Matrix.isVisited(self.visited, currCoord):

            # if self.callbackManager.canVisit(prevCoordinate, currCoord, prevMove):

            CallbackManager.beforeFirstVisit(self, prevCoord, currCoord, prevMove)

            # *******************************************+++
            # ****** START: OPERATIONS BEFORE CELL IS MARKED AS VISITED
            # you can perform more custom operations here, 
            # before marking the cell as visited and then moving
            # to maybe other cells


            # after we've performed custom operations on this cell, 
            # we mark cell as visited right before we go in other directions
            # important: after the cell is marked as visited, we should not
            # perform operations that rely on whether the cell is visited or not
            Matrix.markAsVisited(self.visited, currCoord)

            # self.stateManager.updateStatsAfterFirstVisit(prevCoord, currCoord, prevMove)

        # ****** END: OPERATIONS BEFORE CELL IS MARKED AS VISITED
        # *******************************************+++

        # GET THE MOVES OF THIS CELL
        nextMoves = CallbackManager.getNextMoves(self, prevCoord, currCoord, prevMove)

        # MOVE THROUGH THE MOVES
        # move in the order that was specified
        for nextMove in nextMoves:

            if nextMove == Move.UP:
                # up
                if CallbackManager.canMove(self, currCoord.up(), prevCoord, currCoord, prevMove):
                    self.__traverse(currCoord.up(), currCoord, Move.UP)

            elif nextMove == Move.DIAGONAL_UP_RIGHT:
                # diagonal up right
                if CallbackManager.canMove(self, currCoord.diagonalUpRight(), prevCoord, currCoord, prevMove):
                    self.__traverse(currCoord.diagonalUpRight(), currCoord, Move.DIAGONAL_UP_RIGHT)

            elif nextMove == Move.RIGHT:
                # right
                if CallbackManager.canMove(self, currCoord.right(), prevCoord, currCoord, prevMove):
                    self.__traverse(currCoord.right(), currCoord, Move.RIGHT)

            elif nextMove == Move.DIAGONAL_DOWN_RIGHT:
                # diagonal down right
                if CallbackManager.canMove(self, currCoord.diagonalDownRight(), prevCoord, currCoord, prevMove):
                    self.__traverse(currCoord.diagonalDownRight(), currCoord, Move.DIAGONAL_DOWN_RIGHT)

            elif nextMove == Move.DOWN:
                # down
                if CallbackManager.canMove(self, currCoord.down(), prevCoord, currCoord, prevMove):
                    self.__traverse(currCoord.down(), currCoord, Move.DOWN)

            elif nextMove == Move.DIAGONAL_DOWN_LEFT:
                # diagonal down left
                if CallbackManager.canMove(self, currCoord.diagonalDownLeft(), prevCoord, currCoord, prevMove):
                    self.__traverse(currCoord.diagonalDownLeft(), currCoord, Move.DIAGONAL_DOWN_LEFT)

            elif nextMove == Move.LEFT:
                # left
                if CallbackManager.canMove(self, currCoord.left(), prevCoord, currCoord, prevMove):
                    self.__traverse(currCoord.left(), currCoord, Move.LEFT)

            elif nextMove == Move.DIAGONAL_UP_LEFT:
                # diagonal up left 
                if CallbackManager.canMove(self, currCoord.diagonalUpLeft(), prevCoord, currCoord, prevMove):
                    self.__traverse(currCoord.diagonalUpLeft(), currCoord, Move.DIAGONAL_UP_LEFT)

    #  def __jumpTo() -> None:
    #     """
    #     Jumps to a cell with at the .
    #     """           

    # def findOne(self, findOneCallback, startFromCoordinate: Coordinate) -> Coordinate:
    #     """
    #     Find the first cell that makes the given callback evaluate to true. 
    #     """

    #     if not isfunction(findOneCallback):
    #         raise Exception("findOneCallback must be a function")
        
    #     def canEndCallback(findOneMt: MatrixTraverser, 
    #                         prevCoordinate: Coordinate, 
    #                         currCoordinate: Coordinate,
    #                         prevMove: Move) -> bool:
            
    #         if findOneCallback(findOneMt, prevCoordinate, currCoordinate, prevMove):
    #             return True 
    #         return False 
    

    #     def onEndCallback(findOneMt: MatrixTraverser):
    #         # print("ended findOne")
    #         pass
        

    #     callbackMapOfFindOne = {
    #         "canEnd": canEndCallback,
    #         "onEnd": onEndCallback
    #     }

    #     matrixTraverserOfFindOne = MatrixTraverser(self.matrix, 
    #                                                 startFromCoordinate,
    #                                                 MatrixTraverserCallbackManager(callbackMapOfFindOne),
    #                                                 MatrixTraverserStateManager({}))
        
    #     matrixTraverserOfFindOne.traverseMatrix()

    #     matrixTraverserOfFindOne.callbackManager.onEnd()



class CallbackManager:
    """
    Defines the behavior of 
    a cell, at specific points in time.
    For example, if a cell can move in a certain direction,
    the directions that a cell that meets certain criteria should move to etc.
    """

    def __init__(self, callbackMap: dict):
        self.callbackMap = callbackMap

    @staticmethod
    def canMove(mt: MatrixTraverser, 
                desiredCoordinate: Coordinate, 
                prevCoordinate: Coordinate, 
                currCoordinate: Coordinate,
                prevMove: Move) -> bool:
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
        if not Matrix.isInsideMatrix(mt.matrix, desiredCoordinate):
            # ..custom behavior when the current cell is asking if it can move 
            # to a coordinate that is not in the matrix..
            return False

        # run the user-defined callback, if exists
        if FunctionHelper.mapHasFunction("canMove", mt.callbackManager.callbackMap):
            userSaysCanMove: bool | None = mt.callbackManager.callbackMap["canMove"](mt, 
                                                                                    desiredCoordinate, 
                                                                                    prevCoordinate, 
                                                                                    currCoordinate,
                                                                                    prevMove)
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

    @staticmethod
    def beforeFirstVisit(mt: MatrixTraverser, 
                         prevCoordinate: Coordinate, 
                         currCoordinate: Coordinate, 
                         prevMove: Move) -> None:
        """
        Before first visit of a cell, run this callback.
        """

        # run the user-defined callback, if exists
        if FunctionHelper.mapHasFunction("beforeFirstVisit", mt.callbackManager.callbackMap):
            mt.callbackManager.callbackMap["beforeFirstVisit"](mt, 
                                                                prevCoordinate, 
                                                                currCoordinate,
                                                                prevMove)
        # if the user did not specify a callback,
        # we don't have to do anything particular here


    @staticmethod
    def beforeVisit(mt: MatrixTraverser, 
                        prevCoordinate: Coordinate, 
                        currCoordinate: Coordinate, 
                        prevMove: Move) -> None:
        """
        Before ANY visit of a cell, run this callback.
        """

        # run the user-defined callback, if exists
        if FunctionHelper.mapHasFunction("beforeVisit", mt.callbackManager.callbackMap):
            mt.callbackManager.callbackMap["beforeVisit"](mt, 
                                                            prevCoordinate, 
                                                            currCoordinate,
                                                            prevMove)
        # if the user did not specify a callback,
        # we don't have to do anything particular here


    @staticmethod
    def getNextMoves(mt: MatrixTraverser, 
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
        if FunctionHelper.mapHasFunction("getNextMoves", mt.callbackManager.callbackMap):
            nextMoves: list[Move] | None = mt.callbackManager.callbackMap["getNextMoves"](mt, 
                                                                                        prevCoordinate, 
                                                                                        currCoordinate, 
                                                                                        prevMove)
            # if the user did not return, it means 
            # it's happy with the default moves
            if nextMoves is None:
                return Moves.getDefaultMoves()
            
            # check if the returned value is correct
            if not isinstance(nextMoves, list):
                raise Exception("next moves must be of type list")
            
            return nextMoves

        # if the user did not provide the getNextMoves callback
        # fall back to the default moves
        return Moves.getDefaultMoves()



    # def canVisit(self, 
    #             prevCoordinate: Coordinate, 
    #             currCoordinate: Coordinate,
    #             prevMove: Move) -> bool:
    #     """
    #     Do I mark as visited this cell? 
    #     This is useful when we want our algorithm to keep exploring
    #     until the specific cells that meet certain criteria are found.
    #     This allows the algorithm to effectively "explore but not visit".

    #     In conjuction with onMultipleVisitMustStop, it can be used to express
    #     logic like "visit a cell only if.." and "if it's been visited, continue anyway".

    #     NOTE: If we never visit any cell, the algorithm will never terminate.
    #     """

    #     # run the user-defined callback, if exists
    #     if MatrixTraverserCallbackManager._dictHasFunction("canVisit", self.callbackMap):
    #         userSaysCanVisit: bool | None = self.callbackMap["canVisit"](self.matrixTraverser, 
    #                                                                         prevCoordinate, 
    #                                                                         currCoordinate,
    #                                                                         prevMove)
    #         # if the user did not return, it means 
    #         # it's happy with this cell being visited, 
    #         # which is the default behavior
    #         if userSaysCanVisit is None:
    #             return True
            
    #         # check if the returned value is correct
    #         if not isinstance(userSaysCanVisit, bool):
    #             raise Exception("userSaysCanVisit must be of type bool")
            
    #         return userSaysCanVisit

    #     # by default, we always visit a cell
    #     return True 
    
    @staticmethod
    def onMultipleVisitMustStop(mt: MatrixTraverser, 
                                prevCoordinate: Coordinate, 
                                currCoordinate: Coordinate, 
                                prevMove: Move) -> bool:
        """
        Defines the logic of whether a cell that is visited multiple times
        must be skipped. Wrong configuration of this callback
        can result in non termination of the algorithm, which is 
        why the primary semantics points to skip instead of continuing.
        
        If we don't skip (so if we continue) it probably means 
        we're more interested in exploring the matrix rather than
        using some cell value. This behavior is desirable 
        in the following cases, for example: 
        
        - we don't know where a certain target cell is, and therefore
        we don't really care about whether a cell was visited or not
        
        - we must ignore that this cell was visited because we might
        need to go back to certain places of the matrix, and therefore 
        we have to inevitably pass through some visited cells, and we 
        don't care that they were visited
        """

        # run the user-defined callback, if exists
        if FunctionHelper.mapHasFunction("onMultipleVisitMustStop", mt.callbackManager.callbackMap):
            mustStop: bool | None = mt.callbackManager.callbackMap["onMultipleVisitMustStop"](mt, 
                                                                                        prevCoordinate, 
                                                                                        currCoordinate,
                                                                                        prevMove)
            # if the user did not return, it means 
            # it's happy with this cell moving being skipped, 
            # if it's been visited 
            if mustStop is None:
                return True
            
            # check if the returned value is correct
            if not isinstance(mustStop, bool):
                raise Exception("stop must be of type bool")
            
            return mustStop
        
        # default behavior is, we always skip visited cells
        # in other words, in this case the algorithm cannot 
        # "jump" or ignore visited cells, which means that 
        # the algorithm might get stuck in a sort of "fence"
        # where it will not visit visited cells, and therefore
        # it will not explore other cells "on the other side" 
        # of the visited cells. this behavior is normal, if 
        # if the "explorer" behaviour is not desired or needed. 
        return True
    

    # def canEnd(self, 
    #             prevCoordinate: Coordinate, 
    #             currCoordinate: Coordinate,
    #             prevMove: Move) -> bool:
    #     """
    #     Can I end the algorithm right now?
        
    #     By default the algorithm will terminate only 
    #     when all cells will be visited. We can prevent that 
    #     and decide the end of the algorithm.
    #     """

    #     # run the user-defined callback, if exists
    #     if MatrixTraverserCallbackManager._dictHasFunction("canEnd", self.callbackMap):
    #         userSaysCanEnd: bool | None = self.callbackMap["canEnd"](self.matrixTraverser, 
    #                                                                         prevCoordinate, 
    #                                                                         currCoordinate,
    #                                                                         prevMove)
    #         # if the user did not return, it means 
    #         # it's happy with not ending the algorithm
    #         if userSaysCanEnd is None:
    #             return False
            
    #         # check if the returned value is correct
    #         if not isinstance(userSaysCanEnd, bool):
    #             raise Exception("userSaysCanEnd must be of type bool")
            
    #         return userSaysCanEnd

    #     # by default, we don't end the algorithm
    #     return False
    

    # def onEnd(self) -> None:
    #     """
    #     What should happen right before the algorithm terminates?
    #     """

    #     # run the user-defined callback, if exists
    #     if MatrixTraverserCallbackManager._dictHasFunction("onEnd", self.callbackMap):
    #         self.callbackMap["onEnd"](self.matrixTraverser)




class StateManager:
    """
    State manager for Matrix Traverser instances.
    """

    def __init__(self, userState: dict):
        # user-defined state
        self.userState = userState
        # the algorithm's state so far
        self.state: dict = {
            # the cells that were visited
            # "visitedCells": []
        }
        # dummy coordinate, will be overwritten soon
        self.startCoordinate: Coordinate = Coordinate(-1, -1, isStart=True)
    

    @staticmethod
    def _setStartCoordinate(mt: MatrixTraverser, coord: Coordinate):        
        mt.stateManager.startCoordinate = coord


    @staticmethod
    def getStartCoordinate(mt: MatrixTraverser) -> Coordinate:
        return mt.stateManager.startCoordinate

    @staticmethod
    def getUserState(mt: MatrixTraverser) -> dict:
        """
        Returns the user-provided state.
        """
        return mt.stateManager.userState
    




class Matrix:

    @staticmethod
    def isVisited(visitedMatrix: list[list[int]], 
                  coord: Coordinate) -> bool:
        """
        Checks if the cell at the given coordinate has been
        visited or not.
        """
        # check that given row and col exist in matrix
        return visitedMatrix[coord.getRow()][coord.getCol()] == 1


    @staticmethod
    def markAsVisited(visitedMatrix: list[list[int]], 
                      coord: Coordinate) -> None:
        """
        Mark the cell at the given coordinates as visited.
        """
        val = visitedMatrix[coord.getRow()][coord.getCol()]

        if val != 0:
            raise Exception(f"cell value had to be 0 when visiting "
                            +f"cell for the first time, got {val} instead")
        
        visitedMatrix[coord.getRow()][coord.getCol()] = 1


    @staticmethod
    def isAMatrix(matrix: list[list]) -> bool:
        """
        Is this a matrix? The matrix must have
        the exact same number of rows and columns.
        """
        # FIX 
        return False


    @staticmethod
    def getAtCoordinate(matrix: list[list], 
                        coord: Coordinate):
        """
        Get the cell value in the matrix, at the given coordinate.
        """

        # cannot access the "before to start" coordinate
        if coord.isBeforeStart:
            raise Exception("cannot access 'before to start' coordinate")

        # check if the coordinate exists in the matrix
        if not Matrix.isInsideMatrix(matrix, coord):
            raise Exception("the coordinate does not exist in this matrix")
        
        # check if the row and col exist

        return matrix[coord.getRow()][coord.getCol()]


    @staticmethod
    def isInsideMatrix(matrix: list[list], 
                       coordinate: Coordinate) -> bool:
        """
        Checks if the given row and column index
        are inside the given matrix. 
        """

        # the coordinate "is before start" is never in the matrix
        if coordinate.isBeforeStart:
            return False
        
        insideRows = coordinate.getRow() >= 0 and coordinate.getRow() < len(matrix)
        insideCols = coordinate.getCol() >= 0 and coordinate.getCol() < len(matrix[0])

        return insideRows and insideCols


    @staticmethod
    def getHowManyCols(matrix: list[list]) -> int:
        return len(matrix[0])


    @staticmethod
    def getHowManyRows(matrix: list[list]) -> int:
        return len(matrix)

    @staticmethod
    def isSquare(matrix: list[list]) -> bool:
        return Matrix.getHowManyCols(matrix) == Matrix.getHowManyRows(matrix)

    @staticmethod
    def hasOneCol(matrix: list[list]) -> bool:
        return Matrix.getHowManyCols(matrix) == 1


    @staticmethod
    def hasOneRow(matrix: list[list]) -> bool:
        return Matrix.getHowManyRows(matrix) == 1


    @staticmethod
    def hasEvenRows(matrix: list[list]) -> bool:
        return Matrix.getHowManyRows(matrix) % 2 == 0


    @staticmethod
    def hasEvenCols(matrix: list[list]) -> bool:
        return Matrix.getHowManyCols(matrix) % 2 == 0


    @staticmethod
    def hasOddRows(matrix: list[list]) -> bool:
        return not Matrix.hasEvenRows(matrix)


    @staticmethod
    def hasOddCols(matrix: list[list]) -> bool:
        return not Matrix.hasEvenCols(matrix)

    @staticmethod
    def getFirstCol() -> int:
        return 0
    
    @staticmethod
    def getFirstRow() -> int:
        return 0

    @staticmethod
    def getLastRow(matrix: list[list]) -> int:
        return Matrix.getHowManyRows(matrix)-1

    @staticmethod
    def getLastCol(matrix: list[list]) -> int:
        return Matrix.getHowManyCols(matrix)-1

    @staticmethod
    def getMiddleCol(matrix: list[list]) -> int:
        """
        Returns the index of the middle column,
        if the matrix has odd number of columns.
        """
        if Matrix.hasEvenCols(matrix):
            raise Exception("cannot get middle col of matrix with even number of cols")
        return Matrix.getHowManyCols(matrix) // 2

    @staticmethod
    def getMiddleRow(matrix: list[list]) -> int:
        """
        Returns the index of the middle row,
        if the matrix has odd number of rows.
        """
        if Matrix.hasEvenRows(matrix):
            raise Exception("cannot get middle row of matrix with even number of rows")
        return Matrix.getHowManyRows(matrix) // 2


    @staticmethod
    def getRowsNextToMiddle(matrix: list[list]) -> list[int]:
        """
        Returns the indexes of the two rows before the middle row.
        """
        if Matrix.hasOneRow(matrix):
            raise Exception("matrix has only one row; cannot give you two rows")

        if Matrix.hasOddRows(matrix):
            middleRow = Matrix.getMiddleRow(matrix)
            return [middleRow-1, middleRow+1]

        # matrix has more than 1 row and it has even number of rows
        return [
            # the left row 
            (Matrix.getHowManyRows(matrix) // 2) - 1,
            # the right row
            Matrix.getHowManyRows(matrix) // 2
        ]

    @staticmethod
    def getColsNextToMiddle(matrix: list[list]) -> list[int]:
        """
        Returns the indexes of the two cols before the middle col.
        """
        if Matrix.hasOneCol(matrix):
            raise Exception("matrix has only one col; cannot give you two cols")

        if Matrix.hasOddCols(matrix):
            middleCol = Matrix.getMiddleCol(matrix)
            return [middleCol-1, middleCol+1]

        # matrix has more than 1 col and it has even number of cols
        return [
            # the left col
            (Matrix.getHowManyCols(matrix) // 2) - 1,
            # the right col
            Matrix.getHowManyCols(matrix) // 2
        ]



    @staticmethod
    def generateVisitedMatrixFrom(matrix: list[list]) -> list[list[int]]:
        """
        Generate a "visited matrix" 
        to mark the cells as visited or not.
        """
        return Matrix.generate0MatrixFrom(matrix)


    @staticmethod
    def generate0MatrixFrom(matrix: list[list]) -> list[list[int]]:
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




class Moves:
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

    @staticmethod
    def getAllMoves() -> list[Move]:
        return [move for move in Move]



class Coordinate:
    """
    A cell coordinate, so row and column.
    """
    def __init__(self, row: int, col: int, isStart: bool=False, isBeforeStart: bool=False):
        self.row = row
        self.col = col
        self.isStart = isStart
        self.isBeforeStart = isBeforeStart
    
    def hasSameCoordinate(self, otherCoord: Coordinate) -> bool:
        return self.getRow() == otherCoord.getRow() and self.getCol() == otherCoord.getCol()
    
    def isCol(self, col: int) -> bool:
        return self.getCol() == col

    def isRow(self, row: int) -> bool:
        return self.getRow() == row

    def isFirstRow(self) -> bool:
        return self.isRow(Matrix.getFirstRow())

    def isLastRow(self, matrix: list[list]) -> bool:
        return self.isRow(Matrix.getLastRow(matrix))

    def isFirstCol(self) -> bool:
        return self.isCol(Matrix.getFirstCol())

    def isLastCol(self, matrix: list[list]) -> bool:
        return self.isCol(Matrix.getLastCol(matrix)) 

    def isMiddleRow(self, matrix: list[list]) -> bool:
        """
        Is this row the middle row?
        Note that the middle row only exists in a matrix
        whose number of rows is odd.
        In a matrix with even number of rows,
        you'll have to use other methods like isRowBeforeMiddle
        """
        if Matrix.hasEvenRows(matrix):
            raise Exception("if this row is the middle row cannot be answered "
                            +"because the given matrix has an even number of rows")

        return self.isRow(Matrix.getMiddleRow(matrix))


    def isMiddleCol(self, matrix: list[list]) -> bool:
        """
        Is this col the middle col?
        """
        if Matrix.hasEvenCols(matrix):
            raise Exception("if this col is the middle col cannot be answered "
                            +"because the given matrix has an even number of cols")

        return self.isCol(Matrix.getMiddleCol(matrix))


    def isColNextToMiddle(self, matrix: list[list]) -> bool:
        """
        Is this coord at any of the two cols before the middle col?
        """
        return self.getCol() in Matrix.getColsNextToMiddle(matrix)


    def isRowNextToMiddle(self, matrix: list[list]) -> bool:
        """
        Is this coord at any of the two rows before the middle row?
        """
        return self.getRow() in Matrix.getRowsNextToMiddle(matrix)


    def isTopLeft(self) -> bool:
        """
        Is the coord at the top-left?
        """
        return self.isFirstCol() and self.isFirstRow()


    def isTopRight(self, matrix: list[list]) -> bool:
        """
        Is the coord at the top-right?
        """
        return self.isLastCol(matrix) and self.isFirstRow()


    def isBottomLeft(self, matrix: list[list]) -> bool:
        """
        Is the coord at the bottom-left?
        """
        return self.isFirstCol() and self.isLastRow(matrix)


    def isBottomRight(self, matrix: list[list]) -> bool:
        """
        Is the coord at the bottom-right?
        """
        return self.isLastCol(matrix) and self.isLastRow(matrix)

    # def isMainDiagonal(self, matrix: list[list]) -> bool:
    #     """
    #     Is this coord at the main diagonal? (from top-left to bottom-right)
    #     \
    #       \
    #         \
    #           \
    #     """



    # def isAntiDiagonal(self, matrix: list[list]) -> bool:
    #     """
    #     Is this coord at the anti diagonal? (from top-left to bottom-right)
    #           /
    #         /
    #       /
    #     /
    #     """


    @staticmethod
    def generateIsStartCoord(row: int, col: int) -> Coordinate:
        return Coordinate(row, col, isStart=True)
    
    @staticmethod
    def generateIsBeforeStartCoord() -> Coordinate:
        return Coordinate(-1, -1, isBeforeStart=True)

    
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

    def clone(self) -> Coordinate:
        return Coordinate(self.getRow(), self.getCol(), self.isStart, self.isBeforeStart)

    def __str__(self) -> str:
        flags = []
        if self.isStart:
            flags.append("isStart")
        if self.isBeforeStart:
            flags.append("isBeforeStart")
        
        flag_str = f", {', '.join(flags)}" if flags else ""
        return f"[Coordinate: [{self.row}, {self.col}]{flag_str}]"

    def __repr__(self) -> str:
        flags = []
        if self.isStart:
            flags.append("isStart")
        if self.isBeforeStart:
            flags.append("isBeforeStart")
        
        flag_str = f", {', '.join(flags)}" if flags else ""
        return f"[Coordinate: [{self.row}, {self.col}]{flag_str}]"


class Move(Enum):
    # the initial move
    _BEFORE_START = "_before-start"
    UP = "up"
    DIAGONAL_UP_RIGHT = "diagonal-up-right"
    RIGHT = "right"
    DIAGONAL_DOWN_RIGHT = "diagonal-down-right"
    DOWN = "down"
    DIAGONAL_DOWN_LEFT = "diagonal-down-left"
    LEFT = "left"
    DIAGONAL_UP_LEFT = "diagonal-up-left"



class FunctionHelper:
    
    @staticmethod
    def mapHasFunction(key: str, _map: dict[str, any]) -> bool: # type: ignore
        """
        Does the given dictionary, at the given key,
        have a function as value?
        """
        if not isinstance(_map, dict):
            raise Exception("the given map is not a dictionary")
         
        return key in _map and isfunction(_map[key])




# class VisitStrategy(Enum):
#     # the algorithm skips visited cells (default value)
#     ON_MULTIPLE_VISIT_SKIP = "on-multiple-visit-skip"
#     # the algorithm ignores visited cells 
#     # (this can use infinite recursion, so a strategy must be
#     # used to exit the algorithm upon meeting certain conditions)
#     ON_MULTIPLE_VISIT_CONTINUE = "on-multiple-visit-continue"