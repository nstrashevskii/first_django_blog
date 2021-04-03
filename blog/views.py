import math

from django.core.paginator import Paginator
from django.db.models import Avg
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Books, Comment
from .serializers import BookSerializer, BookDetailSerializer, BookEditorSerializer, CommentAddSerializer


class BooksView(APIView):
    """ книги для блога """

    def get(self, request, page_number=1):
        """ Получить книги для блога """
        page_size = self.request.query_params.get('page_size', 5)
        # `select_related` - это оптимизация запроса (join). Отношение Один к Одному
        # https://django.fun/docs/django/ru/3.1/ref/models/querysets/#select-related
        books = Books.objects.filter(public=True).order_by('-date_add', 'title').select_related('author')

        # Рассчитать средний рейтинг
        books = books.annotate(average_rating=Avg('comments__rating'))
        paginator = Paginator(books, page_size)
        page_count = math.ceil(Books.objects.count() / page_size)

        if page_count // page_number == 0:
            raise NotFound(f'Нет страницы с номером {page_number}')

        serializer = BookSerializer(paginator.page(page_number), many=True)

        return Response(serializer.data)


class BookDetailView(APIView):

    def get(self, request, book_id):
        """ Получить статю """
        # `prefetch_related` - это оптимизация запроса для отношения Многие к Одному
        # https://django.fun/docs/django/ru/3.1/ref/models/querysets/#prefetch-related
        book = Books.objects.select_related(
            'author'
        ).prefetch_related(
            'comments'
        ).filter(
            pk=book_id, public=True
        ).first()

        if not book:
            raise NotFound(f'Опубликованная книга с id={book_id} не найдена')

        serializer = BookDetailSerializer(book)
        return Response(serializer.data)


class BookEditorView(APIView):

    permission_classes = (IsAuthenticated, )

    def post(self, request):
        """ Новая книга для блога """

        # Передаем в сериалайзер (валидатор) данные из запроса
        new_book = BookEditorSerializer(data=request.data)

        # Проверка параметров
        if new_book.is_valid():
            # Записываем новую статью и добавляем текущего пользователя как автора
            new_book.save(author=request.user)
            return Response(new_book.data, status=status.HTTP_201_CREATED)
        else:
            return Response(new_book.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, book_id):
        """ Правка в книге """

        # Находим редактируемую статью
        book = Books.objects.filter(pk=book_id, author=request.user).first()
        if not book:
            raise NotFound(f'Статья с id={book_id} для пользователя {request.user.username} не найдена')

            # Для сохранения изменений необходимо передать 3 параметра
            # Объект связанный со статьей в базе: `note`
            # Изменяемые данные: `data`
            # Флаг частичного оновления (т.е. можно проигнорировать обязательные поля): `partial`
        new_book = BookEditorSerializer(book, data=request.data, partial=True)

        if new_book.is_valid():
            new_book.save()
            return Response(new_book.data, status=status.HTTP_200_OK)
        else:
            return Response(new_book.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentView(APIView):
    """ Комментарий к статье """
    permission_classes = (IsAuthenticated,)

    def post(self, request, book_id):
        """ Новый комментарий """

        book = Books.objects.filter(pk=book_id).first()
        if not book:
            raise NotFound(f'Статья с id={book_id} не найдена')

        new_comment = CommentAddSerializer(data=request.data)
        if new_comment.is_valid():
            new_comment.save(book=book, author=request.user)
            return Response(new_comment.data, status=status.HTTP_201_CREATED)
        else:
            return Response(new_comment.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_id):
        """ Удалить комментарий """
        comment = Comment.objects.filter(pk=comment_id, author=request.user)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
