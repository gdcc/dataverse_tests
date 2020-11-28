import os
import requests
from ..conftest import read_json


dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(os.path.dirname(dir_path), "data")


class TestRobotsTxt:
    def test_robots_txt(self):
        INSTANCE = os.getenv("INSTANCE")
        data = read_json(
            os.path.join(data_path, f"instances/{INSTANCE}/test-data.json")
        )
        base_url = data["instance"]["base-url"]

        url = f"{base_url}/robots.txt"
        resp = requests.get(url)
        assert resp.status_code == 200
        assert resp.encoding == data["instance"]["robots.txt"]["encoding"]
        assert "text/plain" in requests.head(url).headers["Content-Type"]
