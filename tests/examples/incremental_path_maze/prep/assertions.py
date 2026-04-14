from src.components import Coordinate


def assertOnCellInfo(cellInfo: dict):
        assert isinstance(cellInfo["prevCoord"], Coordinate)
        assert isinstance(cellInfo["currCoord"], Coordinate)
        assert Coordinate.areAdjacent(cellInfo["currCoord"], cellInfo["prevCoord"])

        # if this is the very start (before start -> start)
        if cellInfo["prevCoord"].isBeforeStart:
           assert cellInfo["currCoord"].isStart  
        
        # if the previous cell is start, the next must be 1
        elif cellInfo["prevCoord"].isStart:
            assert isinstance(cellInfo["currValue"], int)
            assert cellInfo["currValue"] == 1

        # for every other cell
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
