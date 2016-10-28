from domain.InvalidArgumentException import InvalidDomainArgumentException
from django.conf import settings


class InvalidAllergen(InvalidDomainArgumentException):
    pass


ALLERGEN_TITLES = map(lambda a : a[1], settings.NC_ALLERGENS)

class Allergen:
    def __init__(self, name):
        if name not in ALLERGEN_TITLES:
            raise InvalidAllergen(name)
        self.name = name

    def getAllergenName(self):
        return self.name


def to_allergens(allergen_list):
    return map(lambda x: Allergen(x.strip()).getAllergenName(), filter(lambda x: x, allergen_list))


class SelectedAllergens:
    def __init__(self, allergens):
        self.allergens = set(to_allergens(allergens))

    @staticmethod
    def new(allergens=list()):
        return SelectedAllergens(allergens)

    def add(self, allergen):
        self.allergens.add(allergen.getAllergenName())

    def remove(self, allergen):
        if allergen.getAllergenName() in self.allergens:
            self.allergens.remove(allergen.getAllergenName())

    def __str__(self):
        self.allergens = list(set(self.allergens))
        return ', '.join(self.allergens)

    def toAllergenString(self):
        return self.__str__()

class EdamamSelectedAllergens:
    def __init__(self, edamam_allergens_free):
        self.selected_allergens = self._filterAllergens(edamam_allergens_free)

    def _filterAllergens(self, edamam_allergens_free):
        edamam_allergens = filter(lambda a : a[1] not in edamam_allergens_free, settings.EDAMAM_ALLERGENS)
        allergen_keys = map(lambda a : a[0], edamam_allergens)
        allergens = filter(lambda a : a[0] in allergen_keys, settings.NC_ALLERGENS)
        return map(lambda a : a[1], allergens)

    def __str__(self):
        return ', '.join(self.selected_allergens)

    def to_allergen_string(self):
        return self.__str__()

    @staticmethod
    def new(edamam_allergens_free=list()):
        return EdamamSelectedAllergens(edamam_allergens_free)
