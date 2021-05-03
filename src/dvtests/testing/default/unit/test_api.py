import json
import os

import pytest

from ..conftest import CONFIG
from ..conftest import ROOT_DIR
from ..conftest import TESTING_DATA_DIR


with open(
    os.path.join(TESTING_DATA_DIR, "default/unit/testdata_api.json")
) as json_file:
    testdata = json.load(json_file)


class TestDataverse:
    @pytest.mark.v4_18_1
    @pytest.mark.v4_20
    @pytest.mark.parametrize("test_input,expected", testdata["dataverse"]["valid"])
    def test_valid(self, config, native_api, test_input, expected):
        """Test important Dataverses."""
        # Arrange
        # Act
        resp = native_api.get_dataverse(test_input["alias"])
        r_data = resp.json()["data"]

        # Assert
        assert r_data["alias"] == expected["alias"]
        assert r_data["name"] == expected["name"]
        assert r_data["affiliation"] == expected["affiliation"]
        for c in r_data["dataverseContacts"]:
            assert c["contactEmail"] in expected["emails"]
        assert len(r_data["dataverseContacts"]) == len(expected["emails"])
        assert r_data["theme"]["tagline"] == expected["tagline"]
        assert r_data["theme"]["linkUrl"] == expected["link-url"]
        assert resp.status_code == 200
        assert resp.headers["Content-Type"] == "application/json"
        assert resp.url == expected["url"]

        # Cleanup
