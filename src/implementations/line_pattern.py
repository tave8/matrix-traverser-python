"""
Traverse in a line_pattern.
"""

from typing import List

from src.core.PatternTraverser import PatternTraverser
from src.components import Coordinate, Move, MatrixTree


def makeLinePattern(matrix: List[List],
                    onlyDirection: Move) -> PatternTraverser:

    patternTraverser = PatternTraverser(
        matrix,
        getNextMovesCallback=_getNextMovesWrapper(onlyDirection),
    )

    return patternTraverser



def _getNextMovesWrapper(onlyDirection: Move):

    # CLOSURE FUNCTION
    # callback specific for this pattern problem
    def _getNextMoves(patternTraverser: PatternTraverser,
                      currNode: MatrixTree) -> List[Move]:


        movesMap = {
            # this must be here, because the first previous move
            # is always before start
            Move._BEFORE_START: [onlyDirection],
            # BUG FIXED: the Move enum was imported, in this file,
            # from components import Move
            # whereas in the  other file, it was imported as
            # from src.components import Move
            # python seemed to think they were two different classes?
            # SOLUTION: always qualify imports from the root,
            # and to get the IDE to not mess up the import paths
            # for you, mark the root director as the sources root (right click)
            # and unmark other folders as the sources root
            onlyDirection: [onlyDirection]
        }

        # the next moves of this cell are
        # its corresponding list values
        return movesMap[currNode.prevMove]


    return _getNextMoves
