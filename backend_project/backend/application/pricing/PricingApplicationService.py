from domain.pricing.PricingService import PricingService


class PricingApplicationService:
    def __init__(self, pricing_service=PricingService()):
        self.pricing_service = pricing_service

    def getFakeData(self):
        fakeDatas = self.pricing_service.getFakeData()
        for fakeData in fakeDatas:
            arrAmount = self.pricing_service.splitStringIntoTwoParts(fakeData['price']['amount'])
            if len(arrAmount) > 1:
                fakeData['price']['amountBegin'] = arrAmount[0]
                fakeData['price']['amountEnd'] = arrAmount[1]
            else:
                fakeData['price']['amountBegin'] = arrAmount[0]
                fakeData['price']['amountEnd'] = ''
        return fakeDatas
