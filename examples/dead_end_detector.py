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
        if not "foundEnd" in currNode.myState:
            # currNode.myState["foundEnd"] = True
            mt.stateManager.userState["endNode"] = currNode
            # print(currNode.coord)
            # print(currNode.parent.coord)
            # print(currNode.getAncestorCellValues(mt.matrix))
            # print("reached end from: ", currNode.parent.coord)

        # currNode.myState[""]

        # currNode.parent.myState[""]



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
#
matrix = [
    ["S",   1,     4],
    [ 3,    2,     3],
    [ 2,    5,     4],
    [ 2,    6,     4],
    [ 7,    7,     10],
    [ 9,    8,     8],
    [ 9,    10,     4],
    [ 10,   9,    "E"],
]

startCoord = Coordinate(0,0)


def afterAllFutureMoves(mt: MatrixTraverser, currNode: MatrixTree) -> None:
    # if currNode.countNodes() == 1:
    #     print("completed ALL moves at node that has no exit: ", currNode.coord)
    pass

def afterOneFutureMove(mt: MatrixTraverser, currNode: MatrixTree) -> None:
    # a leaf node is the first to finish its future moves,
    # if the currNode does not have a
    # if currNode.countNodes() == 1:
    #     print("completed one move at node that has no exit: ", currNode.coord)
    pass

# def onMultipleVisitMustStop(mt: MatrixTraverser,
#                             parentNode: MatrixTree,
#                             currCoord: Coordinate) -> bool:
#     # you must continue only if the next value is incrementing
#     # currValueIsBigger = currCoord.getCellValue(mt.matrix) == 1+parentNode.coord.getCellValue(mt.matrix)
#     # # currValueIsEnd = currCoord.getCellValue(mt.matrix) == "E"
#     # return not currValueIsBigger
#
#     return True

callbackMap = {
    "afterAllFutureMoves": afterAllFutureMoves,
    "canMoveTo": canMoveTo,
    "afterOneFutureMove": afterOneFutureMove
    # "onMultipleVisitMustStop": onMultipleVisitMustStop
    # "getNextMoves": getNextMoves,
}


traverser = MatrixTraverser(matrix, callbackMap)

# traverser.stateManager.state["endFound"] = False

traverser.traverseMatrixDFS(startCoord)

# traverser.matrixTree.printUsingBFS(matrix)


def getCoordsFromStartToEnd(node: MatrixTree) -> List[Coordinate]:
    ret = node.getAncestorCellCoords()
    ret.append(node.coord)
    return ret


# if the end was found
if "endNode" in traverser.stateManager.userState:
    print("*******END WAS FOUND**********")
    print()
    endNode: MatrixTree = traverser.stateManager.userState["endNode"]
    coordsFromStartToEnd = getCoordsFromStartToEnd(endNode)

    pathMatrix = Matrix.generateBinaryMatrixFromCoordsFrom(coordsFromStartToEnd, matrix)

    print("> MATRIX OF 1 PATH")
    for row in range(Matrix.getHowManyRows(matrix)):
        print(pathMatrix[row])


    # CALLBACK OF SECOND TRAVERSER

    traverser2 = MatrixTraverser(matrix, {

    })

    traverser2.traverseMatrixDFS(startCoord.clone())











