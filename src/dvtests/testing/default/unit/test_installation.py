import os

import pytest

from ..conftest import read_json
from ..conftest import TESTING_DATA_DIR


test_config = read_json(
    os.path.join(TESTING_DATA_DIR, "default/unit/test-config_installation.json")
)


class TestVersion:
    @pytest.mark.v4_20
    @pytest.mark.parametrize(
        "test_input,expected", test_config["version"]["valid"]["input-expected"]
    )
    def test_valid(self, native_api, test_input, expected):
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
    @pytest.mark.parametrize(
        "test_input,expected", test_config["server"]["api-valid"]["input-expected"]
    )
    def test_api_valid(self, native_api, test_input, expected):
        """Test Dataverse server via API."""
        # Arrange
        # Act
        resp = native_api.get_info_server()
        r_data = resp.json()["data"]
        # Assert
        assert r_data["message"] == expected["url"]
        # Cleanup

    @pytest.mark.v4_20
    @pytest.mark.parametrize(
        "test_input,expected", test_config["server"]["request-valid"]["input-expected"]
    )
    def test_request_valid(self, config, session, test_input, expected):
        """Test Dataverse server via homepage."""
        # Arrange
        # Act
        resp = session.get(config.BASE_URL)
        # Assert
        assert resp.headers["Server"] == expected["server"]
        assert resp.headers["Content-Encoding"] == expected["content-encoding"]
        assert resp.headers["Keep-Alive"] == expected["keep-alive"]
        assert resp.headers["Connection"] == expected["connection"]
        # Cleanup
