from domain.chefs.plan.Plan import Plan
from infrastructure.BaseRepository import BaseRepository

class PlanRepository(BaseRepository):

    def __init__(self, model=Plan):
        BaseRepository.__init__(self, model)

    def findByTypeAndInterval(self, type, interval):
        return self.model.objects.get(type=type, interval=interval)

    def findPlanType(self):
        return self.model.PLAN_CHOICES

    def findPlanInterval(self):
        return self.model.INTERVAL_CHOICES

    @staticmethod
    def new(model=Plan):
        return PlanRepository(model)
