"""
Pattern Traverser, built on top of the Matrix Traverser Engine.
"""
from typing import List

from core.MazeTraverser import MazeTraverser


from inspect import isfunction
from collections.abc import Callable
from src.core.MatrixTraverser import MatrixTraverser, StateManager
from src.components import Coordinate, Matrix, Move
from src.exceptions.ExpectedUserCallbackError import ExpectedUserCallbackError


class SimplePatternTraverser(MatrixTraverser):
    """

    """

    def __init__(self,
                 matrix: list[list],
                 getNextMovesCallback: Callable[[SimplePatternTraverser, Coordinate, Coordinate, Move], List[Move]],
                 userState: dict = {}) -> None:

        # callback must be a function
        if not isfunction(getNextMovesCallback):
            raise ExpectedUserCallbackError(getNextMovesCallback)

        # ************ START *********************
        # these logical block must go together

        super().__init__(
            matrix,
            {},
            userState
        )

        simplePatternCallbackMap = SimplePatternTraverser._getSimplePatternCallbackMap(self)
        self._setCallbackManager(simplePatternCallbackMap)

        # ********************END *************************

        self.getNextMovesCallback = getNextMovesCallback


    def run(self, startCoord: Coordinate) -> None:
        """
        Run the pattern.
        """
        self.traverseMatrix(startCoord)


    @staticmethod
    def _getNextMoves(patternTraverser: SimplePatternTraverser) -> Callable[[SimplePatternTraverser, Coordinate, Coordinate, Move], List[Move]]:

        # CLOSURE FUNCTION: this will be run directly
        # by the Matrix Traversal Engine
        def _getNextMovesWrapper(_matrixTraverser: MatrixTraverser,
                                  prevCoord: Coordinate,
                                  currCoord: Coordinate,
                                  prevMove: Move) -> List[Move]:

            # user-defined next moves.
            return patternTraverser.getNextMovesCallback(patternTraverser,
                                                         prevCoord,
                                                         currCoord,
                                                         prevMove)


        return _getNextMovesWrapper


    @staticmethod
    def _getSimplePatternCallbackMap(patternTraverser: SimplePatternTraverser) -> dict[str, Callable]:

        return {
            "getNextMoves": SimplePatternTraverser._getNextMoves(patternTraverser)
        }

