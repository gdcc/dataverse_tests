import os
import requests
from ..conftest import read_json


dir_path = os.path.dirname(os.path.realpath(__file__))


class TestRobotsTxt:
    def test_robots_txt(self):
        url = f"{os.getenv('BASE_URL')}/robots.txt"
        resp = requests.get(url)
        assert resp.status_code == 200
        assert resp.encoding == "UTF-8"
        assert "text/plain" in requests.head(url).headers["Content-Type"]
