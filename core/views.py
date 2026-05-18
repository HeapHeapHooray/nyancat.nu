import json
import os
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
import requests
import yt_dlp
from yt_dlp.networking.impersonate import ImpersonateTarget


def index(request):
    return render(request, "core/index.html")


def databases_collection(request):
    normal_path = os.path.join(settings.BASE_DIR, "tagged_databases", "tagged_databases.json")
    with open(normal_path, "r", encoding="utf-8") as f:
        normal_databases = json.load(f)
    
    normal_tags = set()
    for db in normal_databases:
        for tag in db.get("tags", []):
            normal_tags.add(tag)

    others_path = os.path.join(settings.BASE_DIR, "tagged_databases", "other_tagged_databases.json")
    with open(others_path, "r", encoding="utf-8") as f:
        other_databases = json.load(f)
    
    other_tags = set()
    for db in other_databases:
        for tag in db.get("tags", []):
            other_tags.add(tag)
            
    dorks_path = os.path.join(settings.BASE_DIR, "tagged_databases", "dorks.txt")
    dorks = []
    if os.path.exists(dorks_path):
        with open(dorks_path, "r", encoding="utf-8") as f:
            dorks = [line.strip() for line in f if line.strip()]
    
    context = {
        "normal_databases": normal_databases,
        "normal_tags": sorted(list(normal_tags)),
        "other_databases": other_databases,
        "other_tags": sorted(list(other_tags)),
        "dorks": dorks,
    }
    return render(request, "core/databases.html", context)


def converter(request):
    return render(request, "core/converter.html")


def video_compressor(request):
    return render(request, "core/video_compressor.html")


def bg_remover(request):
    return render(request, "core/bg_remover.html")


def notepad(request):
    return render(request, "core/notepad.html")


def minecraft_vault(request):
    return render(request, "core/minecraft_vault.html")


def minecraft_videos(request):
    json_path = os.path.join(settings.BASE_DIR, "minecraft_vault", "all_videos.json")
    videos = []
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            videos = json.load(f)
    
    return render(request, "core/minecraft_videos.html", {"videos_json": json.dumps(videos)})


def video_slicer(request):
    return render(request, "core/video_slicer.html")


def audio_to_video(request):
    return render(request, "core/audio_to_video.html")


def x_downloader(request):
    video_info = None
    error = None

    if request.method == "POST":
        url = request.POST.get("url", "").strip()
        if url:
            if not ("twitter.com" in url or "x.com" in url):
                error = "Only videos from X (Twitter) are supported."
            else:
                ydl_opts = {
                    "format": "best",
                    "noplaylist": True,
                    "quiet": True,
                    "js_runtimes": {"node": {}},
                    "remote_components": ["ejs:github"],
                    "impersonate": ImpersonateTarget(client="chrome"),
                }
                try:
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=False)

                        # Format duration properly
                        duration_seconds = info.get("duration")
                        if duration_seconds:
                            duration_seconds = int(duration_seconds)
                            hours = duration_seconds // 3600
                            minutes = (duration_seconds % 3600) // 60
                            seconds = duration_seconds % 60
                            if hours > 0:
                                duration_formatted = (
                                    f"{hours}:{minutes:02d}:{seconds:02d}"
                                )
                            else:
                                duration_formatted = f"{minutes}:{seconds:02d}"
                        else:
                            duration_formatted = info.get("duration_string", "Unknown")

                        video_info = {
                            "title": info.get("title"),
                            "thumbnail": info.get("thumbnail"),
                            "url": info.get("url"),
                            "duration": duration_formatted,
                            "uploader": info.get("uploader"),
                            "original_url": url,
                        }
                except Exception as e:
                    error = str(e) if str(e) else repr(e)

    return render(
        request, "core/x_downloader.html", {"video_info": video_info, "error": error}
    )


def instagram_downloader(request):
    video_info = None
    error = None

    if request.method == "POST":
        url = request.POST.get("url", "").strip()
        if url:
            if not ("instagram.com" in url):
                error = "Only videos from Instagram are supported."
            else:
                ydl_opts = {
                    "format": "best",
                    "noplaylist": True,
                    "quiet": True,
                    "js_runtimes": {"node": {}},
                    "remote_components": ["ejs:github"],
                    "impersonate": ImpersonateTarget(client="chrome"),
                }
                try:
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=False)

                        # Format duration properly
                        duration_seconds = info.get("duration")
                        if duration_seconds:
                            duration_seconds = int(duration_seconds)
                            hours = duration_seconds // 3600
                            minutes = (duration_seconds % 3600) // 60
                            seconds = duration_seconds % 60
                            if hours > 0:
                                duration_formatted = (
                                    f"{hours}:{minutes:02d}:{seconds:02d}"
                                )
                            else:
                                duration_formatted = f"{minutes}:{seconds:02d}"
                        else:
                            duration_formatted = info.get("duration_string", "Unknown")

                        # Get the best possible thumbnail
                        thumbnail = info.get("thumbnail")
                        if not thumbnail and info.get("thumbnails"):
                            thumbnail = info.get("thumbnails")[-1].get("url")

                        video_info = {
                            "title": info.get("title") or info.get("description") or "Instagram Video",
                            "thumbnail": thumbnail,
                            "url": info.get("url"),
                            "duration": duration_formatted,
                            "uploader": info.get("uploader"),
                            "original_url": url,
                        }
                except Exception as e:
                    error = str(e) if str(e) else repr(e)

    return render(
        request,
        "core/instagram_downloader.html",
        {"video_info": video_info, "error": error},
    )


def thumbnail_proxy(request):
    url = request.GET.get("url")
    if not url:
        return HttpResponse(status=400)

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        }
        response = requests.get(url, headers=headers, stream=True, timeout=10)
        response.raise_for_status()

        return StreamingHttpResponse(
            response.iter_content(chunk_size=8192),
            content_type=response.headers.get("Content-Type", "image/jpeg"),
        )
    except Exception as e:
        return HttpResponse(status=500)


def youtube_downloader(request):
    video_info = None
    error = None

    if request.method == "POST":
        url = request.POST.get("url", "").strip()
        if url:
            # Basic validation to ensure it's a YouTube URL
            if not ("youtube.com" in url or "youtu.be" in url):
                error = "Only videos from YouTube are supported."
            else:
                ydl_opts = {
                    "format": "best",
                    "noplaylist": True,
                    "quiet": True,
                    "cookiefile": "/var/remote_cookies.txt",
                    "extractor_args": {"youtubepot-wpc": {"nosandbox": []}},
                }
                try:
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=False)

                        # Format duration properly
                        duration_seconds = info.get("duration")
                        if duration_seconds:
                            duration_seconds = int(duration_seconds)
                            hours = duration_seconds // 3600
                            minutes = (duration_seconds % 3600) // 60
                            seconds = duration_seconds % 60
                            if hours > 0:
                                duration_formatted = (
                                    f"{hours}:{minutes:02d}:{seconds:02d}"
                                )
                            else:
                                duration_formatted = f"{minutes}:{seconds:02d}"
                        else:
                            duration_formatted = info.get("duration_string", "Unknown")

                        video_info = {
                            "title": info.get("title"),
                            "thumbnail": info.get("thumbnail"),
                            "url": info.get("url"),
                            "duration": duration_formatted,
                            "uploader": info.get("uploader"),
                            "original_url": url,
                        }
                except Exception as e:
                    error = str(e) if str(e) else repr(e)

    return render(
        request,
        "core/youtube_downloader.html",
        {"video_info": video_info, "error": error},
    )
