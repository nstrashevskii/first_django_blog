from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Books
from .serializers import BookSerializer, AuthorSerializer, BookDetailSerializer, BookEditorSerializer


class BooksView(APIView):
    """ Статьи для блога """

    def get(self, request):
        """ Получить статьи для блога """
        notes = Books.objects.filter(public=True).order_by('-date_add', 'title')
        serializer = BookSerializer(notes, many=True)

        return Response(serializer.data)


class BookDetailView(APIView):

    def get(self, request, book_id):
        """ Получить статю """
        book = Books.objects.filter(pk=book_id, public=True).first()

        if not book:
            raise NotFound(f'Опубликованная книга с id={book_id} не найдена')

        serializer = BookDetailSerializer(book)
        return Response(serializer.data)


class BookEditorView(APIView):

    def post(self, request):
        """ Новая статья для блога """

        # Передаем в сериалайзер (валидатор) данные из запроса
        new_note = BookEditorSerializer(data=request.data)

        # Проверка параметров
        if new_note.is_valid():
            # Записываем новую статью и добавляем текущего пользователя как автора
            new_note.save(author=request.user)
            return Response(new_note.data, status=status.HTTP_201_CREATED)
        else:
            return Response(new_note.errors, status=status.HTTP_400_BAD_REQUEST)
