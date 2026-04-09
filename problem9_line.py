"""
PROBLEM: Traverse the matrix in a line.


"""

from MatrixTraverser import MatrixTraverser, MatrixTraverserCallbackManager, MatrixTraverserStateManager, Coordinate, Move


matrix = [
    [10,   2,    6,   7,   15],
    [3,    8,    7,  2,    16],
    [1,    2,    3,  4,    5],
    [10,   6,    8,  4,    23],
    [11,   19,   9,   24,  25]
]

state = {
    "crossValues": []
}


def beforeFirstVisitCallback(mt: MatrixTraverser, 
                             prevCoordinate: Coordinate, 
                             currCoordinate: Coordinate,
                             prevMove: Move):
    if currCoordinate.isStart:
        print(f"START: {mt.getAtCoordinate(currCoordinate)} ({prevMove.name})")
    else:
        print(f"FROM {mt.getAtCoordinate(prevCoordinate)} TO {mt.getAtCoordinate(currCoordinate)} ({prevMove.name})")
    pass
    # print(mt.stateManager.stats)


def getNextMovesCallback(mt: MatrixTraverser, 
                         prevCoordinate: Coordinate, 
                         currCoordinate: Coordinate,
                         prevMove: Move):

    # get the row in the middle
    # if currCoordinate.getRow() == len(mt.matrix) // 2:
    #     return [
    #         Move.RIGHT
    #     ]

   # previous move: next moves 
#    moves = {
#         Move._BEFORE_START: [Move.RIGHT],
#         Move.DOWN: [Move.DIAGONAL_UP_RIGHT],
#         Move.DIAGONAL_UP_RIGHT: [Move.DIAGONAL_UP_RIGHT, Move.RIGHT],
#         Move.RIGHT: [Move.DIAGONAL_DOWN_LEFT],
#         Move.DIAGONAL_DOWN_LEFT: [Move.DIAGONAL_DOWN_LEFT, Move.DOWN]
#     }
   
#    return moves[prevMove]
    pass
   


def canMoveCallback(mt: MatrixTraverser, 
                    desiredCoordinate: Coordinate, 
                    prevCoordinate: Coordinate, 
                    currCoordinate: Coordinate,
                    prevMove: Move):
    pass    



def canVisitCallback(mt: MatrixTraverser, 
                    prevCoordinate: Coordinate, 
                    currCoordinate: Coordinate,
                    prevMove: Move):
    
    
    # step 1: find the start of the row in the middle
    # if the horizontal line of the cross is complete, 
    # if currCoordinate.getRow() == len(mt.matrix) // 2:
    #     return False
    
    # if currCoordinate.getCol() == len(mt.matrix[0]) // 2:
    #     return False 
    pass


def onMultipleVisitStopCallback(mt: MatrixTraverser, 
                         prevCoordinate: Coordinate, 
                         currCoordinate: Coordinate,
                         prevMove: Move):
    # skip the visited cells that are part of the circle
    # so you can move freely through them
    # if(mt.getAtCoordinate(currCoordinate)) > 0:
    #     return False  
    pass


def canEndCallback(mt: MatrixTraverser, 
                         prevCoordinate: Coordinate, 
                         currCoordinate: Coordinate,
                         prevMove: Move):
    return False 


callbackMap = {
    "canMove": canMoveCallback,
    "getNextMoves": getNextMovesCallback,
    "beforeFirstVisit": beforeFirstVisitCallback,
    "canVisit": canVisitCallback,
    "onMultipleVisitStop": onMultipleVisitStopCallback,
    "canEnd": canEndCallback
}


stateManager = MatrixTraverserStateManager(state)
callbackManager = MatrixTraverserCallbackManager(callbackMap)

matrixTraverser = MatrixTraverser(
    matrix, 
    Coordinate(0, 0),
    callbackManager,
    stateManager
)


def findOneCallback(findOneMt: MatrixTraverser, 
                    prevCoordinate, 
                    currCoordinate, 
                    prevMove) -> bool:
    # find cell with value 3
    if findOneMt.getAtCoordinate(currCoordinate) == 3:
        return True 
    return False 

# for now you cannot call the method more than once
matrixTraverser.traverseMatrix()
# matrixTraverser.findOne(findOneCallback, Coordinate(0, 0))

# for move, moveStats in matrixTraverser.stateManager.stats["byMove"].items():
#     print()
#     print(f"{move}: {moveStats}")
#     print()

# print(state)