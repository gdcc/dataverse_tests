import os

import pytest

from ..conftest import read_json
from ..conftest import TESTING_CONFIG_DIR


test_config = read_json(
    os.path.join(TESTING_CONFIG_DIR, "default/unit/test-config_authentication.json",)
)


class TestShibboleth:
    @pytest.mark.v4_20
    @pytest.mark.parametrize(
        "test_input,expected",
        test_config["shibboleth"]["interface-valid"]["input-expected"],
    )
    def test_interface_valid(self, config, session, test_input, expected):
        """Test Shibboleth interface."""
        # Arrange
        url = f'{config.BASE_URL}{test_input["url"]}'
        # Act
        resp = session.get(url)
        # Assert
        assert resp.url == url
        assert resp.status_code == 200
        assert resp.headers["Content-Type"] == expected["content-type"]
        # Cleanup
