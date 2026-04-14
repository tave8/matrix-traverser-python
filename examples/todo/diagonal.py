from core.MatrixTraverser import Matrix, MatrixTraverser, Coordinate, Move

matrix = [
    [5,   6,   11,  16,  21],
    [2,   4,   12,  17,  22],
    [3,   8,   3,  18,  23],
    [4,   9,   14,  2,  24],
    [5,   10,  15,  20,  1],
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



def getNextMovesCallback(mt: MatrixTraverser, 
                         prevCoordinate: Coordinate, 
                         currCoordinate: Coordinate,
                         prevMove: Move):

    return [
        Move.DIAGONAL_UP_LEFT
    ]



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
    Coordinate(
        Matrix.getLastRow(matrix),
        Matrix.getLastCol(matrix)
    )
)