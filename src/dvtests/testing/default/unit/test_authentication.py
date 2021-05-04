import json
import os

import pytest

from ..conftest import TESTING_DATA_DIR


with open(
    os.path.join(TESTING_DATA_DIR, "default/unit/testdata_authentication.json",)
) as json_file:
    testdata = json.load(json_file)


class TestShibboleth:
    @pytest.mark.v4_20
    @pytest.mark.parametrize(
        "test_input,expected", testdata["shibboleth"]["interface-valid"]
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
