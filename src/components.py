"""
The building blocks.
"""

from enum import Enum






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
