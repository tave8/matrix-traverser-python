from os.path import curdir
from typing import List

from src.core.MazeTraverser import MazeTraverser
from src.core.MatrixTraverser import MatrixTraverser, StateManager
from src.components import Coordinate, Move, Matrix, MatrixTree, MazeTerminationPolicy


# callback specific for this maze problem
def canMoveTo(mt: MatrixTraverser,
               currNode: MatrixTree,
               desiredCoord: Coordinate,
               desiredMove: Move) -> bool:
    # return True

    # print(currNode.getCellValue(mt.matrix), desiredCoord.getCellValue(mt.matrix))

    currentCellIsStart = currNode.coord.isStart

    if currentCellIsStart:
        return desiredCoord.getCellValue(mt.matrix) == 1

    desiredCellIsStart = desiredCoord.getCellValue(mt.matrix) == "S"

    if desiredCellIsStart:
        return False

    desiredCellIsEnd = desiredCoord.getCellValue(mt.matrix) == "E"

    # if the next move is the end, you can move
    if desiredCellIsEnd:
        return True
    # if Matrix.isVisited(mt.matrix, currNode.coord):
    #     return False

    currentCellIsEnd = currNode.getCellValue(mt.matrix) == "E"


    # if the curr coordinate is the end itself,
    # apply the maze termination policy
    if currentCellIsEnd:
        # print(currNode.coord)
        # print(currNode.parent.coord)
        # print(currNode.getAncestorCellValues(mt.matrix))
        # print("reached end")

        # MazeTraverser._onEndFoundCallback(mazeTraverser, currNode)
        # StateManager.setWasEnded(mt, True)

        # if end is found and this is the end,
        # end cell cannot move
        return False

    # print(currNode.getCellValue(mt.matrix), desiredCoord.getCellValue(mt.matrix))

    nextNum = Matrix.getAtCoordinate(mt.matrix, desiredCoord)
    currNum = Matrix.getAtCoordinate(mt.matrix, currNode.coord)

    cond = nextNum == currNum + 1 # type: ignore


    if cond:
        # print(currNode.parent.coord.getCellValue(mt.matrix), currNode.coord.getCellValue(mt.matrix))
        #     print(currNum, nextNum)
        pass
    #
    # # this cell can move to the desired/next coordinate
    # # only if this condition is met
    return cond
    #

# def getNextMoves(mt: MatrixTraverser, currNode: MatrixTree) -> List[Move]:
#     return [
#         Move.RIGHT,
#         Move.DOWN,
#         Move.UP
#     ]

matrix = [
    ["S",   1,  2],
    [ 1,    3,  3],
    [ 2,    2,  4],
    [ 3,   15, "E"],
    [ 4,   17,  19],
    [ 5,   6,   8],
    [ 6,   6,   7],
    [ 8,   7,   8],
]


def afterAllFutureMoves(mt: MatrixTraverser, currNode: MatrixTree) -> None:
    # if this node is a "leaf node" and the end
    # was still not found, then there's no end

    if currNode.getCellValue(mt.matrix) == "E":
        print("reached end. PATH: ", currNode.getAncestorCellValues(mt.matrix))
        # mt.stateManager.state["foundEnd"] = True
    else:
        if currNode.countNodes() == 1:
            print("leaf node value: ",
                  currNode.getCellValue(mt.matrix), f" in coord {currNode.coord}. ancestors: ",
                  currNode.getAncestorCellValues(mt.matrix),
                  "children: ", currNode.children
                )
            # print(currNode.getAncestors())
            pass


def onMultipleVisitMustStop(mt: MatrixTraverser,
                            parentNode: MatrixTree,
                            currCoord: Coordinate) -> bool:
    # you must continue only if the next value is incrementing
    # currValueIsBigger = currCoord.getCellValue(mt.matrix) == 1+parentNode.coord.getCellValue(mt.matrix)
    # # currValueIsEnd = currCoord.getCellValue(mt.matrix) == "E"
    # return not currValueIsBigger

    return True


traverser = MatrixTraverser(matrix, {
    "afterAllFutureMoves": afterAllFutureMoves,
    "canMoveTo": canMoveTo,
    "onMultipleVisitMustStop": onMultipleVisitMustStop
    # "getNextMoves": getNextMoves,
})

# traverser.stateManager.state["endFound"] = False

traverser.traverseMatrixDFS(Coordinate(0,0))

# print(traverser.getMovesHistory())





