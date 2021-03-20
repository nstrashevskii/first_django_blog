from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Books
from .serializers import NoteSerializer


class BlogListView(APIView):
    """ BlogListView """
    def get(self, request):
        notes = Books.objects.filter(public=True)

        res = []
        for note in notes:
            res.append({
                'id': note.id,
                'title': note.title,
                'author': {
                    'id': note.author.id,
                    'username': note.author.username,
                }
            })

        return Response(res)


class BlogViewMix(generics.ListAPIView):
    queryset = Books.objects.all()
    serializer_class = NoteSerializer
