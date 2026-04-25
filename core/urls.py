from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("converter/", views.converter, name="converter"),
    path("video-compressor/", views.video_compressor, name="video_compressor"),
    path("video-slicer/", views.video_slicer, name="video_slicer"),
    path("audio-to-video/", views.audio_to_video, name="audio_to_video"),
    path("x-downloader/", views.x_downloader, name="x_downloader"),
    path("bg-remover/", views.bg_remover, name="bg_remover"),
    path("notepad/", views.notepad, name="notepad"),
]
