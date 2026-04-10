"""
Traverse the matrix in spiral.
"""

from src.MatrixTraverser import Matrix, MatrixTraverser, Coordinate, Move


matrix = [
    [1,    2,    3,   4,   5],
    [16,   17,   18,  19,  6],
    [15,   24,   25,  20,  7],
    [14,   23,   22,  21,  8],
    [13,   12,   11,  10,  9]
]

state = {
    "values": []
}


def beforeFirstVisitCallback(mt: MatrixTraverser, 
                             prevCoordinate: Coordinate, 
                             currCoordinate: Coordinate,
                             prevMove: Move):
    if currCoordinate.isStart:
        print(f"START: {Matrix.getAtCoordinate(mt.matrix, currCoordinate)} ({prevMove.name})")
    else:
        print(f"FROM {Matrix.getAtCoordinate(mt.matrix, prevCoordinate)} TO {Matrix.getAtCoordinate(mt.matrix, currCoordinate)} ({prevMove.name})")



def getNextMovesCallback(mt: MatrixTraverser, 
                         prevCoordinate: Coordinate, 
                         currCoordinate: Coordinate,
                         prevMove: Move):

   # previous move: next moves 
   moves = {
        Move._BEFORE_START: [Move.RIGHT],
        Move.DOWN: [Move.DOWN, Move.LEFT],
        Move.RIGHT: [Move.RIGHT, Move.DOWN],
        Move.LEFT: [Move.LEFT, Move.UP],
        Move.UP: [Move.UP, Move.RIGHT]
    }
   
   return moves[prevMove]
   


callbackMap = {
    "getNextMoves": getNextMovesCallback,
    "beforeFirstVisit": beforeFirstVisitCallback,
}



matrixTraverser = MatrixTraverser(
    matrix, 
    callbackMap,
    state
)

matrixTraverser.traverseMatrix(
    Coordinate.generateIsStartCoord(0, 0)
)