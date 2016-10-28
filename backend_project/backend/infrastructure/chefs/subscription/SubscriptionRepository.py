from infrastructure.BaseRepository import BaseRepository
from domain.chefs.subscription.Subscription import Subscription

class SubscriptionRepository(BaseRepository):
    def __init__(self, model=Subscription):
        BaseRepository.__init__(self, model)

    @staticmethod
    def new(model=Subscription):
        return SubscriptionRepository(model)
