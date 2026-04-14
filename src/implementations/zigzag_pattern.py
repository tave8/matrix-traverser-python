"""
Traverse in a zigzag.
"""

from typing import List

from src.core.PatternTraverser import PatternTraverser
from src.components import Coordinate, Move


def makeZigzagPattern(matrix: List[List]) -> PatternTraverser:

    patternTraverser = PatternTraverser(
        matrix,
        getNextMovesCallback=_getNextMovesWrapper(),
    )

    return patternTraverser



def _getNextMovesWrapper():

    # CLOSURE FUNCTION
    # callback specific for this pattern problem
    def _getNextMoves(st: PatternTraverser,
                       prevCoord: Coordinate,
                       currCoord: Coordinate,
                       prevMove: Move) -> List[Move]:


        movesMap = {
            Move._BEFORE_START: [Move.DOWN, Move.RIGHT],
            Move.DOWN: [Move.DIAGONAL_UP_RIGHT, Move.DIAGONAL_DOWN_LEFT, Move.DOWN],
            Move.DIAGONAL_UP_RIGHT: [Move.DIAGONAL_UP_RIGHT, Move.RIGHT, Move.DOWN],
            Move.RIGHT: [Move.DIAGONAL_UP_RIGHT, Move.DIAGONAL_DOWN_LEFT, Move.RIGHT],
            Move.DIAGONAL_DOWN_LEFT: [Move.DIAGONAL_DOWN_LEFT, Move.DOWN, Move.RIGHT]
        }

        # the next moves of this cell are
        # its corresponding list values
        return movesMap[prevMove]


    return _getNextMoves
