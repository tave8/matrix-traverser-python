from collections.abc import Callable
from src.helpers import FunctionHelper
from src.components import Coordinate, Move, Moves, Matrix, MatrixTree
from src.exceptions.DuringUserCallbackError import DuringUserCallbackError


class MatrixTraverser:
    """
    The Matrix Traverser Engine.
    """

    def __init__(self, 
                 matrix: list[list],
                 callbackMap=None,
                 userState=None):
        
        if callbackMap is None:
            callbackMap = {}
        if userState is None:
            userState = {}

        self.matrix = matrix
        self.visited = Matrix.generateVisitedMatrixFrom(matrix)
        self.stateManager = StateManager(userState)
        self.callbackManager = CallbackManager(callbackMap)
        # this will be set as soon as the user runs traverseMatrix
        # NOTE: this is a dummy tree: you 
        self.matrixTree: MatrixTree = MatrixTree.makeDummyNode()


    def _setCallbackManager(self, callbackMap: dict):
        """
        Set the Callback Manager instance manually,
        from a callback map. Careful: this manual setting 
        should be only for proven reasons. 
        """
        self.callbackManager = CallbackManager(callbackMap)


    def traverseMatrix(self, startCoord: Coordinate) -> None:
        """
        Main user-facing method to run the matrix traversal algorithm. 
        """

        StateManager._setStartCoordinate(self, startCoord)
        beforeStartCoord = Coordinate.generateIsBeforeStartCoord()

        self.__traverse(
            currCoord=startCoord,
            prevCoord=beforeStartCoord,
            prevMove=Move._BEFORE_START,
            parentNode=None
        ) 
    

    def __traverse(self, 
                  currCoord: Coordinate, 
                  prevCoord: Coordinate, 
                  prevMove: Move,
                  parentNode: MatrixTree | None) -> None:
        """
        The core algorithm: Traverses the matrix.
        """


        if self.stateManager.state["wasEnded"]:
            return 

        # if you can end the algorithm now
        # if CallbackManager.canEnd(self, prevCoord, currCoord, prevMove):
        #     # self.callbackManager.onEnd()
        #     return 

        # if this cell does not exist (out of matrix)
        if not Matrix.isInsideMatrix(self.matrix, currCoord):
            return


        # CallbackManager.beforeVisit(self, prevCoord, currCoord, prevMove)

        currentCellInfo = {
            "prevCoord": prevCoord,
            "currCoord": currCoord,
            "prevMove": prevMove,
            "prevValue": Matrix.getAtCoordinate(self.matrix, prevCoord, ignoreIfBeforeStart=True),
            "currValue": Matrix.getAtCoordinate(self.matrix, currCoord)
        }

        # we add this cell as visited as a default,
        # we must remove it when necessary
        self.stateManager.state["movesHistory"].append(currentCellInfo)


        wasVisited = Matrix.isVisited(self.visited, currCoord)

        # if this cell has been visited
        if wasVisited:

            # if CallbackManager.onMultipleVisitMustStop(self, prevCoord, currCoord, prevMove):
                # if the user does not want to consider
                # cells that have been already visited, we must
                # pop the cell we just added 
                self.stateManager.state["movesHistory"].pop()
                # ... operations when cell is already visited...
                return 
        
        # because skipping a visited cell is left to the user,
        # we don't know if, when we get here, that cell will have 
        # been visited for the first time or not. so we must do a check
        if not wasVisited:

            # if self.callbackManager.canVisit(prevCoordinate, currCoord, prevMove):

            # because we promise to only give the "movesHistory"
            # that means we must pop the one we just added, and then 
            # add it back right after the callback
            # self.stateManager.state["movesHistory"].pop()

            # CallbackManager.beforeFirstVisit(self, prevCoord, currCoord, prevMove)

            # self.stateManager.state["movesHistory"].append(currentCellInfo)


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


        # ********************************************
        # ****** START: MATRIX TREE OPERATIONS ******** 

        # *** STEP 1: initialize root if not exists
        # if there's no parent node, it means 
        # we are at the current node wanting to be root
        if parentNode is None:
            # set the matrix tree
            self.matrixTree = MatrixTree(
                parent=None,
                coord=currCoord,
                prevMove=Move._BEFORE_START,
                isRoot=True
            )
        
        # *** STEP 2: create current node or pick the root as current node
        # if we are at the current node being the root,
        # then at STEP 1 we have created the root itself.
        # now in STEP 2 we say, "if we are at the root,
        # the current node is the root, otherwise we are
        # at whatever other current node"
        currNode = self.matrixTree if parentNode is None else MatrixTree(
            parent=parentNode,
            coord=currCoord,
            prevMove=prevMove
        )

        # *** STEP 3: append the child to the parent
        # if the parent node does not exist, 
        # it means we are currently at the root,
        # and at the root, we simply set the matrix tree to be 
        # the root node itself.
        # if we are not at the root, and so a parent node exists,
        # then we append it to the list of children, and this is 
        # actually the standard operation
        if parentNode is not None:
            parentNode.children.append(currNode)
        
        # ****** END: MATRIX TREE OPERATIONS ******** 
        # ********************************************


        # print(Matrix.getAtCoordinate(self.matrix, currNode.currCoord), currNode.currCoord)

        # GET THE MOVES OF THIS CELL
        nextMoves = CallbackManager.getNextMoves(self, prevCoord, currCoord, prevMove)

        # print(Matrix.getAtCoordinate(self.matrix, currNode.coord), Matrix.getAtCoordinate(self.matrix, currCoord))

        # MOVE THROUGH THE MOVES
        # move in the order that was specified
        for nextMove in nextMoves:

            if nextMove == Move.UP:
                # up
                if CallbackManager.canMoveTo(self, currCoord.up(), prevCoord, currCoord, prevMove, currNode):
                    # CALLBACK IDEA: beforeMove
                    self.__traverse(currCoord.up(), currCoord, Move.UP, currNode)
                    # CALLBACK IDEA: afterMove

            elif nextMove == Move.DIAGONAL_UP_RIGHT:
                # diagonal up right
                if CallbackManager.canMoveTo(self, currCoord.diagonalUpRight(), prevCoord, currCoord, prevMove, currNode):
                    self.__traverse(currCoord.diagonalUpRight(), currCoord, Move.DIAGONAL_UP_RIGHT, currNode)

            elif nextMove == Move.RIGHT:
                # right
                if CallbackManager.canMoveTo(self, currCoord.right(), prevCoord, currCoord, prevMove, currNode):
                    self.__traverse(currCoord.right(), currCoord, Move.RIGHT, currNode)

            elif nextMove == Move.DIAGONAL_DOWN_RIGHT:
                # diagonal down right
                if CallbackManager.canMoveTo(self, currCoord.diagonalDownRight(), prevCoord, currCoord, prevMove, currNode):
                    self.__traverse(currCoord.diagonalDownRight(), currCoord, Move.DIAGONAL_DOWN_RIGHT, currNode)

            elif nextMove == Move.DOWN:
                # down
                if CallbackManager.canMoveTo(self, currCoord.down(), prevCoord, currCoord, prevMove, currNode):
                    self.__traverse(currCoord.down(), currCoord, Move.DOWN, currNode)

            elif nextMove == Move.DIAGONAL_DOWN_LEFT:
                # diagonal down left
                if CallbackManager.canMoveTo(self, currCoord.diagonalDownLeft(), prevCoord, currCoord, prevMove, currNode):
                    self.__traverse(currCoord.diagonalDownLeft(), currCoord, Move.DIAGONAL_DOWN_LEFT, currNode)

            elif nextMove == Move.LEFT:
                # left
                if CallbackManager.canMoveTo(self, currCoord.left(), prevCoord, currCoord, prevMove, currNode):
                    self.__traverse(currCoord.left(), currCoord, Move.LEFT, currNode)

            elif nextMove == Move.DIAGONAL_UP_LEFT:
                # diagonal up left 
                if CallbackManager.canMoveTo(self, currCoord.diagonalUpLeft(), prevCoord, currCoord, prevMove, currNode):
                    self.__traverse(currCoord.diagonalUpLeft(), currCoord, Move.DIAGONAL_UP_LEFT, currNode)


        # This is the moment where ALL the recursions and operations
        # of the successors of the current node have been exhausted.
        # This is exactly the moment where we trigger the relevant callback
        # that handles exactly that timing.
        CallbackManager.afterAllFutureMoves(self, currNode)



    def getMovesHistory(self) -> list[dict]:
        """
        Get the moves history, which is the list containing pairs of
        previous and current cell, with their values and previous move,
        of the last traversal done.
        """
        return self.stateManager.state["movesHistory"]
    

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
    def canMoveTo(mt: MatrixTraverser, 
                desiredCoordinate: Coordinate, 
                prevCoordinate: Coordinate, 
                currCoordinate: Coordinate,
                prevMove: Move,
                currNode: MatrixTree) -> bool:
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
        if FunctionHelper.mapHasFunction("canMoveTo", mt.callbackManager.callbackMap):
            # this callback can be any user-defined callback,
            # or even one defined from a problem-specific traversal engine,
            # for example the Maze Traverser
            canMoveToCallback: Callable[[MatrixTraverser, Coordinate, Coordinate, Coordinate, Move, MatrixTree], bool] = (
                mt.callbackManager.callbackMap["canMoveTo"]
            )

            try:
                userWantsMove: bool | None = canMoveToCallback(mt,
                                                                desiredCoordinate, 
                                                                prevCoordinate, 
                                                                currCoordinate,
                                                                prevMove,
                                                                currNode)
            except Exception as e:
                raise DuringUserCallbackError(canMoveToCallback) from e

            # if the user did not return, it means 
            # it's happy with this cell moving in the desired direction 
            if userWantsMove is None:
                return True
            
            # check if the returned value is correct
            if not isinstance(userWantsMove, bool):
                raise Exception("userWantsMove must be of type bool")
            
            return userWantsMove

        # if the user did not specify the callback, 
        # we assume every direction is good to move to
        return True


    # @staticmethod
    # def beforeFirstVisit(mt: MatrixTraverser, 
    #                      prevCoord: Coordinate, 
    #                      currCoord: Coordinate, 
    #                      prevMove: Move) -> None:
    #     """
    #     Before first visit of a cell, run this callback.
    #     """

    #     # run the user-defined callback, if exists
    #     if FunctionHelper.mapHasFunction("beforeFirstVisit", mt.callbackManager.callbackMap):
    #         beforeFirstVisitCallback = mt.callbackManager.callbackMap["beforeFirstVisit"]

    #         beforeFirstVisitCallback(mt, prevCoord, currCoord, prevMove)
        
        # if the user did not specify a callback,
        # we don't have to do anything particular here


    # @staticmethod
    # def beforeVisit(mt: MatrixTraverser, 
    #                     prevCoordinate: Coordinate, 
    #                     currCoordinate: Coordinate, 
    #                     prevMove: Move) -> None:
    #     """
    #     Before ANY visit of a cell, run this callback.
    #     """

    #     # run the user-defined callback, if exists
    #     if FunctionHelper.mapHasFunction("beforeVisit", mt.callbackManager.callbackMap):
    #         mt.callbackManager.callbackMap["beforeVisit"](mt, 
    #                                                         prevCoordinate, 
    #                                                         currCoordinate,
    #                                                         prevMove)
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


    @staticmethod
    def afterAllFutureMoves(mt: MatrixTraverser,
                            currNode: MatrixTree) -> None:
        """
        After all the moves of the future nodes of the current node
        will have completed their moves, the Engine will trigger this callback.

        How is this achieved? Because in the Engine, the call
        of this callback is positioned AFTER the traversal recursive call,
        it means that we won't be calling this callback before all of
        those recursive calls will have been completed.

        In other words, as long as any "successor" node/cell
        of the current node/cell has more traversals to run,
        we will continue with these until there are no more left.

        In practice, the current node passed to this callback,
        and therefore also the timing at which this callback gets called,
        will allow the user to perform operations based on future moves
        of ANY successor of the given node/cell,
        ONLY IF EVERY path of the successor nodes of the current node
        has been exhausted.

        In short, the current node passed to this callback can know
        the history of the future and can therefore do/undo stuff.

        This callback will get triggered the moment AFTER ALL
        the future paths of the successor nodes
        of the current node will have been exhausted,
        and the afterAllFutureMoves of those successor nodes
        will also have been completed.

        """

        # run the user-defined callback, if exists
        if FunctionHelper.mapHasFunction("afterAllFutureMoves", mt.callbackManager.callbackMap):

            afterAllFutureMovesCallback: Callable[[MatrixTraverser, MatrixTree], bool] = mt.callbackManager.callbackMap["afterAllFutureMoves"]

            try:

                afterAllFutureMovesCallback(mt, currNode)

            except Exception as e:
                raise DuringUserCallbackError(afterAllFutureMovesCallback) from e





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
    
    # @staticmethod
    # def onMultipleVisitMustStop(mt: MatrixTraverser, 
    #                             prevCoordinate: Coordinate, 
    #                             currCoordinate: Coordinate, 
    #                             prevMove: Move) -> bool:
    #     """
    #     Defines the logic of whether a cell that is visited multiple times
    #     must be skipped. Wrong configuration of this callback
    #     can result in non termination of the algorithm, which is 
    #     why the primary semantics points to skip instead of continuing.
        
    #     If we don't skip (so if we continue) it probably means 
    #     we're more interested in exploring the matrix rather than
    #     using some cell value. This behavior is desirable 
    #     in the following cases, for example: 
        
    #     - we don't know where a certain target cell is, and therefore
    #     we don't really care about whether a cell was visited or not
        
    #     - we must ignore that this cell was visited because we might
    #     need to go back to certain places of the matrix, and therefore 
    #     we have to inevitably pass through some visited cells, and we 
    #     don't care that they were visited
    #     """

    #     # run the user-defined callback, if exists
    #     if FunctionHelper.mapHasFunction("onMultipleVisitMustStop", mt.callbackManager.callbackMap):
    #         mustStop: bool | None = mt.callbackManager.callbackMap["onMultipleVisitMustStop"](mt, 
    #                                                                                     prevCoordinate, 
    #                                                                                     currCoordinate,
    #                                                                                     prevMove)
    #         # if the user did not return, it means 
    #         # it's happy with this cell moving being skipped, 
    #         # if it's been visited 
    #         if mustStop is None:
    #             return True
            
    #         # check if the returned value is correct
    #         if not isinstance(mustStop, bool):
    #             raise Exception("stop must be of type bool")
            
    #         return mustStop
        
    #     # default behavior is, we always skip visited cells
    #     # in other words, in this case the algorithm cannot 
    #     # "jump" or ignore visited cells, which means that 
    #     # the algorithm might get stuck in a sort of "fence"
    #     # where it will not visit visited cells, and therefore
    #     # it will not explore other cells "on the other side" 
    #     # of the visited cells. this behavior is normal, if 
    #     # if the "explorer" behaviour is not desired or needed. 
    #     return True
    

    # @staticmethod
    # def canEnd(mt: MatrixTraverser, 
    #             prevCoord: Coordinate, 
    #             currCoord: Coordinate,
    #             prevMove: Move) -> bool:
    #     """
    #     Can I end the algorithm right now?
        
    #     By default the algorithm will terminate only 
    #     when all cells will be visited. We can prevent that 
    #     and decide the end of the algorithm.
    #     """

    #     # run the user-defined callback, if exists
    #     if FunctionHelper.mapHasFunction("canEnd", mt.callbackManager.callbackMap):
    #         canEndCallback = mt.callbackManager.callbackMap["canEnd"]
            
    #         userSaysCanEnd: bool | None = canEndCallback(mt, prevCoord, currCoord, prevMove)
            
    #         # if the user did not return, it means 
    #         # it's happy with not ending the algorithm
    #         if userSaysCanEnd is None:
    #             return False
            
    #         # check if the returned value is correct
    #         if not isinstance(userSaysCanEnd, bool):
    #             raise Exception("userSaysCanEnd must be of type bool")

    #         if userSaysCanEnd:
    #             mt.stateManager.state["wasEnded"] = True
            
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
            # the algorithm was ended?
            "wasEnded": False,
            # the cells that were visited so far, 
            # which does not include the one we're about to visit
            "movesHistory": []
        }
        # dummy coordinate, will be overwritten soon
        self.startCoordinate: Coordinate = Coordinate(-1, -1, isStart=True)
    
    # @staticmethod
    # def addToVisitedC(mt: MatrixTraverser, coord: Coordinate):
    #     mt.stateManager.state["movesHistory"].append(coord)

    # @staticmethod
    # def pop(mt: MatrixTraverser, coord: Coordinate):
    #     mt.stateManager.state["movesHistory"].append(coord)


    @staticmethod
    def _setStartCoordinate(mt: MatrixTraverser, coord: Coordinate): 
        # make sure this coordinate is marked as
        # isStart, so that the user doesn't have to
        coord.isStart = True       
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

    @staticmethod
    def setWasEnded(mt: MatrixTraverser, wasEnded: bool) -> None:
        """
        Set that the algorithm will end immediately.
        """
        mt.stateManager.state["wasEnded"] = wasEnded
    

