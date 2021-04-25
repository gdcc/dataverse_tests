import pytest
import requests


class TestSitemap:
    @pytest.mark.v4_18_1
    def test_sitemap(self, test_config):
        """

        Input
        * base url

        Expected result
        * content type
        * status code
        * url

        """
        base_url = test_config["instance"]["base-url"]
        url = f"{base_url}/sitemap.xml"

        assert requests.get(url).status_code == 200
        assert "application/xml" in requests.head(url).headers["Content-Type"]
