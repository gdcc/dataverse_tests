import os

import pytest

from ..conftest import INSTALLATION_TESTING_CONFIG_DIR
from ..conftest import read_json


test_config = read_json(
    os.path.join(INSTALLATION_TESTING_CONFIG_DIR, "default/test_robots-txt.json",)
)


class TestRobotsTxt:
    @pytest.mark.v4_18_1
    @pytest.mark.v4_20
    @pytest.mark.v5_2
    @pytest.mark.v5_6
    @pytest.mark.v5_7
    @pytest.mark.parametrize(
        "test_input,expected", test_config["robots-txt"]["valid"]["input-expected"]
    )
    def test_valid(self, config, session, test_input, expected):
        """Test robots.txt."""
        # Arrange
        url = f"{config.BASE_URL}/robots.txt"
        # Act
        resp = session.get(url)
        # Assert
        assert resp.url == url
        assert resp.status_code == 200
        assert resp.encoding == expected["encoding"]
        if config.VERSION == "dataverse_4-20":
            assert resp.headers["Content-Type"] == expected["content-type"]
        # Cleanup
