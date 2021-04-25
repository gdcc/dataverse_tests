import pytest
import requests


class TestResources:
    @pytest.mark.v4_18_1
    @pytest.mark.selenium
    def test_urls(self, test_config, selenium):
        """

        TODO
        * no selenium necessary

        Input
        * url

        Expected result
        * url
        * title

        """
        for res in test_config["resources"]:
            resp = requests.get(res["url_start"], allow_redirects=True)
            assert resp.status_code == 200
            assert resp.encoding == "UTF-8"
            if "url_end" in res:
                assert resp.url == res["url_end"]
            else:
                assert resp.url == res["url_start"]
            if "title" in res:
                selenium.get(res["url"])
                assert res["title"] == selenium.title
