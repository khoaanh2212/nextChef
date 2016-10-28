from infrastructure.costing.CostingIngredientViewRepository import CostingIngredientViewRepository


class CostingIngredientService:

    def __init__(self, repository):
        self.repository = repository

    @staticmethod
    def new(repository=CostingIngredientViewRepository.new()):
        return CostingIngredientService(repository)

    def get_by_recipe_id(self, recipe_id):
        return self.repository.find_by_chef_id(chef_id=recipe_id)

    def get_suggestion_list(self, chef, filter, page):
        return self.repository.find_by_chef_id(chef_id=chef.id, filter=filter, page=page, is_suggestion_list=True)

    def count_suggestion_list(self, chef, filter):
        return self.repository.count_by_chef_id(chef.id, filter)

    def get_costing_table(self, chef, filter='', page=1):
        return self.repository.find_by_chef_id(chef_id=chef.id, filter=filter, page=page)
