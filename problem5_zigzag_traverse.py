"""
PROBLEM: Traverse the matrix in zigzag.
"""

from MatrixTraverser import Matrix, MatrixTraverser, Coordinate, Move


matrix = [
  [1, 3, 4, 10],
  [2, 5, 9, 11],
  [6, 8, 12, 15],
  [7, 13, 14, 16]
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
    pass
    state["values"].append(Matrix.getAtCoordinate(mt.matrix, currCoordinate))


def getNextMovesCallback(mt: MatrixTraverser, 
                         prevCoordinate: Coordinate, 
                         currCoordinate: Coordinate,
                         prevMove: Move):

   # from the previous move, this the core logic of how the zigzag traverse works.
   # the key of this map is the previous move; the values are the ordered values where 
   # the cell can move to     
   moves = {
        Move._BEFORE_START: [Move.DOWN, Move.RIGHT],
        Move.DOWN: [Move.DIAGONAL_UP_RIGHT, Move.DIAGONAL_DOWN_LEFT, Move.DOWN],
        Move.DIAGONAL_UP_RIGHT: [Move.DIAGONAL_UP_RIGHT, Move.RIGHT, Move.DOWN],
        Move.RIGHT: [Move.DIAGONAL_UP_RIGHT, Move.DIAGONAL_DOWN_LEFT, Move.RIGHT],
        Move.DIAGONAL_DOWN_LEFT: [Move.DIAGONAL_DOWN_LEFT, Move.DOWN, Move.RIGHT]
    }
   
   return moves[prevMove]
   
   


def canMoveCallback(mt: MatrixTraverser, 
                    desiredCoordinate: Coordinate, 
                    prevCoordinate: Coordinate, 
                    currCoordinate: Coordinate,
                    prevMove: Move):
    pass    



callbackMap = {
    "canMove": canMoveCallback,
    "getNextMoves": getNextMovesCallback,
    "beforeFirstVisit": beforeFirstVisitCallback,
}



matrixTraverser = MatrixTraverser(
    matrix, 
    callbackMap,
    state
)

# for now you cannot call the method more than once
matrixTraverser.traverseMatrix(
    Coordinate.generateIsStartCoord(0, 0), 
    Coordinate.generateIsBeforeStartCoord()
)
