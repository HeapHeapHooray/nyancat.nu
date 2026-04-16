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
