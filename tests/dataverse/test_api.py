import os
from pyDataverse.api import NativeApi
import requests


class TestApi:
    def test_api_dataverses(self, test_data):
        if test_data["tests"]["api"]["dataverses"]["test"]:
            base_url = test_data["instance"]["base-url"]

            for dv in test_data["dataverses"]:
                url = f"{base_url}/api/dataverses/{dv}"
                resp = requests.get(url)

                assert resp.status_code == 200
                assert "application/json" in resp.headers["Content-Type"]
                assert (
                    resp.json()["data"]["name"] == test_data["dataverses"][dv]["name"]
                )
                assert (
                    resp.json()["data"]["alias"] == test_data["dataverses"][dv]["alias"]
                )
                assert (
                    resp.json()["data"]["affiliation"]
                    == test_data["dataverses"][dv]["affiliation"]
                )
                assert (
                    resp.json()["data"]["theme"]["tagline"]
                    == test_data["dataverses"][dv]["tagline"]
                )
                assert (
                    resp.json()["data"]["theme"]["linkUrl"]
                    == test_data["dataverses"][dv]["url"]
                )
                for contact in resp.json()["data"]["dataverseContacts"]:
                    assert (
                        contact["contactEmail"] in test_data["dataverses"][dv]["emails"]
                    )

    def test_dataverse_version(self, test_data):
        if test_data["tests"]["api"]["dataverse-version"]["test"]:
            base_url = test_data["instance"]["base-url"]

            api = NativeApi(base_url)
            resp = api.get_info_version()
            assert resp.json()["data"]["version"] == test_data["instance"]["version"]
