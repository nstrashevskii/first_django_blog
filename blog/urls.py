from django.urls import path, include
from . import views


app_name = 'blog'
urlpatterns = [
    path('books/', views.BooksView.as_view(), name='books'),
    path('book/<int:book_id>/', views.BookDetailView.as_view(), name='book'),
    path('book/add/', views.BookEditorView.as_view(), name='add')
]