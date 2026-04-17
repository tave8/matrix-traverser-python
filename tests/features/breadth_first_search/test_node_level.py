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



def test_node_level_all_cols_except_first():
    matrix = [
        [1,  2,   3,  4],
        [5,  6,   7,  8],
        [9,  10, 11, 12],
        [13, 14, 15, 16],
        [17, 18, 19, 20],
    ]

    valuesByLevel = {
        2: 3,
        3: 3,
        4: 3,
        6: 2,
        7: 2,
        8: 4,
        10: 1,
        11: 3,
        12: 5,
        14: 2,
        15: 4,
        16: 6,
        18: 3,
        19: 5,
        20: 6
    }

    def getNextMoves(mt: MatrixTraverser,
                     currNode: MatrixTree) -> List[Move]:

        return [
            Move.UP,
            Move.DOWN,
            Move.DIAGONAL_UP_RIGHT
        ]


    def afterAddToBFSQueue(mt: MatrixTraverser,
                          currNode: MatrixTree) -> None:

        cellValue = currNode.getCellValue(mt.matrix)

        assert valuesByLevel[cellValue] == currNode.level


    startCoord = Coordinate(2, 1)

    matrixTraverser = MatrixTraverser(matrix, {
        "getNextMoves": getNextMoves,
        "afterAddToBFSQueue": afterAddToBFSQueue
    })

    matrixTraverser.traverseMatrixBFS(startCoord)




