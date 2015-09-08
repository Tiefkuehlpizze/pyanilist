
class AmbigiousCallError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class NotAuthenticatedError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class ApiError(Exception):
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc
    def __str__(self):
        return repr(self.value)
