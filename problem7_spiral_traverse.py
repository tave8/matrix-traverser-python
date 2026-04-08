"""
PROBLEM: Traverse the matrix in spiral traverse.

---------------
^ --------- v  |
| ------>   |  |
| --------  v  v
 <-------------

"""

from MatrixTraverser import MatrixTraverser, MatrixTraverserCallbackManager, MatrixTraverserStateManager, Coordinate, Move


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
        print(f"START: {mt.getAtCoordinate(currCoordinate)} ({prevMove.name})")
    else:
        print(f"FROM {mt.getAtCoordinate(prevCoordinate)} TO {mt.getAtCoordinate(currCoordinate)} ({prevMove.name})")

    # print(mt.stateManager.stats)


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