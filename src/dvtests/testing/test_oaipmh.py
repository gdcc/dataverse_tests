import pytest
import requests


class TestMetadataServer:
    def test_metadata_server(self, test_config):
        if not test_config["tests"]["metadata-server"]["test"]:
            pytest.skip("Test not configured to be executed.")

        for res in test_config["metadata-server"]["resources"]:
            resp = requests.get(res["url"], allow_redirects=True)
            assert resp.status_code == 200
            assert resp.encoding == "UTF-8"
            assert "text/xml" in resp.headers["Content-Type"]
