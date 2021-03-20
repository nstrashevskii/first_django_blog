from rest_framework import serializers
from .models import Books


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ['id', 'title', 'message', 'public', ]