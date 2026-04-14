from components import Coordinate, Matrix
from implementations.diagonal import makeDiagonalPattern

diagonalPattern = makeDiagonalPattern([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
])

diagonalPattern.run(
    Coordinate(
        Matrix.getLastRow(diagonalPattern.matrix),
        Matrix.getLastCol(diagonalPattern.matrix)
    )
)

for cellInfo in diagonalPattern.getMovesHistory():
    print(cellInfo)

