import json
import os

import pytest

from ..conftest import TESTING_DATA_DIR


with open(
    os.path.join(TESTING_DATA_DIR, "default/unit/testdata_installation.json",)
) as json_file:
    testdata = json.load(json_file)


class TestVersion:
    @pytest.mark.v4_20
    @pytest.mark.parametrize("expected", testdata["version"]["valid"])
    def test_valid(self, native_api, expected):
        """Test Dataverse version."""
        # Arrange
        # Act
        resp = native_api.get_info_version()
        r_data = resp.json()["data"]
        # Assert
        assert r_data["version"] == expected["version"]
        assert r_data["build"] == expected["build"]
        # Cleanup


class TestServer:
    @pytest.mark.v4_20
    @pytest.mark.parametrize("expected", testdata["server"]["api-valid"])
    def test_api_valid(self, native_api, expected):
        """Test Dataverse server."""
        # Arrange
        # Act
        resp = native_api.get_info_server()
        r_data = resp.json()["data"]
        # Assert
        assert r_data["message"] == expected["url"]
        # Cleanup

    @pytest.mark.v4_20
    @pytest.mark.parametrize("expected", testdata["server"]["request-valid"])
    def test_request_valid(self, config, session, expected):
        """Test Dataverse server."""
        # Arrange
        # Act
        resp = session.get(config.BASE_URL)
        # Assert
        assert resp.headers["Server"] == expected["server"]
        assert resp.headers["Content-Encoding"] == expected["content-encoding"]
        assert resp.headers["Keep-Alive"] == expected["keep-alive"]
        assert resp.headers["Connection"] == expected["connection"]
        # Cleanup
