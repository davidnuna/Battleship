# The module that contains custom exceptions

class InvalidUI(Exception):
    pass

class InvalidCoordinates(Exception):
    pass

class InvalidBattleship(Exception):
    pass

class AreaTaken(Exception):
    pass

class SquareAlreadyHit(Exception):
    pass