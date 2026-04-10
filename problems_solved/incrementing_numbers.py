"""
Find the path where each cell must be exactly +1 from the previous.
"""

from MatrixTraverser import Matrix, MatrixTraverser, Coordinate, Move, StateManager



matrix = [
    ["S",   "8",   "9",   "9",   "90"],
    ["1",   "2",   "7",   "8",   "10"],
    ["10",  "3",   "6",   "9",   "13"],
    ["12",  "4",   "10",  "6",   "14"],
    ["5",   "6",   "5",   "16",  "E"]
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


def canMoveToCallback(mt: MatrixTraverser, 
                    desiredCoord: Coordinate, 
                    prevCoord: Coordinate, 
                    currCoord: Coordinate,
                    prevMove: Move):

    # from the start, you can only move to 
    # a cell with value 1
    if currCoord.isStart:
        return Matrix.getAtCoordinate(mt.matrix, desiredCoord) == "1"

    # the cells around S might try to go to S, but they must not
    if Matrix.getAtCoordinate(mt.matrix, desiredCoord) == "S":
        return False
    
    # if the next move is the end, you can move
    if Matrix.getAtCoordinate(mt.matrix, desiredCoord) == "E":
        return True
    
    # if the curr coordinate is the end itself,
    # end the algorithm
    if Matrix.getAtCoordinate(mt.matrix, currCoord) == "E":
        # end the algorithm at 
        StateManager.setWasEnded(mt, True)
        # it does not matter what you return
        return

    nextNum = int(Matrix.getAtCoordinate(mt.matrix, desiredCoord))
    currNum = int(Matrix.getAtCoordinate(mt.matrix, currCoord))

    # this cell can move to the desired/next coordinate 
    # only if this condition is met
    return nextNum == currNum + 1


def onMultipleVisitMustStopCallback(mt: MatrixTraverser, 
                                    prevCoord: Coordinate, 
                                    currCoord: Coordinate, 
                                    prevMove: Move):
    return False 
    



callbackMap = {
    "canMoveTo": canMoveToCallback,
    "beforeFirstVisit": beforeFirstVisitCallback,
    "onMultipleVisitMustStop": onMultipleVisitMustStopCallback
}


matrixTraverser = MatrixTraverser(
    matrix, 
    callbackMap,
    state
)

matrixTraverser.traverseMatrix(
    Coordinate(
        Matrix.getFirstRow(),
        Matrix.getFirstCol()
    )
)



