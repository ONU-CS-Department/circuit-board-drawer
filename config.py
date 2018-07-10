class Config():
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.function = lambda: None

    def set(self, key, value):
        setattr(self, key, value)
        if (self.__hasFunction(key) == True):
            self.__callFunction(key)

    def get(self, key):
        return getattr(self, key)

    def registerFunction(self, key, function):
        setattr(self.function, key, function)

    def __hasFunction(self, key):
        try:
            getattr(self.function, key)
            return True
        except AttributeError:
            return False

    def __callFunction(self, key):
        getattr(self.function, key)()

