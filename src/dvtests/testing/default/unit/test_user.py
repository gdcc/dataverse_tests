import os

import pytest

from ..conftest import read_json
from ..conftest import TESTING_CONFIG_DIR

test_config = read_json(
    os.path.join(TESTING_CONFIG_DIR, "default/unit/test-config_user.json",)
)


class TestApi:
    @pytest.mark.v5_2
    @pytest.mark.parametrize(
        "test_input,expected", test_config["api"]["valid"]["input-expected"]
    )
    def test_valid(self, native_api, test_input, expected):
        """Test API user endpoint.

        Does not work below Dataverse 5.2.
        """
        # Arrange
        # Act
        resp = native_api.get_user()
        r_data = resp.json()["data"]
        # Assert
        assert r_data["message"] == expected["url"]
        # Cleanup
