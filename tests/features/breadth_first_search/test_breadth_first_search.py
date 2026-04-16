from src.components import Coordinate, Matrix, MatrixTree
from src.core.MatrixTraverser import MatrixTraverser


# def test_

matrix = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16]
]

startCoord = Coordinate(Matrix.getFirstRow(), Matrix.getFirstCol())

matrixTraverser = MatrixTraverser(matrix)

matrixTraverser.traverseMatrixBFS(startCoord)

# for node in nodes:
#     cellValue = Matrix.getAtCoordinate(matrix, node.coord)
#     print(cellValue)

targetValue = 4
(nodeFound, ancestors) = MatrixTree.findOneByValueFrom(matrixTraverser.matrixTree,
                                                       targetValue,
                                                       matrix)

print()
# for each ancestor, see its children
print("******** ANCESTORS FOR VALUE: ", targetValue)
print("NODE FOUND: ", nodeFound)

print()
for ancestor in ancestors:
    ancestorValue = Matrix.getAtCoordinate(matrix, ancestor.coord)
    print("ancestor: ", ancestorValue)
    for child in ancestor.children:
        childValue = Matrix.getAtCoordinate(matrix, child.coord)
        print("  > child: ", childValue)

# MatrixTree.findAllAncestorsOf(root)


targetValue = 12
(nodeFound, ancestors) = MatrixTree.findOneByValueFrom(matrixTraverser.matrixTree, targetValue, matrix)

print()
# for each ancestor, see its children
print("******** ANCESTORS FOR VALUE: ", targetValue)
print("NODE FOUND: ", nodeFound)

print()
for ancestor in ancestors:
    ancestorValue = Matrix.getAtCoordinate(matrix, ancestor.coord)
    print("ancestor: ", ancestorValue)
    for child in ancestor.children:
        childValue = Matrix.getAtCoordinate(matrix, child.coord)
        print("  > child: ", childValue)



targetValue = 13
(nodeFound, ancestors) = MatrixTree.findOneByValueFrom(matrixTraverser.matrixTree, targetValue, matrix)

print()
# for each ancestor, see its children
print("******** ANCESTORS FOR VALUE: ", targetValue)
print("NODE FOUND: ", nodeFound)

print()
for ancestor in ancestors:
    ancestorValue = Matrix.getAtCoordinate(matrix, ancestor.coord)
    print("ancestor: ", ancestorValue)
    for child in ancestor.children:
        childValue = Matrix.getAtCoordinate(matrix, child.coord)
        print("  > child: ", childValue)
