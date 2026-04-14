# from src.components import Matrix, Move, Coordinate, MatrixTree
# from tests.examples.line_pattern.prep.helpers import makeAndRunLinePattern
# from tests.examples.line_pattern.prep.assertions import *
#
#
# def test_right():
#
#     startCoord = Coordinate(
#         Matrix.getFirstRow(),
#         Matrix.getFirstCol(),
#     )
#
#     dataToTest = makeAndRunLinePattern([
#         [1, 2, 3],
#         [4, 5, 6],
#         [7, 8, 9],
#     ], startCoord, Move.DOWN)
#
#     # assert that the node found has
#     # the value we were looking for
#     (nodeFound, ancestors) = MatrixTree.findOneByValueFrom(
#         dataToTest.patternTraverser.matrixTree,
#         7,
#         dataToTest.patternTraverser.matrix
#     )
#
#     # assert that the number of ancestors is 2
#     # assert that the ancestors are 1 and 4
#
#
