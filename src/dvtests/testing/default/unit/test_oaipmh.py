import pytest
import requests


class TestMetadataServer:
    @pytest.mark.v4_18_1
    def test_endpoints(self, test_config):
        """

        Input
        * url

        Expected result
        * status code
        * encoding
        * content type

        """
        for ep in test_config["metadata-server"]["endpoints"]:
            resp = requests.get(ep["url"], allow_redirects=True)
            assert resp.status_code == 200
            assert resp.encoding == "UTF-8"
            assert "text/xml" in resp.headers["Content-Type"]
