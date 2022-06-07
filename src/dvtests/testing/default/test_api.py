import os

import pytest

from ..conftest import read_json
from ..conftest import TESTING_CONFIG_DIR

test_config = read_json(os.path.join(TESTING_CONFIG_DIR, "default/test_api.json"))

DATAVERSE_METADATA_ATTR = ["affiliation", "tagline", "linkUrl"]


class TestDataverse:
    @pytest.mark.v4_20
    @pytest.mark.parametrize(
        "test_input,expected", test_config["dataverse"]["valid"]["input-expected"]
    )
    def test_valid(self, config, native_api, test_input, expected):
        """Test important valid Dataverses."""
        # Arrange
        # Act
        resp = native_api.get_dataverse(test_input["alias"])
        resp_data = resp.json()["data"]
        # Assert
        assert resp_data["alias"] == expected["alias"]
        assert resp_data["name"] == expected["name"]
        for c in resp_data["dataverseContacts"]:
            assert c["contactEmail"] in expected["emails"]
        assert len(resp_data["dataverseContacts"]) == len(expected["emails"])
        for attr in DATAVERSE_METADATA_ATTR:
            if attr == "linkUrl" or attr == "tagline":
                if "tagline" in expected:
                    assert resp_data["theme"]["tagline"] == expected["tagline"]
                if "link-url" in expected:
                    assert resp_data["theme"]["linkUrl"] == expected["linkUrl"]
            else:
                if attr in expected:
                    assert resp_data[attr] == expected[attr]
        assert resp.status_code == 200
        if config.VERSION == "dataverse-docker_5-2-cvm":
            assert resp.headers["Content-Type"] == expected["content-type"]
        assert resp.url == expected["url"]
        # Cleanup
