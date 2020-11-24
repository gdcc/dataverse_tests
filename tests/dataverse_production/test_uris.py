import os
import requests
from ..conftest import read_json


dir_path = os.path.dirname(os.path.realpath(__file__))


class TestUris:
    def test_uris(self, browsers):
        data = read_json(os.path.join(dir_path, "data.json"))

        for driver in browsers:
            for res in data["resources"]:
                resp = requests.get(res["url"], allow_redirects=True)
                assert resp.status_code == 200
                assert resp.encoding == "UTF-8"
                if "final-url" in res:
                    assert resp.url == res["final-url"]
                else:
                    assert resp.url == res["url"]
                if "title" in res:
                    driver.get(res["url"])
                    assert res["title"] == driver.title
