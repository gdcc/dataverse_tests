import os
import requests
from ..conftest import read_json


dir_path = os.path.dirname(os.path.realpath(__file__))


class TestUris:
    def test_uris(self, browser):
        data = read_json(os.path.join(dir_path, "data.json"))

        for r in data["resources"]:
            resp = requests.get(r["uri"])
            assert resp.status_code == 200
            assert resp.url == r["uri"]
            assert resp.encoding == "utf-8"
            if "title" in r:
                browser.get(r["uri"])
                assert r["title"] == browser.title
