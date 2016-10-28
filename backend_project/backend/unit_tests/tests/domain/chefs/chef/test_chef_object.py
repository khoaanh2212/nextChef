import unittest, mock
from domain.chefs.chef.ChefObject import Chef
from test_data_provider.ChefDataProvider import ChefDataProvider


class ChefTest(unittest.TestCase):

    def setUp(self):
        self.sut = Chef

    def toDTO(self):
        chef = ChefDataProvider.get()\
            .withId(1)\
            .withName('first')\
            .withSurname('surname')\
            .withEmail('first@mail.com')

        chef.avatar_thumb = mock.Mock()
        chef.avatar_thumb.return_value = 'avatar_link'

        expected = {
            'id': 1,
            'name': 'first',
            'surname': 'surname',
            'email': 'first@mail.com',
            'avatar': 'avatar_link'
        }

        sut = self.sut(chef)
        actual = sut.toDTO()

        self.assertEqual(actual, expected)
