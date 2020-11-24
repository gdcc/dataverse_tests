import requests
import os
from ..conftest import read_json


dir_path = os.path.dirname(os.path.realpath(__file__))


class TestApi:
    def test_api(self):
        data = read_json(os.path.join(dir_path, "data.json"))

        for dv in data["dataverses"]:

            url = os.getenv("BASE_URL") + "/api/dataverses/" + dv
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
                resp.json()["data"]["theme"]["linkUrl"] == data["dataverses"][dv]["url"]
            )
