from .Plan import Plan
from infrastructure.chefs.plan.PlanRepository import PlanRepository


class PlanService:

    '''Plan Service'''

    def __init__(self, repository=PlanRepository.new(), model=Plan):
        self.repository = repository
        self.model = model

    def create(self, type, interval, amount_per_month):
        return self.repository.save(self.model.create(type, interval, amount_per_month))

    def getPlanByTypeAndInterval(self, type, interval):
        return self.repository.findByTypeAndInterval(type, interval)

    def get(self, id):
        return self.repository.findById(id)

    def getPlanType(self):
        return self.repository.findPlanType()

    def getPlanInterval(self):
        return self.repository.findPlanInterval()

    @staticmethod
    def new(repository=PlanRepository.new(), model=Plan):
        return PlanService(repository, model)
