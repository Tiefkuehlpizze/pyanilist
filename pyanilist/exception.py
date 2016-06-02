class AmbigiousCallError(BaseException):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return '%s: %s' % (self.__class__.__name__, self.desc)


class NotAuthenticatedError(BaseException):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return '%s: %s' % (self.__class__.__name__, self.desc)


class ApiError(BaseException):
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc

    def __str__(self):
        return '%s: [%s] %s' % (self.__class__.__name__, self.name, self.desc)
