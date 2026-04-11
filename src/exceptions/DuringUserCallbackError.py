from inspect import isfunction
from src.exceptions.ExpectedUserCallbackError import ExpectedUserCallbackError


class DuringUserCallbackError(Exception):
    """
    Exception raised when an exception
    in a user-defined callback is not caught. 
    """

    def __init__(self, callback, userMessage=""):
        # if the callback is not a function, must throw 
        if not isfunction(callback):
            raise ExpectedUserCallbackError(callback) 

        msg = f"Uncaught exception during execution of user-defined callback '{callback.__name__}'. "
        self.callback = callback
        self.message = msg
        super().__init__(msg)
