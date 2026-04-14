from src.components import Coordinate, Move
from src.implementations.line_pattern import makeLinePattern
from src.core.PatternTraverser import PatternTraverser


class DataToTest:
    def __init__(self,
                 patternTraverser: PatternTraverser) -> None:

        self.patternTraverser = patternTraverser


def makeAndRunLinePattern(matrix: list[list],
                         startCoord: Coordinate,
                         onlyDirection: Move) -> DataToTest:

    patternTraverser = makeLinePattern(matrix, onlyDirection)

    patternTraverser.run(startCoord)

    return DataToTest(
        patternTraverser
    )
