import unittest, mock
from application.book.BookApplicationService import BookApplicationService
from test_data_provider.ChefDataProvider import ChefDataProvider
from django.test.client import RequestFactory


class BookApplicationServiceTest(unittest.TestCase):
    def setUp(self):
        self.bookServiceStub = mock.Mock()
        self.chefServiceStub = mock.Mock()
        self.sut = BookApplicationService.new(self.bookServiceStub, self.chefServiceStub)
        self.factory = RequestFactory()

    def test__getBookCollaborators_should_callToChefService_GetByIdsWithExpected(self):
        self.chefServiceStub.getByIds.return_value = [1, 2, 3, 4, 5]
        self.sut._getBookCollaborators('1,2,3,4,5')
        self.chefServiceStub.getByIds.assert_called_with([1, 2, 3, 4, 5])

    def test_setBookCollaborator_should_setTheBookWithCollaborators(self):
        self.sut._getBookCollaborators = mock.Mock()
        self.sut._getBookCollaborators.return_value = 'list-chefs'
        request_stub = self.factory.get('/book/')
        request_stub.META = {'HTTP_HOST': 'localhost'}
        self.sut.set_book_collaborators('book', '1,2,3,4,5', request_stub)
        self.bookServiceStub.set_collaborators.assert_called_with('book', 'list-chefs')

    def test_getCollaborators_should_returnListOfChefs(self):
        chef = ChefDataProvider.get() \
            .withName('chef') \
            .withEmail('chef1@mail.com') \
            .withSurname('01') \
            .withId(1) \
            .build()

        collaborators = "[1],[2],[3],[4],"
        self.chefServiceStub.getByIds.return_value = [chef]

        actual = self.sut.getCollaborators(collaborators)
        expected = [{
            'email': 'chef1@mail.com',
            'surname': '01',
            'id': 1,
            'avatar': '/static/img/chef_avatar.jpg',
            'name': 'chef'
        }]

        self.chefServiceStub.getByIds.assert_called_with([1, 2, 3, 4])
        self.assertEqual(actual, expected)

    def test_check_recipe_belong_to_public_book_should_returnBookServiceResult(self):
        self.bookServiceStub.check_recipe_belong_to_public_book.return_value = True
        actual = self.sut.check_recipe_belong_to_public_book('')
        self.assertEqual(actual, True)

    def test_decorate_collaborator_return_expect_string(self):
        actual = self.sut.decorate_collaborators('[4],[5],[6]')
        self.assertEquals(actual, '4,5,6')

    def test_compare_collaborator_should_return_empty_array_if_no_different(self):
        actual = self.sut.compare_collaborator('4,5,6', '6,5,4')
        self.assertEquals(actual, [])

    def test_compare_collaborator_should_return_array_element_different(self):
        actual = self.sut.compare_collaborator('4,5,6', '7,5,2,4,5')
        self.assertEquals(actual, ['7', '2'])

    def test_send_email_collaborator_when_edit_should_call_expect_function_if_have_different_collaborator(self):
        self.sut.compare_collaborator = mock.Mock()
        self.sut.compare_collaborator.return_value = ['7']
        request_stub = self.factory.get('/book/')
        request_stub.META = {'HTTP_HOST': 'localhost'}
        book = mock.Mock()
        self.chefServiceStub.getByIds.return_value = [{}, {}]
        self.sut.send_email_collaborator_when_edit('4,5,6', '4,5,6,7', book, request_stub)
        self.chefServiceStub.getByIds.assert_called_with([7])
        self.bookServiceStub.notify_collaborators.assert_called_with(book, [{},{}], 'localhost')
