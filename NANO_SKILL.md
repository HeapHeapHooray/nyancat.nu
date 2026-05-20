# Nano Playroom Skill

Welcome, Nano! This document outlines how you can leverage the **Nano Playroom** environment to dynamically generate, serve, and iterate on client-side web applications and games in real time.

---

## 🚀 Playroom Overview

The playroom is a dedicated static-sandboxed environment integrated into the Django web server of `nyancat.nu`. It allows you to build front-end web tools, utilities, retro games, and experimental UI layouts.

- **Dynamic Real-Time Access**: Any file you write to the playroom directory is immediately available to external browsers.
- **Cache-Bypassing**: The server enforces cache-control headers on playroom paths, meaning any updates you make will be served instantly to visitors without browser caching delays.
- **Pure Client-Side Sandbox**: No backend code (Python, Django templates, PHP) executes on the server. Everything is loaded and executed entirely in the client's browser.

---

## 📂 Filesystem Coordinates

The playroom folder is located at the root of the repository:
```
nano_playroom/
```

### Supported Directory Layouts

1. **Dashboard Listing Mode (Default)**:
   - Save your individual applications at the root of `nano_playroom/` (e.g. `nano_playroom/my_cool_game.html`).
   - The platform will automatically detect and list them on the premium dashboard page at `/nano_playroom/` with their file size, type, and live creation timestamps.
   - Visitors can launch your app directly from the dashboard card grid.

2. **Custom Portal Mode**:
   - If you create an `index.html` at the root of `nano_playroom/` (i.e. `nano_playroom/index.html`), it will **completely take over** the dashboard view.
   - The route `/nano_playroom/` will load your custom index page instead of the default grid list. This is useful if you want to build a custom portal, launcher, or unified single-page application.

3. **Assets & Subfolders**:
   - Organize your stylesheets, JS scripts, images, and audio files inside subfolders (e.g. `nano_playroom/assets/`, `nano_playroom/js/`, `nano_playroom/css/`).
   - All relative links between your HTML, CSS, and JS files will be correctly mapped and served by the routing engine.

---

## 🛠️ How to Create & Update Playroom Files

As an AI system operating on the repository, you can create files by simply writing them to disk.

### Example: Creating a new game
To create a retro-arcade game named `brick_breaker.html`, write it directly to the playroom path relative to the project root:
```
nano_playroom/brick_breaker.html
```

Your game will immediately become visible to users in real time:
- Dashboard: `http://<server-domain-or-ip>/nano_playroom/`
- Direct Link: `http://<server-domain-or-ip>/nano_playroom/brick_breaker.html`

---

## ⚠️ Sandbox Restrictions & Best Practices

To ensure stability, security, and performance, follow these key instructions:

### 1. Pure Front-End Content Only
- All code must run client-side.
- Supported file types: `.html`, `.css`, `.js`, `.json`, `.png`, `.jpg`, `.jpeg`, `.gif`, `.svg`, `.webp`, `.mp3`, `.wav`.
- Do **not** try to run server-side python scripts, node scripts, or database queries inside playroom files.

### 2. Relative Asset Referencing
- Always use relative paths when linking your files.
- **Correct**: `<link rel="stylesheet" href="assets/styles.css">` or `<script src="./js/app.js"></script>`
- **Incorrect**: `<link rel="stylesheet" href="/static/core/css/styles.css">` (which references standard app static files) or referencing files outside of `nano_playroom/`.

### 3. Absolute Security Pathing
- The file server includes robust path-traversal blocking.
- Avoid using `../` segments that reference locations outside the `nano_playroom/` root directory (e.g. `href="../manage.py"`). The web server will block these with a `403 Forbidden` error.

### 4. Rich Aesthetics & Modern Design
- When building playroom apps, align with `nyancat.nu`'s retro-cyberpunk and retro-arcade styling.
- Use vibrant color palettes, clean fonts, custom Canvas animations, smooth animations, and premium glassmorphism layouts to deliver an outstanding user experience.
