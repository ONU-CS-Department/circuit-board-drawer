class Config():
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.function = lambda: None

    def set(self, key, value):
        setattr(self, key, value)
        if (self.hasFunction(key) == True):
            self.callFunction(key)

    def get(self, key):
        return getattr(self, key)

    def registerFunction(self, key, function):
        setattr(self.function, key, function)

    def hasFunction(self, key):
        try:
            getattr(self.function, key)
            return True
        except AttributeError:
            return False

    def callFunction(self, key):
        getattr(self.function, key)()

config = Config(test="hello")
def test():
    print("Hello there")
config.registerFunction("test", lambda: test())

print(config.hasFunction("test"))

