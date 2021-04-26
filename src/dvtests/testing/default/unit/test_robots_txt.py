import json
import os

import pytest

from ..conftest import BASE_URL
from ..conftest import INSTANCE
from ..conftest import ROOT_DIR


with open(
    os.path.join(
        ROOT_DIR,
        "src/dvtests/testing/data",
        INSTANCE,
        "default/unit/testdata_robots-txt.json",
    )
) as json_file:
    testdata = json.load(json_file)


class TestRobotsTxt:
    @pytest.mark.v4_18_1
    @pytest.mark.v4_20
    @pytest.mark.parametrize("expected", testdata["robots-txt"]["valid"])
    def test_valid(self, session, expected):
        """Test robots.txt."""
        # Arrange
        url = f"{BASE_URL}/robots.txt"

        # Act
        resp = session.get(url)

        # Assert
        assert resp.url == url
        assert resp.status_code == 200
        assert resp.encoding == expected["encoding"]
        assert resp.headers["Content-Type"] == expected["content-type"]

        # Cleanup
