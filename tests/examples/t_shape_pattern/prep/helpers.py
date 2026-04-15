from src.core.PatternTraverser import PatternTraverser
from src.components import Coordinate, Matrix, Move, MatrixTree
from src.implementations.t_shape_pattern import makeTShapePattern


class DataToTest:
    def __init__(self,
                 patternTraverser: PatternTraverser) -> None:

        self.patternTraverser = patternTraverser


def makeAndRunTShapePattern(matrix: list[list],
                            startCoord: Coordinate) -> DataToTest:

    patternTraverser = makeTShapePattern(matrix)

    patternTraverser.run(startCoord)


    return DataToTest(
        patternTraverser
    )

