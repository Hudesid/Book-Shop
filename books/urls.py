from django.urls import path
from . import views


urlpatterns = [
    path('books/create/', views.BookCreateAPIView.as_view(), name='book-create'),
    path('books/', views.BookListAPIView.as_view(), name='books-list'),
    path('books/detail/<int:pk>/', views.BookRetrieveAPIView.as_view(), name='book-detail'),
    path('my/books/detail/<int:pk>/', views.BookRetrieveUpdateDestroyAPIView.as_view(), name='my-book-detail')
]