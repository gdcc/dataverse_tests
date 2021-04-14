import pytest
import requests


class TestRobotsTxt:
    def test_robots_txt(self, test_config):
        if not test_config["tests"]["robots.txt"]["test"]:
            pytest.skip("Test not configured to be executed.")

        base_url = test_config["instance"]["base-url"]

        url = f"{base_url}/robots.txt"
        resp = requests.get(url)
        assert resp.status_code == 200
        assert resp.encoding == test_config["tests"]["robots.txt"]["encoding"]
        assert "text/plain" in requests.head(url).headers["Content-Type"]
