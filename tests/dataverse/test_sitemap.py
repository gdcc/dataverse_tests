import requests
import os
from ..conftest import read_json


dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(os.path.dirname(dir_path), "data")


class TestSitemap:
    def test_sitemap(self):
        INSTANCE = os.getenv("INSTANCE")
        data = read_json(os.path.join(data_path, f"instance/dataverse_{INSTANCE}.json"))
        base_url = data["instances"][INSTANCE]["base-url"]

        url = f"{base_url}/sitemap.xml"

        assert requests.get(url).status_code == 200
        assert "application/xml" in requests.head(url).headers["Content-Type"]
