import os

import pytest

from ..conftest import INSTALLATION_TESTING_CONFIG_DIR
from ..conftest import read_json


test_config = read_json(
    os.path.join(INSTALLATION_TESTING_CONFIG_DIR, "default/test_oaipmh.json",)
)


class TestEndpoint:
    @pytest.mark.v4_20
    @pytest.mark.v5_6
    @pytest.mark.parametrize(
        "test_input,expected", test_config["endpoint"]["valid"]["input-expected"]
    )
    def test_valid(self, session, test_input, expected):
        """Test OAI-PMH endpoints."""
        # Arrange
        # Act
        resp = session.get(test_input["url"])
        # Assert
        assert resp.text
        assert resp.url == test_input["url"]
        assert resp.status_code == 200
        assert resp.encoding == expected["encoding"]
        assert resp.headers["Content-Type"] == expected["content-type"]
        # Cleanup
