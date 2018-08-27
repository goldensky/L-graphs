
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({0}, {1})'.format(self.type, repr(self.value))

    def __repr__(self):
        return self.__str__()