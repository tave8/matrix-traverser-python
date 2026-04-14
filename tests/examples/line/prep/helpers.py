from src.components import Coordinate, Move
from src.implementations.line import makeLinePattern
from src.core.SimplePatternTraverser import SimplePatternTraverser


class DataToTest:
    def __init__(self,
                 patternTraverser: SimplePatternTraverser) -> None:

        self.patternTraverser = patternTraverser


def makeAndRunLinePattern(matrix: list[list],
                         startCoord: Coordinate,
                         onlyDirection: Move) -> DataToTest:

    patternTraverser = makeLinePattern(matrix, onlyDirection)

    patternTraverser.run(startCoord)

    return DataToTest(
        patternTraverser
    )
