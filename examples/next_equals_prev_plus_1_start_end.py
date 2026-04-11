"""
Find the path where each cell must be exactly +1 from the previous,
and you also have start and end.

Properties:
- the start must always be start
- for each pair of move from a cell to a cell [prevCell, currCell],
    the distance of the move is 1 cell
- for each pair of move from a cell to a cell [prevCell, currCell],
    the value of currCell = prevCell value + 1
- the end might not exist
"""

from src.MatrixTraverser import Matrix, MatrixTraverser, Coordinate, Move, StateManager



matrix = [
        ["S",  "1",  "2",   "3",   "4",  "5"],
        ["1",  "1",  "2",   "4",   "5",  "6"],
        ["2",  "2",  "4",   "5",   "6",  "7"],
        ["3",  "4",  "3",   "5",   "7",  "8"],
        ["4",  "5",  "6",   "8",   "6",  "9"],
        ["5",  "8",  "11",  "9",   "11", "2"],
        ["6",  "7",  "10",  "10",  "8",  "E"]
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
    pass

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
    # because of how the engine works and the nature of its recursive calls,
    # even though the start is already visited,
    # some start paths might still be asking if i can move to start
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


    nextNum = int(Matrix.getAtCoordinate(mt.matrix, desiredCoord)) # type: ignore
    currNum = int(Matrix.getAtCoordinate(mt.matrix, currCoord)) # type: ignore

    # this cell can move to the desired/next coordinate 
    # only if this condition is met
    return nextNum == currNum + 1





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




