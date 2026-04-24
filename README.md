# nyancat.nu

A Django-based web application featuring a classic Nyan Cat welcome page, a fully client-side media converter, an AI-powered background remover, and a persistent notepad editor.

## Features

- **Classic Welcome Page**: A playful landing page with an animated Nyan Cat banner.
- **In-Browser File Converter**: Convert media files (Video, Audio, Images) entirely in your browser using `ffmpeg.wasm`.
  - No files are uploaded to any server; all processing happens locally.
  - Supports MP4, MP3, WAV, GIF, PNG, JPG, WEBP, and more.
  - Custom extension support for advanced users.
- **AI Background Remover**: Professional-grade background removal powered by RMBG-1.4 AI model.
  - 100% client-side processing using Transformers.js
  - High-quality results for people, products, and objects
  - View original, mask, and result side-by-side
  - Automatic processing history stored locally in your browser
  - Export transparent PNG images
  - ~176MB model download (one-time, cached in browser)
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
- **AI Processing**: [Transformers.js](https://huggingface.co/docs/transformers.js) (@xenova/transformers)
- **AI Model**: [RMBG-1.4](https://huggingface.co/briaai/RMBG-1.4) by BRIA AI
- **Storage**: IndexedDB (for local history)

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
- Requires HTTPS and `SharedArrayBuffer` support

### 2. Background Remover (`/bg-remover/`)
- Remove backgrounds from images using AI
- Powered by RMBG-1.4 model from BRIA AI
- View the generated mask and final result
- Processing history stored locally in IndexedDB
- Download results as transparent PNG files
- Works best with images containing people, products, or clear subjects

### 3. Notepad (`/notepad/`)
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

### 3. Enable Site and Get SSL
```bash
sudo ln -s /etc/nginx/sites-available/nyancat.nu /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
sudo certbot --nginx -d nyancat.nu
```

## Privacy & Security

- **100% Client-Side Processing**: File converter, background remover, and notepad all process everything locally in your browser
- **No Server Uploads**: Your files and text never leave your device
- **Local Storage Only**: Processing history and notepad content are stored in your browser's localStorage/IndexedDB
- **Open Source**: All code is available for inspection

## Browser Requirements

### For File Converter:
- **HTTPS Required**: The converter requires secure context (HTTPS) to work on production
- **SharedArrayBuffer Support**: Modern browsers (Chrome 92+, Firefox 89+, Safari 15.2+)
- **COOP/COEP Headers**: Required for ffmpeg.wasm (configured in Nginx setup above)

### For Background Remover:
- **Modern Browser**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **IndexedDB Support**: For storing processing history
- **WebAssembly Support**: For running the AI model
- **~176MB Initial Download**: Model is cached for future use

## Troubleshooting

### File Converter Not Working
- Ensure you're using HTTPS (required for `SharedArrayBuffer`)
- Check that COOP/COEP headers are set correctly in Nginx
- Verify your browser supports WebAssembly and SharedArrayBuffer
- Try disabling browser extensions that might interfere

### Background Remover Issues
- Clear browser cache if model fails to load
- Ensure you have stable internet for initial model download
- Check browser console for detailed error messages
- Works best with clear, well-lit images

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT
