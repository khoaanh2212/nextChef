# import unittest
# from infrastructure.book.BookRepository import BookRepository
# from chefs.models import Chefs
#
# class BookRepositoryTest(unittest.TestCase):
#     sut = BookRepository.new()
#
#     def test_whenGetBookByChefId_returnExpectedList(self):
#         chef = Chefs.objects.create_user('Test', 'Tests', 'test@example.com', 'secret')
#         self.sut.model.objects.create(name='book_name_1', collaborators='[1]', chef=chef)
#         actual = self.sut.get_book_by_id_and_collaborator(chef)
#         self.assertEqual(actual.__len__(), 1)
#
#     def test_whenGetBookBycollaboratorId_returnExpectedList(self):
#         chef = Chefs.objects.create_user('Test', 'Tests', 'otherTest@example.com', 'secret')
#         self.sut.model.objects.create(name='book_name_1', collaborators='[%s],[2],[3],' % chef.id)
#         self.sut.model.objects.create(name='book_name_2', collaborators='[3],[4],[5],')
#         actual = self.sut.get_book_by_id_and_collaborator(chef)
#         self.assertEqual(actual.__len__(), 1)
