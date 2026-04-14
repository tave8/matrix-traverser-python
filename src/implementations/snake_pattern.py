"""
Traverse in a snake.

|  |--|  |--|
|  |  |  |  |
|__|  |__|  |

"""

from typing import List

from src.core.PatternTraverser import PatternTraverser
from src.components import Coordinate, Move


def makeSnakePattern(matrix: List[List]) -> PatternTraverser:

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
            Move._BEFORE_START: [Move.DOWN],
            Move.DOWN: [Move.DOWN, Move.RIGHT],
            Move.RIGHT: [Move.UP, Move.DOWN],
            Move.UP: [Move.UP, Move.RIGHT]
        }

        # the next moves of this cell are
        # its corresponding list values
        return movesMap[prevMove]


    return _getNextMoves
