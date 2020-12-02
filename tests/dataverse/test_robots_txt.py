import os
import requests


class TestRobotsTxt:
    def test_robots_txt(self, test_config):
        if test_config["tests"]["robots.txt"]["test"]:
            base_url = test_config["instance"]["base-url"]

            url = f"{base_url}/robots.txt"
            resp = requests.get(url)
            assert resp.status_code == 200
            assert resp.encoding == test_config["tests"]["robots.txt"]["encoding"]
            assert "text/plain" in requests.head(url).headers["Content-Type"]
