import pytest
import requests


class TestRobotsTxt:
    @pytest.mark.v4_18_1
    def test_robots_txt(self, test_config):
        """

        Input
        * base url

        Expected result
        * status code
        * content type
        * encoding

        """
        test_cfg = test_config["tests"]["robots.txt"]

        base_url = test_config["instance"]["base-url"]

        url = f"{base_url}/robots.txt"
        resp = requests.get(url)
        assert resp.status_code == 200
        assert resp.encoding == test_cfg["encoding"]
        assert "text/plain" in requests.head(url).headers["Content-Type"]
