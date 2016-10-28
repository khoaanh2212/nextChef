from .Subscription import Subscription
from infrastructure.chefs.subscription.SubscriptionRepository import SubscriptionRepository

class SubscriptionService:

    '''Subscription Service'''

    def __init__(self, repository=SubscriptionRepository.new(), model=Subscription):
        self.repository = repository
        self.model = model

    def create(self, chef, plan):
        return self.repository.save(self.model.create(chef, plan))

    def getSubscriptionByUser(self, chef):
        return self.repository.findByUserId(chef.id)

    def update(self, id, subscription_details):
        subscription = self.repository.findById(id)
        return self.repository.save(self.model.update(subscription, subscription_details))

    @staticmethod
    def new(repository=SubscriptionRepository.new(), model=Subscription):
        return SubscriptionService(repository, model)
