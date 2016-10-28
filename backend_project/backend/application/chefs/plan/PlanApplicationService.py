import datetime

from domain.chefs.plan.PlanService import PlanService


class PlanApplicationService:
    def __init__(self, service=PlanService.new()):
        self.service = service

    def getPlanByTypeAndInterval(self, type, interval):
        plan = self.service.getPlanByTypeAndInterval(type, interval)
        due_date = self.__get_next_due_date(plan)
        amount = self._get_payment_amount(plan)
        return dict(
            plan = plan, due_date = due_date, amount = amount
        )

    def get(self, plan_id):
        return self.service.get(plan_id)

    def getPlanType(self):
        return self.service.getPlanType()

    def getPlanInterval(self):
        return self.service.getPlanInterval()

    def __get_next_due_date(self, plan):
        due_date = datetime.datetime.today()
        if(plan.interval == 'monthly'):
            due_date = due_date + datetime.timedelta(days=30)
        else:
            due_date = due_date + datetime.timedelta(days=365)
        return due_date

    def _get_payment_amount(self, plan):
        return plan.amount_per_year if plan.interval == 'annually' else plan.amount_per_month

    @staticmethod
    def new(service=PlanService.new()):
        return PlanApplicationService(service)
