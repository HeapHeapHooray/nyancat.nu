from django.shortcuts import render
import yt_dlp
from yt_dlp.networking.impersonate import ImpersonateTarget


def index(request):
    return render(request, "core/index.html")


def converter(request):
    return render(request, "core/converter.html")


def video_compressor(request):
    return render(request, "core/video_compressor.html")


def bg_remover(request):
    return render(request, "core/bg_remover.html")


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
                        }
                except Exception as e:
                    error = str(e) if str(e) else repr(e)

    return render(
        request, "core/x_downloader.html", {"video_info": video_info, "error": error}
    )
