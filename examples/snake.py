"""
PROBLEM: Traverse the matrix in snake traverse.

|  |--|  |--|
|  |  |  |  |
|__|  |__|  | 

"""

from src.MatrixTraverser import MatrixTraverser, MatrixTraverserCallbackManager, MatrixTraverserStateManager, Coordinate, Move


matrix = [
    [1,   6,   11,  16,  21],
    [2,   7,   12,  17,  22],
    [3,   8,   13,  18,  23],
    [4,   9,   14,  19,  24],
    [5,   10,  15,  20,  25]
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
        Move._BEFORE_START: [Move.DOWN],
        Move.DOWN: [Move.DOWN, Move.RIGHT],
        Move.RIGHT: [Move.UP, Move.DOWN],
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