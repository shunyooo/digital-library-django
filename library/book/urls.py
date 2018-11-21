from django.urls import path

from . import views

urlpatterns = [
    path('', views.BookListView.as_view(), name='index'),
    path('<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('upload', views.FileFieldView.as_view(), name='book_upload'),
]