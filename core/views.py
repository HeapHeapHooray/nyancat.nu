import json
import os
import mimetypes
import time
from pathlib import Path
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseForbidden, JsonResponse, FileResponse
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


def image_resizer(request):
    return render(request, "core/image_resizer.html")


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


def nano_playroom(request):
    playroom_dir = Path(settings.BASE_DIR) / "nano_playroom"
    
    # Ensure folder exists
    if not playroom_dir.exists():
        playroom_dir.mkdir(parents=True, exist_ok=True)
        
    # Check if format=json is requested (for dynamic polling!)
    if request.GET.get("format") == "json":
        files_list = []
        # Walk directories recursively to list files
        for file_path in sorted(playroom_dir.glob("**/*")):
            # Only list actual files, and skip readme/hidden files
            if file_path.is_file() and file_path.name != "README.md" and not file_path.name.startswith("."):
                relative_path = file_path.relative_to(playroom_dir)
                try:
                    stat = file_path.stat()
                    elapsed = time.time() - stat.st_mtime
                    if elapsed < 60:
                        modified_ago = "Just now"
                    elif elapsed < 3600:
                        modified_ago = f"{int(elapsed // 60)}m ago"
                    elif elapsed < 86400:
                        modified_ago = f"{int(elapsed // 3600)}h ago"
                    else:
                        modified_ago = f"{int(elapsed // 86400)}d ago"
                    
                    files_list.append({
                        "name": file_path.name,
                        "filepath": str(relative_path),
                        "size": stat.st_size,
                        "modified_ago": modified_ago,
                    })
                except Exception:
                    pass
        return JsonResponse({"files": files_list})
        
    # Standard request: check if index.html exists in playroom_dir
    index_file = playroom_dir / "index.html"
    if index_file.exists() and index_file.is_file():
        # Serve it!
        return nano_playroom_file(request, "index.html")
        
    # Serve dashboard
    return render(request, "core/nano_playroom_dashboard.html")


def nano_playroom_file(request, filepath):
    playroom_dir = (Path(settings.BASE_DIR) / "nano_playroom").resolve()
    
    # Resolve the target file path
    target_path = (playroom_dir / filepath).resolve()
    
    # Security: check for path traversal (ensure target is strictly inside playroom_dir)
    if not (target_path == playroom_dir or playroom_dir in target_path.parents):
        return HttpResponseForbidden("Access Denied: Path traversal detected.")
        
    if not target_path.exists() or not target_path.is_file():
        raise Http404("File not found in Playroom.")
        
    # Guess mime type
    content_type, encoding = mimetypes.guess_type(str(target_path))
    if not content_type:
        content_type = "application/octet-stream"
        
    # Check if download is requested via GET parameter
    as_attachment = request.GET.get("download") in ["1", "true"]
        
    # Read and return raw file response
    response = FileResponse(
        open(target_path, "rb"),
        content_type=content_type,
        as_attachment=as_attachment,
        filename=target_path.name
    )
    
    # Prevent caching of dynamic assets so they update instantly in real-time
    response["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"
    
    return response


def nuverse_sh(request):
    return redirect("https://raw.githubusercontent.com/HeapHeapHooray/nuverse/refs/heads/main/download_archives.sh")


def nerd_tools(request):
    return render(request, "core/nerd_tools.html")


def nerd_map_lookup(request):
    return render(request, "core/nerd_map_lookup.html")


def qr_barcode(request):
    return render(request, "core/qr_barcode.html")





