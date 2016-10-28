import unittest
from legacy_wrapper.legacymodelwrap import legacymodelwrap, WrappedManager


class Manager:
    def get(self, n):
        return LegacyModel(n + 5)

    def get_number(self, n):
        return n + 4


class LegacyModel:
    objects = Manager()

    def __init__(self, n):
        self.n = n


@legacymodelwrap(LegacyModel)
class Model:
    def __init__(self, model):
        self.model = model

    @classmethod
    def from_legacy_model(cls, model):
        return cls(model)

    def get_n(self):
        return self.model.n + 10


class legacymodelwrapTest(unittest.TestCase):
    '''
        legacymodelwrap Test
    '''

    def test_decorator_shouldRaiseErrorIfFromLegacyModelFactoryIsMissing(self):
        def actual():
            @legacymodelwrap(LegacyModel)
            class WrongModel:
                pass

        self.assertRaises(AttributeError, actual)

    def test_decorator_shouldRaiseErrorIfLegacyModelIsMissing(self):
        def actual():
            @legacymodelwrap()
            class WrongModel:
                pass

        self.assertRaises(TypeError, actual)

    def test_decorator_shouldRaiseErrorIfObjectsIsMissing(self):
        def actual():
            class WrongLegacyModel:
                pass
            @legacymodelwrap(WrongLegacyModel)
            class OkModel:
                @classmethod
                def from_legacy_model(cls, model):
                    return cls(model)

        self.assertRaises(AttributeError, actual)

    def test_decorator_shouldDefineObjectsClassProperty(self):
        self.assertTrue(isinstance(Model.objects.legacy_model.objects, Manager))

    def test_afterDecorator_callsOnObjectsThatWouldReturnLegacyModel_shouldReturnModelInstead(self):
        instance = Model.objects.get(3)
        self.assertTrue(isinstance(instance, Model))
        self.assertEquals(instance.get_n(), 18)

    def test_afterDecorator_callsOnObjectsThatWouldNotReturnLegacyModel_shouldReturnTheSameResult(self):
        self.assertEquals(Model.objects.get_number(2), 6)



