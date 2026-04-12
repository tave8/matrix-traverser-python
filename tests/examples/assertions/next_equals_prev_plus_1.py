from src.components import Coordinate


def assertOnCellInfo(cellInfo: dict):
        assert isinstance(cellInfo["prevCoord"], Coordinate)
        assert isinstance(cellInfo["currCoord"], Coordinate)
        assert Coordinate.areAdjacent(cellInfo["currCoord"], cellInfo["prevCoord"])

        # the previous cell is the start, so 
        # to the next cell must be 1
        if cellInfo["prevValue"] == "S":
            assert isinstance(cellInfo["currValue"], int)
            assert cellInfo["currValue"] == 1
        else:
            assert isinstance(cellInfo["prevValue"], int)
            assert isinstance(cellInfo["currValue"], int)
            # for each cell pair in a move, this property must be satisfied
            assert cellInfo["currValue"] == cellInfo["prevValue"] + 1


def assertStartMustExist(cells: list[dict]):
    assert cells[0]["currValue"] == "S" 

def assertEndMustExist(cells: list[dict]):
    assert cells[-1]["currValue"] == "E" 

def assertEndMustNotExist(cells: list[dict]):
    assert cells[-1]["currValue"] != "E" 
