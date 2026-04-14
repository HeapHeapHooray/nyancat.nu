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
   git clone https://github.com/HeapHeapHooray/nyancat.nu
   cd nyancat.nu
   ```

2. **Install Django**:
   ```bash
   pip install django
   ```

3. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

4. **Access the site**:
   Open [http://localhost:8000](http://localhost:8000) in your browser.

## Browser Security Requirements

The file converter utilizes `SharedArrayBuffer`, which requires the website to be served in a "cross-origin isolated" state. This project includes custom middleware (`core/middleware.py`) that sends the necessary headers:

- `Cross-Origin-Opener-Policy: same-origin`
- `Cross-Origin-Embedder-Policy: require-corp`

If you are deploying this to production, ensure your hosting environment or reverse proxy (like Nginx) respects or reproduces these headers.

## License

MIT
