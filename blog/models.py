from django.db import models


class Books(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    message = models.TextField(default='', verbose_name='Текст')
    date_add = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    public = models.BooleanField(default=False, verbose_name='Опубликовать')

    def __str__(self):
        return self.title
# Create your models here.
