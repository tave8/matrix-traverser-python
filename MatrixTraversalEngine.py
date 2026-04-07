class MatrixTraversalEngine:
    def __init__(self, matrix):
        self.matrix = matrix
        self.visited = self._get0Matrix(matrix)

    def traverseMatrix(matrix, row, column, callbacks, state):
        # matrix of 0's
        visited = get0Matrix(matrix)
        # print(visited)
        
        traverse(row, column, None, None, IndexInfo(row, column), matrix, visited, callbacks, state)
        
        # print(visited)
        return matrix



    def traverse(rowIdx, colIdx, prevRowIdx, prevColIdx, indexInfo, matrix, visited, callbacks, state):
        # if this cell does not exist (out of matrix)
        if not isInsideMatrix(rowIdx, colIdx, matrix):
            return

        # isStart = rowIdx == indexInfo.rowIdx and colIdx == indexInfo.colIdx
        isVisited = visited[rowIdx][colIdx] == 1

        # if this cell has been visited
        if isVisited:
            return
        
        # cell was not visited; we're visiting it right now
        # print(matrix[rowIdx][colIdx])
        callbacks["firstVisit"](rowIdx, colIdx, matrix) 

        # now we mark cell as visited
        visited[rowIdx][colIdx] = 1

        moves = callbacks["pilotCell"](rowIdx, colIdx, prevRowIdx, prevColIdx, matrix, state)

        # move in the order that was specified
        for move in moves:
            if move == "up":            
                if callbacks["canMove"](rowIdx-1, colIdx, rowIdx, colIdx, matrix, state):
                    # up
                    traverse(rowIdx-1, colIdx, rowIdx, colIdx, indexInfo, matrix, visited, callbacks, state)
            
            elif move == "diag-up-right":
                if callbacks["canMove"](rowIdx-1, colIdx+1, rowIdx, colIdx, matrix, state):
                    # diag up right
                    traverse(rowIdx-1, colIdx+1, rowIdx, colIdx, indexInfo, matrix, visited, callbacks, state)
            
            elif move == "right":
                if callbacks["canMove"](rowIdx, colIdx+1, rowIdx, colIdx, matrix, state):
                    # right
                    traverse(rowIdx, colIdx+1, rowIdx, colIdx, indexInfo, matrix, visited, callbacks, state)
            
            elif move == "diag-down-right":
                if callbacks["canMove"](rowIdx+1, colIdx+1, rowIdx, colIdx, matrix, state):
                    # diag down right
                    traverse(rowIdx+1, colIdx+1, rowIdx, colIdx, indexInfo, matrix, visited, callbacks, state)
            
            elif move == "down":
                if callbacks["canMove"](rowIdx+1, colIdx, rowIdx, colIdx, matrix, state):
                    # down
                    traverse(rowIdx+1, colIdx, rowIdx, colIdx, indexInfo, matrix, visited, callbacks, state)
            
            elif move == "diag-down-left":
                if callbacks["canMove"](rowIdx+1, colIdx-1, rowIdx, colIdx, matrix, state):
                    # diag down left
                    traverse(rowIdx+1, colIdx-1, rowIdx, colIdx, indexInfo, matrix, visited, callbacks, state)
            
            elif move == "left":
                if callbacks["canMove"](rowIdx, colIdx-1, rowIdx, colIdx, matrix, state):
                    # left
                    traverse(rowIdx, colIdx-1, rowIdx, colIdx, indexInfo, matrix, visited, callbacks, state)
            
            elif move == "diag-up-left":
                if callbacks["canMove"](rowIdx-1, colIdx-1, rowIdx, colIdx, matrix, state):
                    # diag up left
                    traverse(rowIdx-1, colIdx-1, rowIdx, colIdx, indexInfo, matrix, visited, callbacks, state)
                




    @staticmethod
    def _get0Matrix(matrix):
        ret = []
        for i in range(len(matrix)):
            row = []
            for j in range(len(matrix[0])):
                row.append(0)
            ret.append(row)
        return ret


    @staticmethod
    def _isInsideMatrix(rowIdx, colIdx, matrix):
        insideRows = rowIdx >= 0 and rowIdx < len(matrix)
        insideCols = colIdx >= 0 and colIdx < len(matrix[0])
        return insideRows and insideCols