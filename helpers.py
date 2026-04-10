from inspect import isfunction


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