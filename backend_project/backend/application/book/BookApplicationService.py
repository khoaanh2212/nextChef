from domain.book.BookService import BookService
from domain.chefs.chef.ChefService import ChefService
from domain.chefs.chef.ChefObject import Chef


class InvalidBookArgumentException(Exception):
    pass


class InvalidBookCollaboratorException(Exception):
    pass


class BookApplicationService:
    def __init__(self, book_service, chef_service):
        self.book_service = book_service
        self.chef_service = chef_service

    def set_book_collaborators(self, book, collaborator_ids, request):
        site_url = request.META['HTTP_HOST']
        book_collaborators = self._getBookCollaborators(collaborator_ids)
        self.book_service.set_collaborators(book, book_collaborators)
        self.book_service.notify_collaborators(book, book_collaborators, site_url)

    def _getBookCollaborators(self, collaborator_ids):

        if not collaborator_ids or collaborator_ids == '':
            return list()

        collaborator_id_list = map(lambda x: int(x), collaborator_ids.split(","))
        book_collaborators = self.chef_service.getByIds(collaborator_id_list)
        if len(book_collaborators) != len(collaborator_id_list):
            raise InvalidBookCollaboratorException

        return book_collaborators

    def getCollaborators(self, collaborator_ids):
        collaborator_id_list = filter(lambda x: x != '', map(lambda x: x, collaborator_ids.split(",")))
        collaborator_id_list = map(lambda x: int(x.replace('[', '').replace(']', '')), collaborator_id_list)
        chefs = self.chef_service.getByIds(collaborator_id_list)
        return map(lambda x: Chef(x).toDTO(), chefs)

    def getBooksByCollaborator(self, chef, collaborator):
        return self.book_service.getBooksByCollaborator(chef, collaborator)

    def get_book_by_chef(self, chef):
        return self.book_service.get_book_by_chef(chef)

    def check_recipe_belong_to_public_book(self, recipe):
        return self.book_service.check_recipe_belong_to_public_book(recipe)

    def check_chef_is_collaborator_of_recipe(self, chef, recipe):
        return self.book_service.check_chef_is_collaborator_of_recipe(chef, recipe)

    def decorate_collaborators(self, collaborator_ids):
        collaborator_ids = collaborator_ids.replace('[', '')
        collaborator_ids = collaborator_ids.replace(']', '')
        return collaborator_ids

    def send_email_collaborator_when_edit(self, old_collaborators, new_collaborators, book, request):
        different_collaborator = self.compare_collaborator(old_collaborators, new_collaborators)
        site_url = request.META['HTTP_HOST']
        if len(different_collaborator) > 0:
            collaborator_id_list = map(lambda x: int(x), different_collaborator)
            book_collaborators = self.chef_service.getByIds(collaborator_id_list)
            self.book_service.notify_collaborators(book, book_collaborators, site_url)

    def compare_collaborator(self, old_collaborator_ids, new_collaborator_ids):
        arr_old_ids = old_collaborator_ids.split(',')
        arr_new_ids = new_collaborator_ids.split(',')
        arr_compare = []
        for newItem in arr_new_ids:
            if newItem not in arr_old_ids and not newItem == '':
                arr_compare.append(newItem)

        return arr_compare

    @staticmethod
    def new(book_service=BookService.new(), chef_service=ChefService.new()):
        return BookApplicationService(book_service, chef_service)
