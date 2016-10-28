import mock, unittest
from domain.book.BookService import BookService
from books.models import Book
from chefs.models import Chefs
from test_data_provider.ChefDataProvider import ChefDataProvider
from domain.mail.mail import InvalidMailException


class BookServiceTest(unittest.TestCase):
    def setUp(self):
        self.modelStub = mock.Mock()
        self.repositoryStub = mock.Mock()
        self.mailerStub = mock.Mock()
        self.sut = BookService.new(
            model=self.modelStub,
            repository=self.repositoryStub,
            mailer=self.mailerStub
        )

    def test_setCollaborators_should_setCollaboratorsAndSaveBook(self):
        _book = Book()
        _book.set_collaborators = mock.Mock()

        self.modelStub.from_legacy_model.return_value = _book

        self.sut.set_collaborators(Book(), [])
        self.assertTrue(_book.set_collaborators.called)
        self.repositoryStub.save.assert_called_with(_book)

    def test_getBookByCollaborator_should_call_getBooksByCollaborator_from_repository(self):
        chef = Chefs()
        collaborator = Chefs()
        self.sut.getBooksByCollaborator(chef, collaborator)
        self.repositoryStub.getBooksByCollaborator.assert_called_with(chef, collaborator.id)

    def test_notifyCollaborators_should_throw_whenEmailInvalid(self):
        book = Book()
        invalid_collaborators = [
            ChefDataProvider.get().withEmail("invalid-email").build(),
            ChefDataProvider.get().withEmail("user1@mail.com").build()
        ]
        self.assertRaises(InvalidMailException, self.sut.notify_collaborators, book, invalid_collaborators)

    def test_notifyCollaborators_should_sendEmails(self):
        book = Book()
        collaborators = [
            ChefDataProvider.get().withEmail("user1@mail.com").build(),
            ChefDataProvider.get().withEmail("user2@mail.com").build(),
            ChefDataProvider.get().withEmail("user3@mail.com").build()
        ]
        self.sut.notify_collaborators(book, collaborators)
        self.assertEqual(self.mailerStub.send_email.call_count, 3)

    def test_get_recipe_by_book_should_return_expected(self):
        self.repositoryStub.get_recipe_by_books.return_value = 'recipes'
        actual = self.sut.get_recipe_by_books('')
        self.assertEqual(actual, 'recipes')

    def test_check_recipe_belong_to_public_book_should_returnRepositoryResult(self):
        self.repositoryStub.is_recipe_belong_to_public_book.return_value = True
        actual = self.sut.check_recipe_belong_to_public_book('')
        self.assertEqual(actual, True)

    def test_get_recipe_in_public_books(self):
        self.repositoryStub.get_recipe_in_public_books.return_value = 'recipes'
        actual = self.sut.get_recipe_in_public_books()
        self.assertEqual(actual, 'recipes')

    def test_get_recipe_by_following_chef(self):
        self.repositoryStub.get_recipe_in_public_books.return_value = 'recipes'
        actual = self.sut.get_recipe_in_public_books()
        self.assertEqual(actual, 'recipes')
