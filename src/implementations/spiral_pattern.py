"""
Traverse in a spiral.
"""

from typing import List

from src.core.PatternTraverser import PatternTraverser
from src.components import Coordinate, Move, MatrixTree


def makeSpiralPattern(matrix: List[List]) -> PatternTraverser:

    patternTraverser = PatternTraverser(
        matrix,
        getNextMovesCallback=_getNextMovesWrapper(),
    )

    return patternTraverser



def _getNextMovesWrapper():

    # CLOSURE FUNCTION
    # callback specific for this pattern problem
    def _getNextMoves(st: PatternTraverser, currNode: MatrixTree) -> List[Move]:


        movesMap = {
            Move._BEFORE_START: [Move.RIGHT],
            Move.DOWN: [Move.DOWN, Move.LEFT],
            Move.RIGHT: [Move.RIGHT, Move.DOWN],
            Move.LEFT: [Move.LEFT, Move.UP],
            Move.UP: [Move.UP, Move.RIGHT]
        }

        # the next moves of this cell are
        # its corresponding list values
        return movesMap[currNode.prevMove]


    return _getNextMoves
