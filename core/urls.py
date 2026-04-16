from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('converter/', views.converter, name='converter'),
    path('downloader/', views.video_downloader, name='video_downloader'),
]
