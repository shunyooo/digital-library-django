from django.urls import path

from . import views

app_name='book'
urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('list', views.BookListView.as_view(), name='list'),
    path('<int:pk>/', views.BookDetailView.as_view(), name='detail'),
    path('upload', views.FileFieldView.as_view(), name='upload'),
]