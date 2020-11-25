import os
import requests
from ..conftest import read_json


dir_path = os.path.dirname(os.path.realpath(__file__))


class TestMetadataServer:
    def test_metadata_server(self):
        data = read_json(os.path.join(dir_path, "data.json"))

        for res in data["metadata-server"]["resources"]:
            resp = requests.get(res["url"], allow_redirects=True)
            assert resp.status_code == 200
            assert resp.encoding == "UTF-8"
            assert "text/xml" in resp.headers["Content-Type"]
