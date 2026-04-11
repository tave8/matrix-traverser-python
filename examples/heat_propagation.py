"""
Heat propagation.
"""

from src.MatrixTraverser import Matrix, MatrixTraverser, Coordinate, Move, StateManager



matrix = [
    ["S",  12,   8,   3,   2],
    [ 11,  10,   7,   4,   3],
    [  9,   8,   7,   5,   4],
    [  7,   6,   6,   5,   5],
    [  5,   4,   5,   5,  "E"]
]

state = {}
 

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
        return Matrix.getAtCoordinate(mt.matrix, desiredCoord) == 10

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

    nextNum = Matrix.getAtCoordinate(mt.matrix, desiredCoord) # type: ignore
    currNum = Matrix.getAtCoordinate(mt.matrix, currCoord) # type: ignore

    # this cell can move to the desired/next coordinate 
    # only if this condition is met
    return nextNum == currNum + 1 # type: ignore





callbackMap = {
    "canMoveTo": canMoveToCallback,
    "beforeFirstVisit": beforeFirstVisitCallback,
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




