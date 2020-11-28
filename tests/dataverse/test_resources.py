import os
import requests
from ..conftest import read_json


dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(os.path.dirname(dir_path), "data")


class TestResources:
    def test_urls(self, browsers):
        INSTANCE = os.getenv("INSTANCE")
        data = read_json(
            os.path.join(data_path, f"instances/{INSTANCE}/test-data.json")
        )

        if "resources" in data:
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
