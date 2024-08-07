class JsonStatException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class JsonStatMalformedJson(JsonStatException):
    pass
