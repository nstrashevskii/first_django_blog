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


class CommentsSerializer(serializers.ModelSerializer):
    """ Комментарии и оценки. Используется в методе: `/note/{note_id}/` Статя блога """
    author = AuthorSerializer(read_only=True)

    # Меняем название параметра в ответе
    comment_id = serializers.SerializerMethodField('get_comment_id')

    def get_comment_id(self, obj):
        return obj.pk

    # Переопределяем параметр в ответе
    rating = serializers.SerializerMethodField('get_rating')

    def get_rating(self, obj):
        return {
            'value': obj.rating,
            'display': obj.get_rating_display()
        }

    class Meta:
        model = Comment
        fields = ('comment_id', 'rating', 'message', 'date_add', 'author',)


class BookDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    comments = CommentsSerializer(many=True, read_only=True)

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
        fields = ('id', 'title',)


class CommentAddSerializer(serializers.ModelSerializer):
    """ Добавление комментария """
    author = AuthorSerializer(read_only=True)
    book = BookMiniSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ['date_add', 'author', 'book']  # Только для чтения
