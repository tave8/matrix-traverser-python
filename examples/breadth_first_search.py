from src.components import Coordinate, Matrix
from src.core.MatrixTraverser import MatrixTraverser

matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

startCoord = Coordinate(Matrix.getFirstRow(), Matrix.getFirstCol())

matrixTraverser = MatrixTraverser(matrix)

nodes = matrixTraverser.traverse_BFS(startCoord)

for node in nodes:
    cellValue = Matrix.getAtCoordinate(matrix, node.coord)
    print(cellValue)

