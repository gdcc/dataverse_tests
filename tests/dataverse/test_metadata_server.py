import os
import requests


class TestMetadataServer:
    def test_metadata_server(self, test_data):
        if test_data["tests"]["metadata-server"]["test"]:
            for res in test_data["metadata-server"]["resources"]:
                resp = requests.get(res["url"], allow_redirects=True)
                assert resp.status_code == 200
                assert resp.encoding == "UTF-8"
                assert "text/xml" in resp.headers["Content-Type"]
