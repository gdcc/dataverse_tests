import json
import os

import pytest

from ..conftest import TESTING_DATA_DIR


with open(
    os.path.join(TESTING_DATA_DIR, "default/unit/testdata_robots-txt.json",)
) as json_file:
    testdata = json.load(json_file)


class TestRobotsTxt:
    @pytest.mark.v4_20
    @pytest.mark.parametrize("expected", testdata["robots-txt"]["valid"])
    def test_valid(self, config, session, expected):
        """Test robots.txt."""
        # Arrange
        url = f"{config.BASE_URL}/robots.txt"
        # Act
        resp = session.get(url)
        # Assert
        assert resp.url == url
        assert resp.status_code == 200
        assert resp.encoding == expected["encoding"]
        assert resp.headers["Content-Type"] == expected["content-type"]
        # Cleanup
