import unittest, mock
from domain.book.Collaborators import Collaborators, InvalidCollaborator
from test_data_provider.ChefDataProvider import ChefDataProvider


class CollaboratorsTest(unittest.TestCase):

    def setUp(self):
        self.sut = Collaborators.new()
        self.CHEF1 = ChefDataProvider().withId(1).withName('first').build()
        self.CHEF2 = ChefDataProvider().withId(2).withName('second').build()

    def test_add_should_addChefToListCollaborators_whenInputValid(self):
        testCases = [
            dict( case = self.CHEF1, expected = [self.CHEF1] ),
            dict( case = [self.CHEF1, self.CHEF2], expected = [self.CHEF1, self.CHEF2] )
        ]
        for testCase in testCases:
            self.sut.collaborators = []
            self.sut.add(testCase['case'])
            self.assertEqual(self.sut.collaborators, testCase['expected'])

    def test_add_should_throw_whenInputInvalid(self):
        testCases = [
            [self.CHEF1, ''], 'CHEF-2', {}, [{}], None
        ]
        for testCase in testCases:
            self.assertRaises(InvalidCollaborator, self.sut.add, testCase)

    def test_toCollaboratorString_should_returnExpected(self):
        self.sut.collaborators = [self.CHEF1, self.CHEF2]
        actual = self.sut.toCollaboratorString()
        self.assertEqual(actual, "[1],[2],")

    def test_collaboratorToList_should_return_list_chef_id(self):
        expected = [1,2]
        actual = self.sut.collaboratorToList('[1],[2]')
        self.assertEquals(actual,expected)