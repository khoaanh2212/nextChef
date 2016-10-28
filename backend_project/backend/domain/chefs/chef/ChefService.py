from .ChefEntity import ChefEntity
from chefs.models import Chefs
from infrastructure.chefs.chef.ChefRepository import ChefRepository
from domain.chefs.chef.ChefObject import Chef


class ChefService:
    def __init__(self, repository, model):
        self.repository = repository
        self.model = model

    def upgradeMembership(self, id, membership):
        chef = self.repository.findById(id)
        return self.repository.save(self.model.updateMembership(chef, membership))

    def cancelMembership(self, id):
        chef = self.repository.findById(id)
        return self.repository.save(self.model.updateMembership(chef, Chefs.MEMBERSHIP_DEFAULT))

    def getByIds(self, ids):
        return self.repository.findById(ids)

    def getByEmails(self, email):
        return self.repository.get_chef_by_email(email)

    @staticmethod
    def new(repository=ChefRepository.new(), model=ChefEntity()):
        return ChefService(repository, model)

    @staticmethod
    def collaborator_list(chefs_list):
        result = {
            'chefs': [],
            'readmore': False
        }

        num = 0
        for chef in chefs_list:
            num += 1
            if num <= 20:
                result['chefs'].append(Chef(chef).toDTO())
            elif num > 20:
                result['readmore'] = True

        return result
