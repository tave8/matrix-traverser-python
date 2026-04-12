
from src.components import Coordinate, Move, Matrix
from src.MazeTraverser import MazeTraverser


# user-defined cell movement
def canMoveTo(mt: MazeTraverser, 
                desiredCoord: Coordinate, 
                prevCoord: Coordinate, 
                currCoord: Coordinate,
                prevMove: Move) -> bool:
            
        nextNum = int(Matrix.getAtCoordinate(mt.matrix, desiredCoord)) # type: ignore
        currNum = int(Matrix.getAtCoordinate(mt.matrix, currCoord)) # type: ignore

        # this cell can move to the desired/next coordinate 
        # only if this condition is met
        return nextNum == currNum + 1



def canMoveToOnStart(mt: MazeTraverser, 
                    desiredCoord: Coordinate, 
                    prevCoord: Coordinate, 
                    currCoord: Coordinate,
                    prevMove: Move) -> bool:
        
    return Matrix.getAtCoordinate(mt.matrix, desiredCoord) == 2
                


# matrix = [
#         ["S",  "1",  "2",   "3",   "4",  "5"],
#         ["1",  "1",  "2",   "4",   "5",  "6"],
#         ["2",  "2",  "4",   "5",   "6",  "7"],
#         ["3",  "4",  "3",   "5",   "7",  "8"],
#         ["4",  "5",  "6",   "8",   "6",  "9"],
#         ["5",  "8",  "11",  "9",   "11", "2"],
#         ["6",  "7",  "10",  "10",  "8",  "E"]
# ]

# matrix = [
#         ["S",  1,  2,  3,  4,  5],
#         [ 1,   1,  2,  4,  5,  6],
#         [ 2,   2,  4,  5,  6,  7],
#         [ 3,   4,  3,  5,  7,  8],
#         [ 4,   5,  6,  8,  6,  9],
#         [ 5,   8, 11,  9, 11,  2],
#         [ 6,   7, 10, 10,  8, "E"]
# ]


matrix = [
        ["S",  2,  2,  3,  4,  5],
        [ 1,   3,  2,  4,  5,  6],
        [ 2,   2,  4,  5,  6,  7],
        [ 3,   4,  3,  5,  7,  8],
        [ 4,   5,  6,  8,  6,  9],
        [ 5,   8, 11,  9, 11,  2],
        [ 6,   7, 10, 10,  8, "E"]
]

mazeTraverser = MazeTraverser(
    matrix, 
    canMoveToCallback=canMoveTo, 
    canMoveToOnStartCallback=canMoveToOnStart
)


startCoord = Coordinate(
    Matrix.getFirstRow(),
    Matrix.getFirstCol()
)

mazeTraverser.run(startCoord)

for cellInfo in mazeTraverser.stateManager.state["movesFromTo"]:
    print(cellInfo)