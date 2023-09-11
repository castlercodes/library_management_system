from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.get_books, name='get_books'),
    path('checked_out_books_user/', views.get_books_checked_out_by_user, name="get_books_user"),
    path('books/<int:book_id>', views.get_book, name='get_book'),
    path('books/create/', views.create_book, name='create_book'),
    path('books/<int:book_id>/update/', views.update_book, name='update_book'),
    path('books/<int:book_id>/delete/', views.delete_book, name='delete_book'),
    path('books/<int:book_id>/check_out', views.check_out_book, name="check_out_book"),
    path('books/<int:book_id>/return', views.return_book, name="return_book"),
    path('login/', views.Login, name='login'),
    path('register/', views.register, name='register'),
]
