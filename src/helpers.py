from inspect import isfunction
from typing import List

# library
from treelib import Tree


class Ensure:

    @staticmethod
    def matrixTraverserHasOnlyAllowedCallbacks(callbackMap: dict) -> None:
        """
        Ensures that the matrix traverser
        only has allowed callbacks.
        This prevents the users
        (which can be subtypes like Maze Traverser or
        human beings themselves)
        from typying/passing callbacks that don't exist,
        at the same time while being convinced that it exists.
        (silent error = callbacks not triggering, for example)
        """

        if not isinstance(callbackMap, dict):
            raise Exception("the given map is not a dictionary")

        allowedCallbackNames = Ensure.getAllowedCallbackNames()

        for callbackName, callback in callbackMap.items():
            if callbackName not in allowedCallbackNames:
                raise Exception(f"in callback map, the key '{callbackName}' "
                                +f"is not allowed or has not been mapped "
                                +"to allowed callback names. allowed callback names: "
                                +Ensure.getAllowedCallbackNamesAsStr())

            if not isfunction(callback):
                raise Exception(f"in callback map, for the key '{callbackName}' "
                                +f"the value should be a function."
                                +f"got {type(callback)} instead.")

    @staticmethod
    def getAllowedCallbackNames() -> List[str]:
        return [
            "canMoveTo",
            "getNextMoves",
            "afterAllFutureMoves"
        ]


    @staticmethod
    def getAllowedCallbackNamesAsStr() -> str:
        return ", ".join(Ensure.getAllowedCallbackNames())


class MatrixTreeVisualizer:
    pass



class FunctionHelper:
    
    @staticmethod
    def mapHasFunction(key: str, _map: dict[str, any]) -> bool: # type: ignore
        """
        Does the given dictionary, at the given key,
        have a function as value?
        """
        if not isinstance(_map, dict):
            raise Exception("the given map is not a dictionary")
         
        return key in _map and isfunction(_map[key])