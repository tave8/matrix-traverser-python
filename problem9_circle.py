"""
PROBLEM: Traverse the matrix in one circle.


"""

from MatrixTraverser import MatrixTraverser, MatrixTraverserCallbackManager, MatrixTraverserStateManager, Coordinate, Move


matrix = [
    [1,    2,    1,   7,   15],
    [3,    8,    90,  2,  16],
    [7,    9,    13,  17,  3],
    [10,   6,    18,  4,  23],
    [11,   19,   5,   24,  25]
]

state = {
    "values": []
}


def beforeFirstVisitCallback(mt: MatrixTraverser, 
                             prevCoordinate: Coordinate, 
                             currCoordinate: Coordinate,
                             prevMove: Move):
    if currCoordinate.isStart:
        print(f"START: {mt.getAtCoordinate(currCoordinate)} ({prevMove.name})")
    else:
        print(f"FROM {mt.getAtCoordinate(prevCoordinate)} TO {mt.getAtCoordinate(currCoordinate)} ({prevMove.name})")

    # print(mt.stateManager.stats)


def getNextMovesCallback(mt: MatrixTraverser, 
                         prevCoordinate: Coordinate, 
                         currCoordinate: Coordinate,
                         prevMove: Move):

    # if current cell is at the border of quadrant 1 and 2,
    # start the algorithm

   # previous move: next moves 
   moves = {
        Move._BEFORE_START: [Move.RIGHT],
        Move.DOWN: [Move.DIAGONAL_UP_RIGHT],
        Move.DIAGONAL_UP_RIGHT: [Move.DIAGONAL_UP_RIGHT, Move.RIGHT],
        Move.RIGHT: [Move.DIAGONAL_DOWN_LEFT],
        Move.DIAGONAL_DOWN_LEFT: [Move.DIAGONAL_DOWN_LEFT, Move.DOWN]
    }
   
   return moves[prevMove]
   
   


def canMoveCallback(mt: MatrixTraverser, 
                    desiredCoordinate: Coordinate, 
                    prevCoordinate: Coordinate, 
                    currCoordinate: Coordinate):
    pass    



callbackMap = {
    "canMove": canMoveCallback,
    "getNextMoves": getNextMovesCallback,
    "beforeFirstVisit": beforeFirstVisitCallback,
}


stateManager = MatrixTraverserStateManager(state)
callbackManager = MatrixTraverserCallbackManager(callbackMap)

matrixTraverser = MatrixTraverser(
    matrix, 
    Coordinate(0, 0),
    callbackManager,
    stateManager
)

# for now you cannot call the method more than once
matrixTraverser.traverseMatrix()


# for move, moveStats in matrixTraverser.stateManager.stats["byMove"].items():
#     print()
#     print(f"{move}: {moveStats}")
#     print()