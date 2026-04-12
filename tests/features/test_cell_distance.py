from core.MatrixTraverser import Coordinate


# ---- isDistant ----

def test_cell_with_same_coord_is_distance_0():
    coord = Coordinate(2, 2)
    other = Coordinate(2, 2)
    assert coord.isDistant(other, 0) == True

def test_same_cell_is_distance_0():
    coord = Coordinate(2, 2)
    assert coord.isDistant(coord, 0) == True

def test_adjacent_cell_right_is_distance_1():
    coord = Coordinate(2, 2)
    other = Coordinate(2, 3)
    assert coord.isDistant(other, 1) == True

def test_adjacent_cell_below_is_distance_1():
    coord = Coordinate(2, 2)
    other = Coordinate(3, 2)
    assert coord.isDistant(other, 1) == True

def test_diagonal_adjacent_cell_is_distance_1():
    coord = Coordinate(2, 2)
    other = Coordinate(3, 3)
    assert coord.isDistant(other, 1) == True

def test_cell_two_steps_right_is_distance_2():
    coord = Coordinate(2, 2)
    other = Coordinate(2, 4)
    assert coord.isDistant(other, 2) == True

def test_cell_two_steps_diagonal_is_distance_2():
    coord = Coordinate(2, 2)
    other = Coordinate(4, 4)
    assert coord.isDistant(other, 2) == True

def test_cell_is_not_distance_2_when_adjacent():
    coord = Coordinate(2, 2)
    other = Coordinate(2, 3)
    assert coord.isDistant(other, 2) == False

def test_distance_is_symmetric():
    coord = Coordinate(2, 2)
    other = Coordinate(5, 5)
    assert coord.isDistant(other, 3) == other.isDistant(coord, 3)

def test_asymmetric_distance_uses_max():
    # row diff = 1, col diff = 3 → distance should be 3
    coord = Coordinate(2, 2)
    other = Coordinate(3, 5)
    assert coord.isDistant(other, 3) == True


# ---- isAdjacent ----

def test_cell_to_the_right_is_adjacent():
    coord = Coordinate(2, 2)
    assert coord.isAdjacent(Coordinate(2, 3)) == True

def test_cell_to_the_left_is_adjacent():
    coord = Coordinate(2, 2)
    assert coord.isAdjacent(Coordinate(2, 1)) == True

def test_cell_above_is_adjacent():
    coord = Coordinate(2, 2)
    assert coord.isAdjacent(Coordinate(1, 2)) == True

def test_cell_below_is_adjacent():
    coord = Coordinate(2, 2)
    assert coord.isAdjacent(Coordinate(3, 2)) == True

def test_diagonal_cell_is_adjacent():
    coord = Coordinate(2, 2)
    assert coord.isAdjacent(Coordinate(3, 3)) == True

def test_same_cell_is_not_adjacent():
    coord = Coordinate(2, 2)
    assert coord.isAdjacent(Coordinate(2, 2)) == False

def test_cell_two_steps_away_is_not_adjacent():
    coord = Coordinate(2, 2)
    assert coord.isAdjacent(Coordinate(2, 4)) == False

def test_adjacency_is_symmetric():
    coord = Coordinate(2, 2)
    other = Coordinate(3, 3)
    assert coord.isAdjacent(other) == other.isAdjacent(coord)