from django.conf import settings


class InvalidCostingIngredientArgumentException(Exception):
    pass


class CostingIngredient:
    def __init__(self, ingredient, family='', quantity=1, unit=settings.UNIT_KG, gross_price=0, waste=0, net_price=0,
                 supplier='', comment=''):
        self.ingredient = string(ingredient)
        self.family = string(family)
        self.quantity = positive_all_kind_float_number(quantity, 1)
        self.unit = unit if unit else settings.UNIT_KG
        self.gross_price = positive_float_number(gross_price)
        self.waste = positive_integer_number(waste)
        self.net_price = positive_float_number(net_price)
        self.supplier = string(supplier)
        self.comment = string(comment)


def positive_integer_number(str, min_value=0):
    if not str:
        return min_value

    try:
        number = int(str)
        if number < 0:
            raise InvalidCostingIngredientArgumentException
        return number if number >= min_value else min_value

    except ValueError:
        raise InvalidCostingIngredientArgumentException


def positive_float_number(str, min_value=0):
    if not str:
        return min_value

    try:
        number = float(str)
        if number < 0:
            raise InvalidCostingIngredientArgumentException
        return number if number >= min_value else min_value

    except ValueError:
        raise InvalidCostingIngredientArgumentException


def positive_all_kind_float_number(str, min_value):
    if not str:
        return min_value

    try:
        number = float(str)
        return number
    except ValueError:
        raise InvalidCostingIngredientArgumentException


def string(str):
    return str if str else ""
