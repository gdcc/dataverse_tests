import os
import requests
from ..conftest import read_json


dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(os.path.dirname(dir_path), "data")


class TestMetadataServer:
    def test_metadata_server(self):
        INSTANCE = os.getenv("INSTANCE")
        data = read_json(
            os.path.join(data_path, f"instances/{INSTANCE}/test-data.json")
        )

        if "metadata-server" in data:
            if "resources" in data["metadata-server"]:
                for res in data["metadata-server"]["resources"]:
                    resp = requests.get(res["url"], allow_redirects=True)
                    assert resp.status_code == 200
                    assert resp.encoding == "UTF-8"
                    assert "text/xml" in resp.headers["Content-Type"]
