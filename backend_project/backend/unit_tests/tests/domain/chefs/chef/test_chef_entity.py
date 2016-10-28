import unittest
from domain.chefs.chef.ChefEntity import ChefEntity
from chefs.models import Chefs
from test_data_provider.ChefDataProvider import ChefDataProvider
from domain.InvalidArgumentException import InvalidDomainArgumentException


class ChefEntityTest(unittest.TestCase):
    '''
        ChefEntity Test
    '''

    def setUp(self):
        self.sut = ChefEntity()
        self.CHEF = ChefDataProvider.getDefault()

    def test_updateMembership_should_throw_if_invalid_membership(self):
        self.assertRaises(InvalidDomainArgumentException, self.sut.updateMembership, self.CHEF, 'invalid')

    def test_updateMembership_should_not_throw_if_valid_membership(self):
        for membership in Chefs.MEMBERSHIP:
            self.sut.updateMembership(self.CHEF, membership[0])
            self.assert_(True)

    def test_updateMembership_should_return_chef_with_updated_membership(self):
        chef = ChefDataProvider.get().withMembership('default')
        membership = 'pro'
        actual = self.sut.updateMembership(chef, membership)
        self.assertEqual(actual.membership, 'pro')
