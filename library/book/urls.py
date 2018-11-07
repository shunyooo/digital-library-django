from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:book_id>/', views.book_detail, name='book_detail'),
    path('upload', views.FileFieldView.as_view(), name='book_upload'),
]