from MatrixTraversalEngine import traverseMatrix, isInsideMatrix


# next is the desired move
# current is the cell where we're at
def canMoveCallback(nextRowIdx, nextColIdx, currRowIdx, currColIdx, matrix, state):
    if not isInsideMatrix(nextRowIdx, nextColIdx, matrix):
        return False

    if state["reachedEnd"]:
        return False

    if matrix[nextRowIdx][nextColIdx] == "E":
        state["reachedEnd"] = True
        return True

    # from the start, you can only move to 
    # a cell with value 1
    if matrix[currRowIdx][currColIdx] == "S":
        return matrix[nextRowIdx][nextColIdx] == "1"

    # the next move cannot be the start 
    if matrix[nextRowIdx][nextColIdx] == "S":
        return False

    return int(matrix[currRowIdx][currColIdx])+1 == int(matrix[nextRowIdx][nextColIdx])


def firstVisitCallback(rowIdx, colIdx, matrix):
    print(matrix[rowIdx][colIdx])


def pilotCellCallback(rowIdx, colIdx, prevRowIdx, prevColIdx, matrix, state):
    # you can specify where the cell should move, in order
    # (order matters)
    # that does not guarantee that the cell will move
    # in that direction, only that it can move in that direction first
    # print(matrix[rowIdx][colIdx])
    # if matrix[rowIdx][colIdx] == "1":
    #     return ["down"]
    # return ["right", "left", "down", "up", "diag-down-right", "diag-down-left"]

    # this is how the cell moves by default
    return [
        "up",
        "diag-up-right",
        "right",
        "diag-down-right",
        "down",
        "diag-down-left",
        "left",
        "diag-up-left"
    ]



state = {
    "reachedEnd": False,
    "values": [],
    "path": []
}

callbacks = {
    "canMove": canMoveCallback,
    "firstVisit": firstVisitCallback,
    "pilotCell": pilotCellCallback
}

# find the path where each cell must be exactly 
# +1 from the previous 
traverseMatrix([
    ["S",   "8",  "9",  "9",   "90"],
    ["1",   "2",   "7",  "8",   "10"],
    ["3",   "43",  "6",  "11",  "13"],
    ["3",   "4",   "5",  "12",   "14"],
    ["5",   "6",  "12",  "16",   "E"]
], 0, 0, callbacks, state)



