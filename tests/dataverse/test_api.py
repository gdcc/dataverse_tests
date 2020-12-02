import os
import pytest
import requests
from pyDataverse.api import NativeApi


class TestApi:
    def test_api_dataverses(self, test_config):
        if not test_config["tests"]["api"]["dataverses"]["test"]:
            pytest.skip("Test not configured to be executed.")

        base_url = test_config["instance"]["base-url"]

        for dv in test_config["dataverses"]:
            url = f"{base_url}/api/dataverses/{dv}"
            resp = requests.get(url)

            assert resp.status_code == 200
            assert "application/json" in resp.headers["Content-Type"]
            assert resp.json()["data"]["name"] == test_config["dataverses"][dv]["name"]
            assert (
                resp.json()["data"]["alias"] == test_config["dataverses"][dv]["alias"]
            )
            assert (
                resp.json()["data"]["affiliation"]
                == test_config["dataverses"][dv]["affiliation"]
            )
            assert (
                resp.json()["data"]["theme"]["tagline"]
                == test_config["dataverses"][dv]["tagline"]
            )
            assert (
                resp.json()["data"]["theme"]["linkUrl"]
                == test_config["dataverses"][dv]["url"]
            )
            for contact in resp.json()["data"]["dataverseContacts"]:
                assert (
                    contact["contactEmail"] in test_config["dataverses"][dv]["emails"]
                )

    def test_dataverse_version(self, test_config):
        if not test_config["tests"]["api"]["dataverse-version"]["test"]:
            pytest.skip("Test not configured to be executed.")

        base_url = test_config["instance"]["base-url"]

        api = NativeApi(base_url)
        resp = api.get_info_version()
        assert resp.json()["data"]["version"] == test_config["instance"]["version"]
