"""
Pattern Traverser, built on top of the Matrix Traverser Engine.
"""
from typing import List


from inspect import isfunction
from collections.abc import Callable
from src.core.MatrixTraverser import MatrixTraverser
from src.components import Coordinate, Matrix, Move
from src.exceptions.ExpectedUserCallbackError import ExpectedUserCallbackError


class PatternTraverser(MatrixTraverser):
    """
    Simple Pattern Traverser.
    Traverses a simple line_pattern.
    """

    def __init__(self,
                 matrix: list[list],
                 getNextMovesCallback: Callable[[PatternTraverser, Coordinate, Coordinate, Move], List[Move]],
                 userState=None) -> None:

        # callback must be a function
        if userState is None:
            userState = {}

        if not isfunction(getNextMovesCallback):
            raise ExpectedUserCallbackError(getNextMovesCallback)

        # ************ START *********************
        # these logical block must go together

        super().__init__(
            matrix,
            {},
            userState
        )

        simplePatternCallbackMap = PatternTraverser._getSimplePatternCallbackMap(self)
        self._setCallbackManager(simplePatternCallbackMap)

        # ********************END *************************
        self.getNextMovesCallback = getNextMovesCallback



    def run(self, startCoord: Coordinate) -> None:
        """
        Run the pattern.
        """
        self.traverseMatrix(startCoord)


    @staticmethod
    def _getNextMoves(patternTraverser: PatternTraverser) -> Callable[[PatternTraverser, Coordinate, Coordinate, Move], List[Move]]:

        # CLOSURE FUNCTION: this will be run directly
        # by the Matrix Traversal Engine
        def _getNextMovesWrapper(_matrixTraverser: MatrixTraverser,
                                  prevCoord: Coordinate,
                                  currCoord: Coordinate,
                                  prevMove: Move) -> List[Move]:

            # here you can define custom "next moves" logic
            # before, after, or based on the user-provided next moves

            # user-defined next moves.
            return patternTraverser.getNextMovesCallback(patternTraverser,
                                                         prevCoord,
                                                         currCoord,
                                                         prevMove)


        return _getNextMovesWrapper


    @staticmethod
    def _getSimplePatternCallbackMap(patternTraverser: PatternTraverser) -> dict[str, Callable]:

        return {
            "getNextMoves": PatternTraverser._getNextMoves(patternTraverser)
        }

