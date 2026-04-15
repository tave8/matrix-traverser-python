"""
Pattern Traverser, built on top of the Matrix Traverser Engine.
"""
from typing import List


from inspect import isfunction
from collections.abc import Callable
from src.core.MatrixTraverser import MatrixTraverser
from src.components import Coordinate, Matrix, Move, MatrixTree
from src.exceptions.ExpectedUserCallbackError import ExpectedUserCallbackError


class PatternTraverser(MatrixTraverser):
    """
    Pattern Traverser.
    """

    def __init__(self,
                 matrix: list[list],
                 getNextMovesCallback: Callable[[PatternTraverser, Coordinate, Coordinate, Move], List[Move]],
                 afterAllFutureMoves: Callable[[PatternTraverser, MatrixTree], None] = None,
                 userState=None) -> None:

        # callback must be a function
        if userState is None:
            userState = {}

        if not isfunction(getNextMovesCallback):
            raise ExpectedUserCallbackError(getNextMovesCallback)

        # afterAllFutureMoves must be either a function or None
        if not isfunction(afterAllFutureMoves) and afterAllFutureMoves is not None:
            raise ExpectedUserCallbackError(f"optional getNextMovesCallback callback must be either "
                                            +f"None or a function, got {type(afterAllFutureMoves)} instead.")

        # ************ START *********************
        # these logical block must go together

        super().__init__(
            matrix,
            {},
            userState
        )

        patternCallbackMap = PatternTraverser._getPatternCallbackMap(self)
        self._setCallbackManager(patternCallbackMap)

        # ********************END *************************
        self.getNextMovesCallback = getNextMovesCallback
        self.afterAllFutureMoves = afterAllFutureMoves



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
    def _afterAllFutureMoves(patternTraverser: PatternTraverser) -> Callable[[MatrixTraverser, MatrixTree], None]:

        # CLOSURE FUNCTION: this will be run directly
        # by the Matrix Traversal Engine
        def _afterAllFutureMovesWrapper(_matrixTraverser: MatrixTraverser,
                                        currNode: MatrixTree) -> None:

            if patternTraverser.afterAllFutureMoves is not None:
                # if this callback is not none, then it must be a function,
                # it cannot be anything else
                if not isfunction(patternTraverser.afterAllFutureMoves):
                    raise ExpectedUserCallbackError(f"optional getNextMovesCallback callback must be either "
                                                    + f"None or a function, got {type(patternTraverser.afterAllFutureMoves)} instead.")


                # run the user-defined  afterAllFutureMoves callback,
                # now that we are certain it exists
                patternTraverser.afterAllFutureMoves(patternTraverser, currNode)

        return _afterAllFutureMovesWrapper


    @staticmethod
    def _getPatternCallbackMap(patternTraverser: PatternTraverser) -> dict[str, Callable]:

        # this dict will be passed directly to the Engine,
        # so this is the callback that the Engine will call
        # at the right timing
        return {
            "getNextMoves": PatternTraverser._getNextMoves(patternTraverser),
            "afterAllFutureMoves":  PatternTraverser._afterAllFutureMoves(patternTraverser)
        }

