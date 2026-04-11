from inspect import isfunction

class ExpectedUserCallbackError(Exception):
    """
    Exception raised when a callback/function is
    expected, but is not found. 
    """

    def __init__(self, obj, userMessage=""):
        # if the callback is actually a function, must throw 
        if isfunction(obj):
            raise Exception(f"The object '{obj}' was thought not to be a function, but it is.")
        
        msg = f"Expected user callback, got type '{type(obj)}' instead, with value: '{obj}'"
        self.message = msg
        
        super().__init__(msg)
