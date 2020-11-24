import requests
import os


class TestSitemap:
    def test_sitemap(self):
        url = os.getenv("BASE_URL") + "/sitemap.xml"

        assert requests.get(url).status_code == 200
        assert "application/xml" in requests.head(url).headers["Content-Type"]
