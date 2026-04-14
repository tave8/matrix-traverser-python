# MUST BE FIXED

from main import traverseMatrix, isInsideMatrix


def canMoveCallback(rowIdx, colIdx, prevRowIdx, prevColIdx, matrix, state):
        # if this cell does not exist (out of matrix)
    if not isInsideMatrix(rowIdx, colIdx, matrix):
        return False


    #     # print(rowIdx, colIdx, prevRowIdx, prevColIdx)
    # print(matrix[rowIdx][colIdx])
    # return matrix[rowIdx][colIdx] % 2 == 0
    if state["reachedEnd"]:
        return False

    if matrix[rowIdx][colIdx] == "E":
        state["reachedEnd"] = True
        return True

    return matrix[rowIdx][colIdx].startswith("X")


def firstVisitCallback(rowIdx, colIdx, matrix):
    print(matrix[rowIdx][colIdx])

state = {
    "reachedEnd": False,

}

callbacks = {
    "canMove": canMoveCallback,
    "firstVisit": firstVisitCallback
}

# navigate from start to end, 
# through all cells whose value starts with X
traverseMatrix([
    ["S",   "V",   "",     "X11",   ""],
    ["X1",  "B",   "X10",  "X12",   ""],
    ["X3",  "O",   "X6",   "",      "X13"],
    ["X5",  "X9", "X7",   "",      "X14"],
    ["",    "",    "",    "",      "E"]
], 0, 0, callbacks, state)



