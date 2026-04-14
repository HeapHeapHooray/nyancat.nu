# nyancat.nu

A Django-based web application featuring a classic Nyan Cat welcome page and a fully client-side media converter.

## Features

- **Classic Welcome Page**: A playful landing page with an animated Nyan Cat banner.
- **In-Browser File Converter**: Convert media files (Video, Audio, Images) entirely in your browser using `ffmpeg.wasm`.
  - No files are uploaded to any server; all processing happens locally.
  - Supports MP4, MP3, WAV, GIF, PNG, JPG, WEBP, and more.
  - Custom extension support for advanced users.

## Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Processing**: [ffmpeg.wasm](https://github.com/ffmpegwasm/ffmpeg.wasm) (FFmpeg ported to WebAssembly)

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
    add_header Cross-Origin-Opener-Policy "same-origin";
    add_header Cross-Origin-Embedder-Policy "require-corp";

    location / {
        proxy_pass http://127.0.0.1:8000;
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

## Browser Security Requirements
... Applied fuzzy match at line 41-52.

## License

MIT
