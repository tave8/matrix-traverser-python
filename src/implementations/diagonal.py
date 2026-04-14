# """
# Traverse in diagonal.
# """
from typing import List

from core.SimplePatternTraverser import SimplePatternTraverser
from src.components import Coordinate, Move, Matrix
from src.core.MazeTraverser import MazeTraverser


def makeDiagonalPattern(matrix: list[list]) -> SimplePatternTraverser:

    patternTraverser = SimplePatternTraverser(
        matrix,
        getNextMovesCallback=_getNextMoves,
    )

    return patternTraverser


# callback specific for this pattern problem
def _getNextMoves(st: SimplePatternTraverser,
                   prevCoord: Coordinate,
                   currCoord: Coordinate,
                   prevMove: Move) -> List[Move]:

    return [
        Move.DIAGONAL_UP_LEFT
    ]


