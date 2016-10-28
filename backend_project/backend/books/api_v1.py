from django.shortcuts import get_object_or_404

from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response

from api_utils.views import CookboothAPIView

from .models import Book
from .serializers import ApiV1BookSerializer, ApiBookBuySerializer, ApiV1ExploreBookSerializer


class BookView(CookboothAPIView):
    def get(self, request, *args, **kwargs):
        """
        View book
        """
        chef = request.user
        book = get_object_or_404(Book, pk=kwargs['pk'])
                
        if book.chef != chef and not book.is_public:
            chef_added_book_ids = request.user.books_added.all().values_list('id',flat=True)
            if not book.id in chef_added_book_ids:
                return self.invalid_request('This book is not available')

        serializer = ApiV1BookSerializer(book)
        serializer.user = chef
        return Response({'book': serializer.data})


class BookBuyView(CookboothAPIView):
    def post(self, request, *args, **kwargs):
        """
        Buy book
        """
        book = get_object_or_404(Book, pk=kwargs['pk'])
        if not book.can_be_sold:
            return self.invalid_request('This book is not available for sale')
        if book.user_has_bought_it(request.user):
            return self.invalid_request('User has already bought this book')

        serializer = ApiBookBuySerializer(data=request.DATA)
        serializer.user = request.user
        if serializer.is_valid():
            book.buy(request.user, serializer.data['vendor'], serializer.data['transaction'])
            return Response({'response': {'return': True}})
        return self.invalid_serializer_response(serializer)


class BooksForSaleView(ListModelMixin, CookboothAPIView):
    serializer_class = ApiV1ExploreBookSerializer

    def get(self, request, *args, **kwargs):
        """
        Get the books for sale
        """
        self.queryset = Book.objects.filter(book_type=Book.TO_SELL, status=Book.AVAILABLE)
        return self.list(request, *args, **kwargs)
