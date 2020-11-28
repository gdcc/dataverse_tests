import os
from pyDataverse.api import NativeApi
import requests
from ..conftest import read_json


dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(os.path.dirname(dir_path), "data")


class TestApi:
    def test_api(self):
        INSTANCE = os.getenv("INSTANCE")
        data = read_json(
            os.path.join(data_path, f"instances/{INSTANCE}/test-data.json")
        )
        base_url = data["instance"]["base-url"]

        if "dataverses" in data:
            for dv in data["dataverses"]:

                url = f"{base_url}/api/dataverses/{dv}"
                resp = requests.get(url)

                assert resp.status_code == 200
                assert "application/json" in resp.headers["Content-Type"]
                assert resp.json()["data"]["name"] == data["dataverses"][dv]["name"]
                assert resp.json()["data"]["alias"] == data["dataverses"][dv]["alias"]
                assert (
                    resp.json()["data"]["affiliation"]
                    == data["dataverses"][dv]["affiliation"]
                )
                assert (
                    resp.json()["data"]["dataverseContacts"][0]["contactEmail"]
                    == data["dataverses"][dv]["email"]
                )
                assert (
                    resp.json()["data"]["theme"]["tagline"]
                    == data["dataverses"][dv]["tagline"]
                )
                assert (
                    resp.json()["data"]["theme"]["linkUrl"]
                    == data["dataverses"][dv]["url"]
                )

    def test_dataverse_version(self):
        API_TOKEN = os.getenv("API_TOKEN")
        INSTANCE = os.getenv("INSTANCE")
        data = read_json(
            os.path.join(data_path, f"instances/{INSTANCE}/test-data.json")
        )
        base_url = data["instance"]["base-url"]

        api = NativeApi(base_url, API_TOKEN)
        resp = api.get_info_version()
        assert resp.json()["data"]["version"] == data["instance"]["version"]
