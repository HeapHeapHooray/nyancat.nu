from django.test import TestCase, Client
from django.urls import reverse

class XDownloaderTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('x_downloader')

    def test_x_downloader_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/x_downloader.html')

    def test_x_downloader_x_url_rejected(self):
        # We don't want to actually call yt-dlp in tests if possible, 
        # but we can test the URL validation logic.
        response = self.client.post(self.url, {'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Only videos from X (Twitter) are supported.")

    def test_x_downloader_x_url_accepted(self):
        # This will likely fail or take long if it tries to hit the network, 
        # but the error message should NOT be the one about unsupported site.
        # In a real scenario, we'd mock yt_dlp.
        response = self.client.post(self.url, {'url': 'https://twitter.com/Twitter/status/123456789'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Only videos from X (Twitter) are supported.")


class MinecraftVaultTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("minecraft_vault")

    def test_minecraft_vault_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/minecraft_vault.html")
        self.assertContains(response, "Replay Mod Recordings")
        self.assertContains(response, "https://drive.google.com/drive/folders/10Rh0U5xQaCo37nnUBQCI8tdaD-qe9DJL?usp=sharing")


class NanoPlayroomTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("nano_playroom")

    def test_nano_playroom_dashboard_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/nano_playroom_dashboard.html")

    def test_nano_playroom_json_api(self):
        response = self.client.get(self.url, {"format": "json"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("files", data)
        # Check that our mock pong game is listed
        filenames = [f["name"] for f in data["files"]]
        self.assertIn("pong.html", filenames)
        self.assertIn("styles.css", filenames)
        self.assertIn("app.js", filenames)

    def test_serve_playroom_html_file(self):
        url = reverse("nano_playroom_file", args=["pong.html"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "text/html")
        self.assertContains(response, "Retro Pong Sandbox")
        # Check no-cache headers are set
        self.assertEqual(response.headers["Cache-Control"], "no-cache, no-store, must-revalidate")

    def test_serve_playroom_css_file(self):
        url = reverse("nano_playroom_file", args=["assets/styles.css"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "text/css")

    def test_serve_playroom_js_file(self):
        url = reverse("nano_playroom_file", args=["assets/app.js"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(response.headers["Content-Type"], ["application/javascript", "text/javascript"])

    def test_path_traversal_blocked(self):
        url = reverse("nano_playroom_file", args=["../manage.py"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.assertContains(response, "Access Denied", status_code=403)

    def test_non_existent_file_404(self):
        url = reverse("nano_playroom_file", args=["ghost_app.html"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_download_playroom_file(self):
        url = reverse("nano_playroom_file", args=["pong.html"])
        # Query parameter download=1
        response = self.client.get(url, {"download": "1"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Content-Disposition", response.headers)
        self.assertIn('attachment; filename="pong.html"', response.headers["Content-Disposition"])


class NuverseScriptTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("nuverse_sh")

    def test_nuverse_sh_redirect(self):
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            "https://raw.githubusercontent.com/HeapHeapHooray/nuverse/refs/heads/main/download_archives.sh",
            fetch_redirect_response=False,
        )


class NerdToolsTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_nerd_tools_dashboard_get(self):
        response = self.client.get(reverse("nerd_tools"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/nerd_tools.html")
        self.assertContains(response, "nerd.nu Tools")

    def test_nerd_map_lookup_get(self):
        response = self.client.get(reverse("nerd_map_lookup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/nerd_map_lookup.html")
        self.assertContains(response, "Nerd.nu Map Lookup")


class ImageResizerTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("image_resizer")

    def test_image_resizer_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/image_resizer.html")
        self.assertContains(response, "Image Compressor & Resizer")









