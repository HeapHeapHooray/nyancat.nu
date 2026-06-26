from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("databases/", views.databases_collection, name="databases_collection"),
    path("converter/", views.converter, name="converter"),
    path("video-compressor/", views.video_compressor, name="video_compressor"),
    path("video-slicer/", views.video_slicer, name="video_slicer"),
    path("audio-to-video/", views.audio_to_video, name="audio_to_video"),
    path("x-downloader/", views.x_downloader, name="x_downloader"),
    path("bg-remover/", views.bg_remover, name="bg_remover"),
    path("notepad/", views.notepad, name="notepad"),
    path("minecraft-vault/", views.minecraft_vault, name="minecraft_vault"),
    path("minecraft-vault/videos/", views.minecraft_videos, name="minecraft_videos"),
    path("nano_playroom/", views.nano_playroom, name="nano_playroom"),
    path("nano_playroom/<path:filepath>", views.nano_playroom_file, name="nano_playroom_file"),
    path("nuverse.sh", views.nuverse_sh, name="nuverse_sh"),
    path("nerd/", views.nerd_tools, name="nerd_tools"),
    path("nerd/map-lookup/", views.nerd_map_lookup, name="nerd_map_lookup"),
]

