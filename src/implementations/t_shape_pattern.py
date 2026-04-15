"""
Traverse in a T shape.

   1
------------------->
        |
        |   2
        |
        |
        v
"""

from collections.abc import Callable
from typing import List

from src.core.PatternTraverser import PatternTraverser
from src.components import Coordinate, Move, MatrixTree, Matrix


def makeTShapePattern(matrix: List[List],
                      afterAllFutureMoves: Callable[[PatternTraverser, MatrixTree], None] = None) -> PatternTraverser:
    """
    Traverse in a T shape.
    The matrix must have an odd number of columns;
    an error will be thrown if this is not provided.
    """

    if Matrix.hasEvenCols(matrix):
        raise Exception("Matrix must have odd number of columns "
                        +"to be traversed in a T shape")

    patternTraverser = PatternTraverser(
        matrix,
        getNextMovesCallback=_getNextMovesWrapper(),
        afterAllFutureMoves=afterAllFutureMoves
    )

    return patternTraverser



def _getNextMovesWrapper():

    # CLOSURE FUNCTION
    # callback specific for this pattern problem
    def _getNextMoves(pt: PatternTraverser, currNode: MatrixTree) -> List[Move]:

        # if this is the cell right
        # at the intersection in the T shape
        # this cell must move first right, and then down
        if currNode.coord.isFirstRow() and currNode.coord.isMiddleCol(pt.matrix):
            return [
                Move.RIGHT,
                Move.DOWN
            ]

        # if this is the cell in a column in the middle,
        # it can only move down
        if currNode.coord.isMiddleCol(pt.matrix):
            return [
                Move.DOWN
            ]

        # if this is the first row, you can only move right
        if currNode.coord.isFirstRow():
            return [
                Move.RIGHT
            ]

        # for any other cell, you cannot move anywhere else
        return []


    return _getNextMoves
