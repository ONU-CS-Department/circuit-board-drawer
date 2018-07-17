"""
This module allows configuration key/value pairs to be stored and retrieved.
Functions can be associated with a key to be called when a value is altered
via the "set" method.
"""
class Config():
    def __init__(self, **kwargs):
        """Construct the object and assign passed in values to self

        Keyword arguments:
        kwards -- arbitrary number of keyword arguments
        """
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.function = lambda: None

    def set(self, key, value):
        """Adds a key/value pair to self and calls associated functions

        Keyword arguments:
        key -- key to hold a value
        value -- the value held by the key
        """
        setattr(self, key, value)
        if (self.__hasFunction(key) == True):
            self.__callFunction(key)

    def get(self, key):
        """Get the value held by a key

        Keyword arguments:
        key -- key that holds a value
        """
        return getattr(self, key)

    def registerFunction(self, key, function):
        """Register a function to be called each time set is called on a key

        Keyword arguments:
        key -- key to associate a function
        function -- the associated function
        """
        setattr(self.function, key, function)

    def __hasFunction(self, key):
        """Return 'True' if key has an associated function

        Keyword arguments:
        key -- key with an associated function
        """
        try:
            getattr(self.function, key)
            return True
        except AttributeError:
            return False

    def __callFunction(self, key):
        """Execute a key's associated function

        Keyword arguments:
        key -- key with an associated function
        """
        getattr(self.function, key)()

