class Coordinate:
    """
    A cell coordinate, so row and column.
    """
    def __init__(self, row: int, col: int, isStart: bool=False, isBeforeStart: bool=False):
        self.row = row
        self.col = col
        self.isStart = isStart
        self.isBeforeStart = isBeforeStart
    
    def rowUp(self) -> Coordinate:
        """
        A row up.
        """
        return Coordinate(self.row-1, self.col)
    

    # def clone(self) -> Coordinate:
    #     """
    #     Clone the coordinate.
    #     """
    #     # note: we do not clone information about whether
    #     # the cell is or was start or before start
    #     return Coordinate(self.row, self.col, False, False)