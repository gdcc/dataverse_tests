import os
import requests
from ..conftest import read_json


dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(os.path.dirname(dir_path), "data")


class TestResources:
    def test_urls(self, browsers):
        test_data = read_json(
            os.path.join(data_path, "instances/website/test-data.json")
        )

        for name, driver in browsers.items():
            for res in test_data["resources"]:
                resp = requests.get(res["url"], allow_redirects=True)
                assert resp.status_code == 200
                assert resp.encoding == "utf-8"
                if "final-url" in res:
                    assert resp.url == res["final-url"]
                else:
                    assert resp.url == res["url"]
                if "title" in res:
                    driver.get(res["url"])
                    assert res["title"] == driver.title
