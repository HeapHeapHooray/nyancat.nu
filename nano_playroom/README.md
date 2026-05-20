# Nano Playroom

This directory is used by the AI "Nano" to dynamically generate and store web files (HTML, CSS, JS, etc.) in real time.

All files saved here are accessible in the browser via `/nano_playroom/<filename>`.
Nothing in this directory runs on the server; everything is served as static client-side content.

### Direct File Downloading
To force the browser to download a playroom file directly as an attachment instead of displaying it inline, append `?download=1` (or `?download=true`) to the URL.
* *Example*: `/nano_playroom/pong.html?download=1`

