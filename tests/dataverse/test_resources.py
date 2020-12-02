import os
import requests


class TestResources:
    def test_urls(self, test_config, browser):
        if test_config["tests"]["homepage"]["header-about"]["test"]:
            for name, driver in browser.items():
                for res in test_config["resources"]:
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
