from infrastructure.chefs.chef.ChefRepository import ChefRepository
from integration_tests.integration_test_case import IntegrationTestCase


class ChefRepositoryTest(IntegrationTestCase):
    sut = ChefRepository.new()

    def test_whenGetChefByNameButDontHaveAnyResult_returnEmptyList(self):
        actual = self.sut.get_chef_by_name('something different')
        self.assertEqual(actual.__len__(), 0)

    def test_whenGetChefByName_returnChefsWithNameAndSurnameSameKeyword(self):
        self.save_chef(name='name_01', surname='something_01', email='test_email_01@hotmail.com')
        self.save_chef(name='something_02', surname='surname_02', email='test_email_02@hotmail.com')
        self.save_chef(name='diff_02', surname='diff_02', email='test_email_03@hotmail.com')
        self.save_chef(name='diff_03', surname='diff_03', email='test_email_03_name@hotmail.com')
        actual = self.sut.get_chef_by_name('name')
        self.assertEqual(actual.__len__(), 3)

    def test_WhenGetChefByName_ReturnLimitChef(self):
        limit = 21

        for n in range(0, 30):
            self.save_chef(name='keyword_%s' % n, surname='keyword_%s' % n, email='test_limit_email_%s@hotmail.com' % n)

        actual = self.sut.get_chef_by_name('keyword')
        self.assertEqual(actual.__len__(), limit)

    def test_WhenGetChefByNameWithNumberOfLimit_returnExpectedList(self):
        for n in range(0, 30):
            self.save_chef(name='limit_paging_%s' % n, surname='limit_paging_%s' % n,
                           email='test_limit_paging_%s@hotmail.com' % n)

        actual = self.sut.get_chef_by_name('limit_paging', limit=2)
        self.assertEqual(actual.__len__(), 10)

    def test_findById_should_returnListOfChefs_whenInputIsList(self):
        list_ids = []
        for n in range(0, 10):
            chef = self.save_chef(name='chef_%s' % n, surname='chef_as%s' % n, email='email_%s@mail.com' % n)
            list_ids.append(chef.id)

        actual = self.sut.findById(list_ids)
        actual = map(lambda x: x.id, actual)
        self.assertEqual(actual, list_ids)
        self.sut.model.objects.filter(id__in=list_ids).delete()

    def test_findById_should_returnListOfChefs_whenInputContainInvalidId(self):
        list_ids = []
        for n in range(0, 10):
            chef = self.save_chef(name='chef_%s' % n, surname='chef_as%s' % n, email='email_%s@mail.com' % n)
            list_ids.append(chef.id)

        wrong_list_ids = list_ids[:]
        wrong_list_ids.append(12345)

        actual = self.sut.findById(wrong_list_ids)
        self.assertEqual(len(actual), 10)
        self.sut.model.objects.filter(id__in=list_ids).delete()

    def save_chef(self, **kwargs):
        return self.sut.model.objects.create(**kwargs)
