"""
The building blocks.
"""

from enum import Enum
from typing import Any



class MatrixTree:
    """
    A tree data structure where 
    each node has N children.
    """
    
    def __init__(self, 
                 parent: MatrixTree | None,
                 coord: Coordinate,
                 # prevCoord: Coordinate,
                 prevMove: Move,
                 isRoot=False,
                 isDummy=False) -> None:
        """
        Matrix Tree.
        """

        self.parent = parent
        self.isRoot = isRoot

        self.children: list[MatrixTree] = [] 
        self.coord = coord
        # self.prevCoord = prevCoord
        self.prevMove: Move = prevMove
        # is this a dummy tree? a dummy tree is used exclusively
        # for initialization reasons and shall be replaced, literally
        # overwritten, when the user runs the traversal algorithm
        self.isDummy = isDummy

    
    @staticmethod
    def findKAncestorsOf(startNode: MatrixTree, k: int) -> list[MatrixTree]:
        """
        Given a node, find up to K ancestors of the given node.
        Why up to k? Because it's not guaranteed that exactly
        k ancestors will be found.

        The ancestors order will be from most distant to most direct.
        The most direct ancestor is simply the parent of the given node.
        The most distant ancestor is the k-th ancestor,
        if such a k-th ancestor exists.

        ```

        Example:
            start node = 5

            k = 3

            actual tree path (ignoring other nodes):

                root -> 1 -> 2 -> 3 -> 4 -> 5 -> 6
                             ^              ^
                             |              |
                        3rd ancestor     start node

            result list = 2 -> 3 -> 4

        ```

        Note:
        -  k = -1 has a special meaning of "find all ancestors".
        """
        
        if not isinstance(k, int):
            raise Exception(f"the number of ancestors k must be an integer, got {type(k)} instead")

        if k <= -2:
            raise Exception(f"don't know how to interpret value {k} for k number of ancestors")

        # -1 means, find all ancestors
        if k == -1:
            ancestorsReversed = []
            currParent = startNode.parent

            while currParent is not None:
                ancestorsReversed.append(currParent)
                currParent = currParent.parent

            return list(reversed(ancestorsReversed))


        if k < 0:
            raise Exception("internal error. it was assumed that k (number of ancestors) was >= 0")


        # from now on, we are certain that k >= 0
        count = k
        ancestorsReversed = []
        currParent = startNode.parent

        while count > 0 and currParent is not None:
            ancestorsReversed.append(currParent)
            currParent = currParent.parent
            count -= 1

        return list(reversed(ancestorsReversed))
        


    @staticmethod
    def findAllAncestorsOf(startNode: MatrixTree) -> list[MatrixTree]:
        """
        Finds all ancestors of the given node.
        """
        return MatrixTree.findKAncestorsOf(startNode, -1)


    @staticmethod
    def findOneByValueFrom(startNode: MatrixTree,  
                                    targetValue: Any,
                                    matrix: list[list]) -> tuple[MatrixTree | None, list[MatrixTree]]:
        """
        Find a matrix tree node where the value of the cell
        is the same as the input, starting from an arbitrary node.
        That means, you can start from the root (matrix tree)
        if you wish so, or you can start from anywhere else in the tree.

        Here are some notes about the internal workings.
        Because adding the ancestor happens BEFORE
        the recursive call, the ancestor list will effectively already 
        be ordered from ROOT node to MOST DIRECT ANCESTOR node,
        which is simply the PARENT node of the target node.

        Example:
        1. The target node has value "E"
        2. The ancestors, from the root, are: S -> 1 -> 2 -> 3 (that means, after 3 we have E)
        3. The ancestor list will therefore contain 
        exactly the nodes S -> 1 -> 2 -> 3
        """

        nodeFound: MatrixTree | None = None
        # collect the ancestors of the node found
        ancestors: list[MatrixTree] = []

        # START RECURSIVE FUNCTION *******************************

        def find(currNode: MatrixTree | None) -> MatrixTree | None:
            # POSSIBLE RETURN 1 (None -> it's the base case = the parent is a leaf node)
            if currNode is None:
                return None
            
            # we found the target node
            if Matrix.getAtCoordinate(matrix, currNode.coord) == targetValue:
                # POSSIBLE RETURN 2
                # we found the target node,
                # therefore the caller will now get this node
                # at its return value
                return currNode 
            
            # the current node is the direct ancestor
            # of its children
            ancestors.append(currNode)

            # **********************************
            # iterate through the children
            # using depth-first traversal

            # we assume that the node was not found
            # if the node is found as any child 
            # at any depth below this current node,
            # we update it
            actualNodeFound = None
            
            # was the target node found at any child
            # (therefore, at any depth)
            # of the current node? (recursive step)
            # if yes, we stop the search immediately,
            # which translates to exiting the loop
            for child in currNode.children:
                # to understand the return value of this
                # recursive call, look at the return values 
                # of this recursive function itself. 
                # here the possible returns:
                #  POSSIBLE RETURN   |          REASON
                # --------------------------------------- 
                #     None                  
                #     node
                #     node or None

                maybeTargetNode = find(child)
                
                if maybeTargetNode:
                    actualNodeFound = maybeTargetNode
                    # we've found the target node at any depth
                    # of this child, so we can exit the loop
                    break
            
            # if we have not found the target node
            # as any child at any depth of the current node,
            # we remove the current node itself
            # the result is that in the ancestors list what will remain
            # are the ancestors of the target node,
            # if the target node was found 
            if actualNodeFound is None:
                ancestors.pop()
            
            # **********************************

            # POSSIBLE RETURN 3: None or node
            # at the current node, if any node was found 
            # at any depth in the children,
            # and therefore returned from the recursive calls,
            # it will be returned to the caller of this function
            return actualNodeFound
        
        # END RECURSIVE FUNCTION *******************************
        
        # this call will give you back the target node,
        # if it existed, or none, if it didn't
        nodeFound = find(startNode)

        return (nodeFound, ancestors)


    # def find 

    @staticmethod
    def makeDummyNode() -> MatrixTree:
        """
        Returns a dummy MatrixTree, which is just needed for internal reasons,
        like "type coherency" and initialization reasons.
        It shall not be used truly, and it should be replaced immediately
        when the user calls the run method on the matrix. 
        """
        return MatrixTree(
            None, 
            Coordinate(-1, -1), 
            # Coordinate(-1, -1),
            prevMove=Move._BEFORE_START,
            isDummy=True
        )


    # def __str__(self) -> str:
    #     return f"<MatrixTree>"

    # def __repr__(self) -> str:
    #     pass


