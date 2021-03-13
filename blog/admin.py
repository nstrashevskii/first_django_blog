from django.contrib import admin
from blog.models import Books


@admin.register(Books)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'public', 'date_add', 'id')
    fields = ('date_add', ('title', 'public'), 'message')
    readonly_fields = ('date_add', )
    search_fields = ['title', 'message', ]
    list_filter = ('public', )

# Register your models here.
