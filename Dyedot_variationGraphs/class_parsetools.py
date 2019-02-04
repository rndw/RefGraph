class Ptools():
    '''
    DEV UTILITIES CLASS . NOT REQUIRED/ESSENTIAL
    '''

    def __init__(self):
        pass

    def head(self, n=10):
        return self[:n]

    def tail(self, n=10):
        return self[len(self) - n - 1:]
