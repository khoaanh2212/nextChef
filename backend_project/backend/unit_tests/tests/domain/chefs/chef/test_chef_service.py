import unittest
from mock import Mock

from domain.chefs.chef.ChefService import ChefService
from test_data_provider.ChefDataProvider import ChefDataProvider

class ChefServiceTest(unittest.TestCase):
    '''
        ChefService Test
    '''

    def setUp(self):
        self.repository = Mock()
        self.model = Mock()

        self.sut = ChefService.new(self.repository, self.model)

        self.repository.save.return_value = 'result'
        self.repository.findById.return_value = 'chef'
        self.model.updateMembership.return_value = 'updated'

    def test_upgradeMembership_should_call_repository_upgradeMemberShip(self):
        actual = self.sut.upgradeMembership(1, 'membership')
        self.repository.save.assert_called_with('updated')
        self.model.updateMembership.assert_called_with('chef', 'membership')
        self.assertEqual(actual, 'result')

    def test_cancelMembership_should_set_membership_to_default(self):
        actual = self.sut.cancelMembership(1)
        self.repository.save.assert_called_with('updated')
        self.model.updateMembership.assert_called_with('chef', 'default')
        self.assertEqual(actual, 'result')

    def test_getByIds_should_call_findById_from_repository(self):
        self.sut.getByIds(1)
        self.repository.findById.assert_called_with(1)

    def test_collaboratorList_whenGetSmallList_returnExpectedResult(self):
        chefs_list = [self.mk_chef_object(name='name%s' % item,
                                          surname='surname%s' % item,
                                          email='email%s@cmail.com' % item) for item in range(10)]
        actual = self.sut.collaborator_list(chefs_list)
        self.assertEqual(actual['chefs'].__len__(), 10)
        self.assertEqual(actual['readmore'], False)

    def test_collaboratorList_whenGetBiggerList_returnExpectedResult(self):
        chefs_list = [self.mk_chef_object(name='name%s' % item,
                                          surname='surname%s' % item,
                                          email='email%s@cmail.com' % item) for item in range(21)]
        actual = self.sut.collaborator_list(chefs_list)
        self.assertEqual(actual['chefs'].__len__(), 20)
        self.assertEqual(actual['readmore'], True)

    def mk_chef_object(self, **kwargs):
        return self.model.objects.create(
            name=kwargs['name'],
            surname=kwargs['surname'],
            email=kwargs['email']
        )