class Matrix:

    # IS VISITED ***********************

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


    # ADDED TO BFS QUEUE *******************

    @staticmethod
    def isAddedToBFSQueue(queueMatrix: list[list[int]],
                          coord: Coordinate) -> bool:
        """
        Checks if the cell at the given coordinate
        has been added to the BFS queue or not.
        """
        # check that given row and col exist in matrix?
        return queueMatrix[coord.getRow()][coord.getCol()] == 1


    @staticmethod
    def markAsAddedToBFSQueue(queueMatrix: list[list[int]],
                              coord: Coordinate) -> None:
        """
        Mark the cell at the given coordinates as added
        to the BFS (breadth-first search) queue.
        """
        val = queueMatrix[coord.getRow()][coord.getCol()]

        if val != 0:
            raise Exception(f"cell value had to be 0 when adding "
                            + f"cell/node to the BFS queue "
                            +f"for the first time, got {val} instead."
                            +f"this might mean that this cell/node was"
                            +f"already added to the BFS queue?")

        queueMatrix[coord.getRow()][coord.getCol()] = 1

    # @staticmethod
    # def isAMatrix(matrix: list[list]) -> bool:
    #     """
    #     Is this a matrix? The matrix must have
    #     the exact same number of rows and columns.
    #     """
    #     # FIX 
    #     return False


    @staticmethod
    def getAtCoordinate(matrix: list[list], 
                        coord: Coordinate,
                        ignoreIfBeforeStart: bool=False):
        """
        Get the cell value in the matrix, at the given coordinate.
        """

        # if the coordinate is before start 
        # and we do not ignore that
        if coord.isBeforeStart and not ignoreIfBeforeStart:
            raise Exception("cannot access 'before to start' coordinate; "
                            +"you've specified to not ignore it")

        # if the coordinate is before start and we are okay
        # ignoring it, return the coordinate itself, not knowing
        # what value would make sense to return
        if coord.isBeforeStart and ignoreIfBeforeStart:
            return coord

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
    def generateAddedToBFSQueueMatrixFrom(matrix: list[list]) -> list[list[int]]:
        """
        Generate a "added to BFS queue" matrix
        to mark the cells as added to the queue or not.
        Useful when working with BFS (breadth-first search).
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




class Coordinate:
    """
    A cell coordinate, so row and column.
    """
    def __init__(self, row: int, col: int, isStart: bool=False, isBeforeStart: bool=False):
        self.row = row
        self.col = col
        self.isStart = isStart
        self.isBeforeStart = isBeforeStart


    @staticmethod
    def ofMove(currCoord: Coordinate, move: Move) -> Coordinate:
        """
        Returns a new coordinate based on the given
        coordinate and the move of that given coordinate.

        Example 1:
            currCoord: Coordinate[0, 0]
            move: RIGHT

            -> Coordinate[0, 1]


        Example 2:
            currCoord: Coordinate[5, 3]
            move: UP

            -> Coordinate[4, 3]


        Example 3:
            currCoord: Coordinate[2, 1]
            move: DIAGONAL DOWN LEFT

            -> Coordinate[3, 0]

        """

        if move == Move.UP:
            return currCoord.up()
        if move == Move.DIAGONAL_UP_RIGHT:
            return currCoord.diagonalUpRight()
        if move == Move.RIGHT:
            return currCoord.right()
        if move == Move.DIAGONAL_DOWN_RIGHT:
            return currCoord.diagonalDownRight()
        if move == Move.DOWN:
            return currCoord.down()
        if move == Move.DIAGONAL_DOWN_LEFT:
            return currCoord.diagonalDownLeft()
        if move == Move.LEFT:
            return currCoord.left()
        if move == Move.DIAGONAL_UP_LEFT:
            return currCoord.diagonalUpLeft()

        raise Exception(f"the move {move} was not mapped. "
                        +"are you sure it exists and that it was correctly mapped?")


    def hasSameCoordinate(self, otherCoord: Coordinate) -> bool:
        return self.getRow() == otherCoord.getRow() and self.getCol() == otherCoord.getCol()


    def isDistant(self, otherCoord: Coordinate, distance: int) -> bool:
        """
        Verify if a cell has a k distance from given cell. 
        The definition of distance is, the direct number of moves
        to reach a cell from a starting cell.
        Therefore, adjacent cells are cells whose distance is 1.
        """
        if self.isBeforeStart or otherCoord.isBeforeStart:
            raise Exception("cannot compare the 'before start' coordinate "
                            +"for distance", self, otherCoord)
        
        return max(
            abs(self.getRow() - otherCoord.getRow()),
            abs(self.getCol() - otherCoord.getCol())
        ) == distance
    

    def isAdjacent(self, otherCoord: Coordinate) -> bool:
        """
        Verify if the cell is adjacent to the given cell.
        """
        return self.isDistant(otherCoord, 1)
    

    @staticmethod
    def areAdjacent(coord1: Coordinate, coord2: Coordinate) -> bool:
        return coord1.isAdjacent(coord2)


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
    
    # -----------------------------------
    # DIRECTIONS/MOVES

    def upBy(self, k: int) -> Coordinate:
        return Coordinate(self.getRow()-k, self.getCol())

    def downBy(self, k: int) -> Coordinate:
        return Coordinate(self.getRow()+k, self.getCol())
    
    def leftBy(self, k: int) -> Coordinate:
        return Coordinate(self.getRow(), self.getCol()-k)
    
    def rightBy(self, k: int) -> Coordinate:
        return Coordinate(self.getRow(), self.getCol()+k)

    def diagonalUpLeftBy(self, k: int) -> Coordinate:
        return Coordinate(self.getRow()-k, self.getCol()-k)

    def diagonalUpRightBy(self, k: int) -> Coordinate:
        return Coordinate(self.getRow()-k, self.getCol()+k)

    def diagonalDownLeftBy(self, k: int) -> Coordinate:
        return Coordinate(self.getRow()+k, self.getCol()-k)

    def diagonalDownRightBy(self, k: int) -> Coordinate:
        return Coordinate(self.getRow()+k, self.getCol()+k)

    # -----------------------------------

    def up(self) -> Coordinate:
        return self.upBy(1)

    def down(self) -> Coordinate:
        return self.downBy(1)
    
    def diagonalUpRight(self) -> Coordinate:
        return self.diagonalUpRightBy(1)

    def diagonalUpLeft(self) -> Coordinate:
        return self.diagonalUpLeftBy(1)

    def right(self) -> Coordinate:
        return self.rightBy(1)

    def left(self) -> Coordinate:
        return self.leftBy(1)
    
    def diagonalDownRight(self) -> Coordinate:
        return self.diagonalDownRightBy(1)
    
    def diagonalDownLeft(self) -> Coordinate:
        return self.diagonalDownLeftBy(1)

    # -----------------------------------

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

    # @staticmethod
    # def isDiagonalMove() -> bool:
    #     """
    #     Is this diagonal move?
    #     """

    @staticmethod
    def getAllMoves() -> list[Move]:
        return [move for move in Move]



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
