# nyancat.nu

A Django-based web application featuring a classic Nyan Cat welcome page, a fully client-side media converter, video compressor, audio/video slicer, audio to video creator, an AI-powered background remover, and a persistent notepad editor.

## Features

- **Classic Welcome Page**: A playful landing page with an animated Nyan Cat banner.
- **In-Browser File Converter**: Convert media files (Video, Audio, Images) entirely in your browser using `ffmpeg.wasm`.
  - No files are uploaded to any server; all processing happens locally.
  - Supports MP4, MP3, WAV, GIF, PNG, JPG, WEBP, and more.
  - Custom extension support for advanced users.
  - Conversion history stored locally in your browser
- **Video Compressor/Resizer**: Compress and resize videos with customizable settings.
  - Adjust resolution, bitrate, frame rate, and codec
  - Multiple codec support (H.264, H.265, VP9)
  - Quick presets for common use cases
  - Before/after comparison and size savings display
  - All processing happens in your browser
- **Audio/Video Slicer**: Precisely slice audio and video files.
  - Manual time input or pick from current playback position
  - High-resolution timestamps (milliseconds precision)
  - Preview sliced results before downloading
  - Automatic re-encoding for accurate cuts
  - Processing history with time ranges
  - Mobile-friendly interface
- **Audio to Video**: Create videos from static images and audio files.
  - Upload an image and audio file to create an MP4 video
  - Image displays for the duration of the audio
  - Automatic dimension adjustment for compatibility
  - Preview both inputs and final result
  - Processing history with video previews
  - Perfect for creating audio visualizers or lyric videos with album art
  - Mobile-friendly responsive design
- **AI Background Remover**: Professional-grade background removal with multiple AI models.
  - Two model options: InSPyReNet (~395MB) for high accuracy, RMBG-1.4 (~42MB) for speed
  - 100% client-side processing using ONNX Runtime Web
  - High-quality results for people, products, and objects
  - View original, mask, and result side-by-side
  - Automatic processing history stored locally in your browser
  - Export transparent PNG images
  - Models cached in browser for instant reuse
- **Notepad Editor**: Full-featured text editor with persistence.
  - Create, edit, and save text files
  - Upload and download text files
  - Auto-save to browser localStorage
  - Line numbers with synchronized scrolling
  - Character and line count
  - Persistent across browser sessions
  - Keyboard shortcuts (Ctrl/Cmd+S to save, Ctrl/Cmd+N for new file)

## Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Media Processing**: [ffmpeg.wasm](https://github.com/ffmpegwasm/ffmpeg.wasm) (FFmpeg ported to WebAssembly)
- **AI Processing**: [ONNX Runtime Web](https://onnxruntime.ai/docs/tutorials/web/) for browser-based inference
- **AI Models**: 
  - [InSPyReNet-SwinB-Plus-Ultra](https://huggingface.co/OS-Software/InSPyReNet-SwinB-Plus-Ultra-ONNX) (~395MB) - High accuracy
  - [RMBG-1.4](https://huggingface.co/briaai/RMBG-1.4) by BRIA AI (~42MB, quantized) - Fast and efficient
- **Storage**: IndexedDB (for local history and model caching)

## Prerequisites

- Python 3.10+
- A modern web browser that supports `SharedArrayBuffer` (required for ffmpeg.wasm).

## Setup & Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/nyancat.nu.git
   cd nyancat.nu
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare static files**:
   ```bash
   python manage.py collectstatic --noinput
   ```

4. **Run the development server (Local)**:
   ```bash
   python manage.py runserver
   ```

5. **Run for Production (Gunicorn)**:
   To host on all interfaces (`0.0.0.0`):
   ```bash
   gunicorn nyancat_site.wsgi:application --bind 0.0.0.0:8000
   ```

6. **Access the site**:
   Open [http://localhost:8000](http://localhost:8000) (or your server's IP) in your browser.

## Available Tools

### 1. File Converter (`/converter/`)
- Convert between various media formats
- Supports video (MP4, AVI, MOV), audio (MP3, WAV, AAC), and images (PNG, JPG, GIF, WEBP)
- All processing happens in your browser using WebAssembly
- Conversion history with preview and re-download capability
- Requires HTTPS and `SharedArrayBuffer` support

### 2. Video Compressor/Resizer (`/video-compressor/`)
- Compress and resize video files with advanced options
- Customizable resolution (4K, 1440p, 1080p, 720p, 480p, 360p, or custom)
- Adjustable bitrate (500k to 8000k)
- Frame rate control (15, 24, 30, 60 fps)
- Multiple codec options (H.264, H.265/HEVC, VP9)
- Audio settings (copy, re-encode, or remove)
- Quick presets: High Quality, Medium, Low, Social Media
- Before/after preview with size comparison
- All processing happens client-side

### 3. Audio/Video Slicer (`/video-slicer/`)
- Slice audio and video files with precision
- Manual time input (HH:MM:SS.mmm format) or set from current playback
- High-resolution timestamps with millisecond precision
- Visual media preview with standard playback controls
- Automatic time range validation and clamping
- Re-encodes for accurate cuts (H.264 for video, AAC for audio)
- Preview sliced results before downloading
- Processing history with time ranges and previews
- Fully responsive mobile-friendly design
- Stores last 50 slices locally in browser

### 4. Audio to Video (`/audio-to-video/`)
- Create MP4 videos from static images and audio files
- Upload any image format (PNG, JPG, GIF, etc.) and audio format (MP3, WAV, AAC, etc.)
- Video duration matches the audio length automatically
- Optimized encoding for still images with H.264 video codec
- Automatic dimension adjustment for maximum compatibility
- Preview both inputs (image and audio) before processing
- Preview final video before downloading
- Processing history with video previews stored in IndexedDB
- Stores last 50 creations locally in browser
- Perfect for creating audio visualizers, lyric videos, or podcasts with cover art
- Mobile-friendly responsive interface

### 5. Background Remover (`/bg-remover/`)
- Remove backgrounds from images using AI with selectable models
- Two model options:
  - **InSPyReNet-SwinB-Plus-Ultra** (~395MB): Highest accuracy for complex scenes
  - **RMBG-1.4** (~42MB, quantized): Fast processing, smaller download
- 100% client-side processing with ONNX Runtime Web
- View original image, generated mask, and final result side-by-side
- Processing history stored locally in IndexedDB
- Download results as transparent PNG files
- Models cached in browser after first download
- Works best with images containing people, products, or clear subjects

### 6. Notepad (`/notepad/`)
- Browser-based text editor with line numbers
- Auto-save functionality with localStorage persistence
- Create new files, upload existing files, and download edited files
- Custom filename support
- Real-time character and line count
- Keyboard shortcuts for common actions
- Supports multiple text file formats (.txt, .md, .json, .js, .css, .html, .xml, .csv, .log)
- Content persists across browser sessions

## VPS Deployment (Nginx + Gunicorn + SSL)

To run the converter on mobile and modern browsers, **HTTPS is mandatory**.

### 1. Install Nginx and Certbot
```bash
sudo apt update
sudo apt install nginx certbot python3-certbot-nginx
```

### 2. Configure Nginx
Create a configuration file at `/etc/nginx/sites-available/nyancat.nu`:

```nginx
server {
    listen 80;
    server_name nyancat.nu;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name nyancat.nu;

    # SSL configuration (Certbot will fill this)
    # ssl_certificate /etc/letsencrypt/live/nyancat.nu/fullchain.pem;
    # ssl_certificate_key /etc/letsencrypt/live/nyancat.nu/privkey.pem;

    # CRITICAL: Headers for ffmpeg.wasm
    add_header Cross-Origin-Opener-Policy "same-origin" always;
    add_header Cross-Origin-Embedder-Policy "require-corp" always;

    location / {
        proxy_pass http://127.0.0.1:8000;
        
        # Prevent duplicate headers if Django also sends them
        proxy_hide_header Cross-Origin-Opener-Policy;
        proxy_hide_header Cross-Origin-Embedder-Policy;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/your/nyancat.nu/staticfiles/;
    }
}
```

### 3. Fix Static Files Permissions
Nginx needs read access to your static files. Run these commands:
```bash
cd /path/to/your/nyancat.nu

# Allow Nginx to traverse your project directories
sudo chmod o+x /path/to/your
sudo chmod o+x /path/to/your/nyancat.nu

# Fix staticfiles permissions (assuming Nginx runs as www-data)
sudo chown -R $USER:www-data staticfiles/
sudo chmod -R 755 staticfiles/
sudo find staticfiles/ -type f -exec chmod 644 {} \;
```

### 4. Enable Site and Get SSL
```bash
sudo ln -s /etc/nginx/sites-available/nyancat.nu /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
sudo certbot --nginx -d nyancat.nu
```

## Privacy & Security

- **100% Client-Side Processing**: File converter, video compressor, audio/video slicer, audio to video, background remover, and notepad all process everything locally in your browser
- **No Server Uploads**: Your files and text never leave your device
- **Local Storage Only**: Processing history and notepad content are stored in your browser's localStorage/IndexedDB
- **Open Source**: All code is available for inspection

## Browser Requirements

### For Media Tools (Converter, Compressor, Slicer, Audio to Video):
- **HTTPS Required**: Media tools require secure context (HTTPS) to work on production
- **SharedArrayBuffer Support**: Modern browsers (Chrome 92+, Firefox 89+, Safari 15.2+)
- **COOP/COEP Headers**: Required for ffmpeg.wasm (configured in Nginx setup above)
- **IndexedDB Support**: For storing processing history

### For Background Remover:
- **Modern Browser**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **IndexedDB Support**: For storing processing history and model caching
- **WebAssembly Support**: For running ONNX models
- **Initial Model Download**: 
  - InSPyReNet: ~395MB (high accuracy)
  - RMBG-1.4: ~42MB (fast, quantized)
- **Models Cached**: After first download, models load instantly from browser cache

## Troubleshooting

### Media Tools Not Working (Converter, Compressor, Slicer, Audio to Video)
- Ensure you're using HTTPS (required for `SharedArrayBuffer`)
- Check that COOP/COEP headers are set correctly in Nginx
- Verify your browser supports WebAssembly and SharedArrayBuffer
- Try disabling browser extensions that might interfere
- For slicer: Ensure time values are in valid format (HH:MM:SS.mmm, MM:SS.mmm, or seconds)
- For audio to video: Ensure image dimensions are reasonable (very large images may take longer to process)

### Background Remover Issues
- Try RMBG-1.4 model first (smaller, faster download at ~42MB)
- Clear browser cache if model fails to load
- Ensure you have stable internet for initial model download
- Check browser console for detailed error messages
- Works best with clear, well-lit images
- If InSPyReNet (~395MB) is too slow, switch to RMBG-1.4 for faster processing

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT
