class InvalidFloatNumberException(Exception):
    pass


class PositiveFloatNumber:

    def __init__(self, number):
        try:
            self.number = float(number)
            if self.number < 0:
                raise InvalidFloatNumberException
        except ValueError:
            raise InvalidFloatNumberException
