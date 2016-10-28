from legacy_wrapper.book_wrapper import Book
from infrastructure.book.BookRepository import BookRepository
from .Collaborators import Collaborators
from infrastructure.mailer_adapter import MailerAdapter
from domain.mail.mail import Mail
import logging
from django.contrib.sites.models import Site
from django.conf import settings


class BookService:
    def __init__(self, model, repository, mail, mailer, logger):
        self.model = model
        self.repository = repository
        self.mail = mail
        self.mailer = mailer
        self.logger = logger

    def set_collaborators(self, book, chefs):
        collaborators = Collaborators.new(chefs)
        _book = self.model.from_legacy_model(book)
        _book.set_collaborators(collaborators)
        self.repository.save(_book)

    def getBooksByCollaborator(self, chef, collaborator):
        return self.repository.getBooksByCollaborator(chef, collaborator.id)

    def notify_collaborators(self, book, collaborators, site_url=settings.SITE_URL):
        for collaborator in collaborators:
            mail = self.mail.new(
                subject='New Book Collaboration',
                message=self._notifyEmailTemplate(collaborator, book, site_url),
                to_email=collaborator.email)
            self.logger.info('sending email to %s', collaborator.email)
            self.mailer.send_email(mail, is_html=True)

    def get_recipe_by_books(self, books):
        return self.repository.get_recipe_by_books(books)

    def get_recipe_by_chef(self, chef):
        return self.repository.get_recipe_by_chef(chef)

    def get_recipe_in_public_books(self):
        return self.repository.get_recipe_in_public_books()

    def get_recipe_by_following_chef(self, chef):
        return self.repository.get_recipe_by_following_chef(chef)

    def get_book_by_chef(self, chef):
        return self.repository.get_book_by_chef(chef)

    def _notifyEmailTemplate(self, collaborator, book, site_url):
        url = 'http://' + site_url + '/library/' + collaborator.name + '-' + collaborator.surname + '-' + str(
            collaborator.id)
        return "<html>Hi %s, <br/>" \
               "You have been invited to collaborate in this book: <a href='%s'>%s</a><br/>" \
               "Best regards." \
               "</html>" % (collaborator.username, url, book.name)

    def check_recipe_belong_to_public_book(self, recipe):
        return self.repository.is_recipe_belong_to_public_book(recipe)

    def check_chef_is_collaborator_of_recipe(self, chef, recipe):
        return self.repository.is_collaborator_of_recipe(chef.id, recipe)

    @staticmethod
    def new(
            model=Book,
            repository=BookRepository.new(),
            mail=Mail,
            mailer=MailerAdapter.new(),
            logger=logging.getLogger('Book')
    ):
        return BookService(model, repository, mail, mailer, logger)
