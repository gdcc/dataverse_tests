import pytest
import requests
from pyDataverse.api import NativeApi


class TestApi:
    @pytest.mark.v4_18_1
    def test_api_dataverses(self, test_config):
        """

        Input
        * base url
        * dataverse aliases

        Expected result
        * dataverse
            * status code
            * url
            * content type
            * alias
            * affiliation
            * tagline
            * link url
            * contact email

        """
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

    @pytest.mark.v4_18_1
    def test_dataverse_version(self, test_config):
        """

        Input
        * base url

        Expected result
        * version
        * build

        """
        base_url = test_config["instance"]["base-url"]

        api = NativeApi(base_url)
        resp = api.get_info_version()
        assert resp.json()["data"]["version"] == test_config["instance"]["version"]

    @pytest.mark.v4_18_1
    def test_dataverse_server(self, test_config):
        """

        Input
        * base url

        Expected result
        * base url

        """
        base_url = test_config["instance"]["base-url"]

        api = NativeApi(base_url)
        resp = api.get_info_server()
        assert resp.json()["data"]["message"] == test_config["instance"]["base-url"]

    def test_user(self, test_config, config):
        """

        Input
        * base url

        Expected result
        * base url

        """
        """Test user endpoint.

        Does not work below Dataverse 5.3 or 5.2
        """
        base_url = test_config["instance"]["base-url"]
        api_token = config.API_TOKEN

        api = NativeApi(base_url, api_token)
        resp = api.get_user()
        assert resp.json()["data"]["message"] == test_config["instance"]["base-url"]
