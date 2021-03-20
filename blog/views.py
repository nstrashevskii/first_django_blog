from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Books
from .serializers import NoteSerializer


class BlogListView(APIView):
    """ BlogListView """
    def get(self, request):
        books = Books.objects.filter(public=True)

        res = []
        for book in books:
            res.append({
                'id': book.id,
                'title': book.title,
                'author': {
                    'id': book.author.id,
                    'username': book.author.username,
                }
            })

        return Response(res)


class BlogViewMix(generics.ListAPIView):
    queryset = Books.objects.all()
    serializer_class = NoteSerializer
