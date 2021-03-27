from django.contrib import admin
from blog.models import Books, Comment

from django.conf.locale.ru import formats as ru_formats
ru_formats.DATE_FORMAT = 'd.m.Y H:i:s'


@admin.register(Books)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'public', 'date_add', 'id')
    fields = ('date_add', ('title', 'public'), 'message')
    readonly_fields = ('date_add', )
    search_fields = ['title', 'message', ]
    list_filter = ('public', )

    def save_model(self, request, obj, form, change):
        # Добавляем текущего пользователя (если не выбран) при сохранении модели
        # docs: https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.save_model
        if not hasattr(obj, 'author') or not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
