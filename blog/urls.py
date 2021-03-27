from django.urls import path, include
from . import views


app_name = 'blog'
urlpatterns = [
    path('books/', views.BooksView.as_view(), name='books'),
    path('book/<int:book_id>/', views.BookDetailView.as_view(), name='book'),
    path('book/add/', views.BookEditorView.as_view(), name='add'),
    path('book/edit/<int:book_id>/', views.BookEditorView.as_view(), name='edit'),

    path('comment/<int:book_id>/add/', views.CommentView.as_view(), name='comment_add'),
    path('comment/<int:comment_id>/del/', views.CommentView.as_view(), name='comment_del'),
]