import requests
import os


class TestSitemap:
    def test_sitemap(self, test_data):
        if test_data["tests"]["sitemap"]["test"]:
            base_url = test_data["instance"]["base-url"]
            url = f"{base_url}/sitemap.xml"

            assert requests.get(url).status_code == 200
            assert "application/xml" in requests.head(url).headers["Content-Type"]
