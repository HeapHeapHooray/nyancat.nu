from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('converter/', views.converter, name='converter'),
    path('x-downloader/', views.x_downloader, name='x_downloader'),
    path('bg-remover/', views.bg_remover, name='bg_remover'),
]
