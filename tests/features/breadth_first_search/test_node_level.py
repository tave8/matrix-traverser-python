from typing import List

from src.components import Coordinate, Matrix, MatrixTree, Move
from src.core.MatrixTraverser import MatrixTraverser



def test_node_level_lower_diagonal():
    matrix = [
        [1,  2,   3,  4],
        [5,  6,   7,  8],
        [9,  10, 11, 12],
        [13, 14, 15, 16]
    ]

    valuesByLevel = {
        1: 1,
        5: 2,
        6: 2,
        9: 3,
        10: 3,
        11: 3,
        13: 4,
        14: 4,
        15: 4,
        16: 4
    }

    def getNextMoves(mt: MatrixTraverser,
                     currNode: MatrixTree) -> List[Move]:


        return [
            Move.DOWN,
            Move.DIAGONAL_DOWN_RIGHT
        ]


    def afterAddToBFSQueue(mt: MatrixTraverser,
                          currNode: MatrixTree) -> None:

        cellValue = currNode.getCellValue(mt.matrix)

        assert valuesByLevel[cellValue] == currNode.level


    startCoord = Coordinate(Matrix.getFirstRow(), Matrix.getFirstCol())

    matrixTraverser = MatrixTraverser(matrix, {
        "getNextMoves": getNextMoves,
        "afterAddToBFSQueue": afterAddToBFSQueue
    })

    matrixTraverser.traverseMatrixBFS(startCoord)





