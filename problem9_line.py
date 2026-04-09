"""
PROBLEM: Traverse the matrix in a line.


"""

from MatrixTraverser import Matrix, MatrixTraverser, Coordinate, Move


matrix = [
    [10,   2,    6,   7,   15],
    [3,    8,    7,  2,    16],
    [1,    2,    3,  4,    5],
    [10,   6,    8,  4,    23],
    [11,   19,   9,   24,  25]
]

state = {
    "crossValues": [],
    "found15": False 
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
    # print(mt.stateManager.stats)

    # if currCoordinate.getRow() == 0 and currCoordinate.getCol == len(mt.matrix)-1:
    #     mt.stateManager.state["found15"] = True




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
   moves = {
        Move._BEFORE_START: [Move.RIGHT],
        Move.RIGHT: [Move.RIGHT, Move.UP],
        Move.UP: [Move.UP],
    }
   
   return moves[prevMove]

   


def canMoveCallback(mt: MatrixTraverser, 
                    desiredCoordinate: Coordinate, 
                    prevCoordinate: Coordinate, 
                    currCoordinate: Coordinate,
                    prevMove: Move):
    pass





def onMultipleVisitMustStopCallback(mt: MatrixTraverser, 
                         prevCoordinate: Coordinate, 
                         currCoordinate: Coordinate,
                         prevMove: Move):
    # skip the visited cells that are part of the circle
    # so you can move freely through them
    # if(mt.getAtCoordinate(currCoordinate)) > 0:
    #     return False  
    pass

# def canVisitCallback(mt: MatrixTraverser, 
#                     prevCoordinate: Coordinate, 
#                     currCoordinate: Coordinate,
#                     prevMove: Move):
    
    
#     # step 1: find the start of the row in the middle
#     # if the horizontal line of the cross is complete, 
#     # if currCoordinate.getRow() == len(mt.matrix) // 2:
#     #     return False
    
#     # if currCoordinate.getCol() == len(mt.matrix[0]) // 2:
#     #     return False 
#     pass

# def canEndCallback(mt: MatrixTraverser, 
#                          prevCoordinate: Coordinate, 
#                          currCoordinate: Coordinate,
#                          prevMove: Move):
    
#     # if mt.getAtCoordinate(currCoordinate) == 3:
#     #     if "numbers" not in mt.stateManager.state:
#     #         mt.stateManager.state["foundCells"] = [currCoordinate]
#     #     else:
#     #         mt.stateManager.state["foundCells"].append(currCoordinate)
#     #     return True 

#     if "found15" not in mt.stateManager.state:
#         return False 

#     if mt.stateManager.state["found15"]:
#         return True     


# def onEndCallback(mt: MatrixTraverser):
#     # print(mt.stateManager.state["foundCells"])
#     pass


callbackMap = {
    "canMove": canMoveCallback,
    "getNextMoves": getNextMovesCallback,
    "beforeFirstVisit": beforeFirstVisitCallback,
    "onMultipleVisitMustStop": onMultipleVisitMustStopCallback,
    # "canVisit": canVisitCallback,
    # "canEnd": canEndCallback,
    # "onEnd": onEndCallback,
}


# stateManager = StateManager(state)
# callbackManager = CallbackManager(callbackMap)

matrixTraverser = MatrixTraverser(
    matrix, 
    callbackMap,
    state
)

# def findOneCallback(findOneMt: MatrixTraverser, 
#                     prevCoordinate, 
#                     currCoordinate, 
#                     prevMove) -> bool:
#     # find cell with value 3
#     # if findOneMt.getAtCoordinate(currCoordinate) == 3:
#     #     print("found value", currCoordinate,findOneMt.getAtCoordinate(currCoordinate) )
#     #     return True 
#     if currCoordinate.getRow() == len(findOneMt.matrix) // 2:
#         print(currCoordinate)
#         return True 
#     return False 

# for now you cannot call the method more than once
matrixTraverser.traverseMatrix(
    Coordinate.generateIsStartCoord(2, 0), 
    Coordinate.generateIsBeforeStartCoord()
)
# matrixTraverser.findOne(findOneCallback, Coordinate(0, 0))

# for move, moveStats in matrixTraverser.stateManager.stats["byMove"].items():
#     print()
#     print(f"{move}: {moveStats}")
#     print()

# print(state)