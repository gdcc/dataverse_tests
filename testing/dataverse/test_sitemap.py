import pytest
import requests


class TestSitemap:
    def test_sitemap(self, test_config):
        if not test_config["tests"]["sitemap"]["test"]:
            pytest.skip("Test not configured to be executed.")

        base_url = test_config["instance"]["base-url"]
        url = f"{base_url}/sitemap.xml"

        assert requests.get(url).status_code == 200
        assert "application/xml" in requests.head(url).headers["Content-Type"]
