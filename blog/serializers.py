from rest_framework import serializers
from .models import Books, Comment
from datetime import datetime
from django.contrib.auth.models import User


class BookSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Books
        fields = ['id', 'title', 'message', 'public', 'author', ]


class AuthorSerializer(serializers.ModelSerializer):
    """ Автор статьи """

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'date_joined')


class BookDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Books
        exclude = ('public',)  # Исключить эти поля


class BookEditorSerializer(serializers.ModelSerializer):
    """ Добавление или изменение статьи """
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Books
        fields = "__all__"
        read_only_fields = ['date_add', 'author', ]  # Только для чтения


class BookMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ('id', 'title', )


class CommentAddSerializer(serializers.ModelSerializer):
    """ Добавление комментария """
    author = AuthorSerializer(read_only=True)
    book = BookMiniSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ['date_add', 'author', 'book']  # Только для чтения
