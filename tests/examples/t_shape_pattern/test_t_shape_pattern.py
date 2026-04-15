from src.components import Coordinate, Matrix, MatrixTree
from tests.examples.t_shape_pattern.prep.helpers import makeAndRunTShapePattern


def test_simple_pass():

    matrix = [
        [ 1,    2,  3],
        [ 4,    4,  6],
        [ 7,    5,  3],
    ]

    startCoord = Coordinate(
        Matrix.getFirstRow(),
        Matrix.getFirstCol()
    )

    dataToTest = makeAndRunTShapePattern(matrix, startCoord)

    (nodeFound, ancestorsFromValue) = MatrixTree.findOneByValueFrom(
       dataToTest.patternTraverser.matrixTree,
        5,
        matrix
    )

    ancestorsFromFound = MatrixTree.findAllAncestorsOf(nodeFound)

    ancestorsFromFoundUpToK = MatrixTree.findKAncestorsOf(nodeFound, 3)

    print(len(ancestorsFromFound))

    assert len(ancestorsFromValue) == len(ancestorsFromFound)
    assert len(ancestorsFromValue) == len(ancestorsFromFoundUpToK)

    for i in range(len(ancestorsFromValue)):
        assert ancestorsFromValue[i] == ancestorsFromFound[i]
        assert ancestorsFromValue[i] == ancestorsFromFoundUpToK[i]

        ancestorValue = Matrix.getAtCoordinate(matrix, ancestorsFromValue[i].coord)
        print(ancestorValue)
