from src.MatrixTraverser import Coordinate, Matrix

matrix = [
    [1,    2,   3,   4,   5],
    [6,    7,   8,   9,   10],
    [11,   12,  13,  14,  15],
    [16,   17,  18,  19,  20],
    [21,   22,  23,  24,  25],
    # [21,   22,  23,  24,  25],
]

# print(Matrix.getRowsNextToMiddle(matrix))
# print(Matrix.getColsNextToMiddle(matrix))
# print(Matrix.getMiddleCol(matrix))
# print(Matrix.getMiddleRow(matrix))
# print(Matrix.getLastRow(matrix))

print(Coordinate(0, 0).isTopLeft(matrix))
print(Coordinate(4, 0).isBottomLeft(matrix))
print(Coordinate(0, 4).isTopRight(matrix))
print(Coordinate(4, 4).isBottomRight(matrix))