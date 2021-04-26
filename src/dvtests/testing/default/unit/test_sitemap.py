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
        "default/unit/testdata_sitemap.json",
    )
) as json_file:
    testdata = json.load(json_file)


class TestSitemap:
    @pytest.mark.v4_18_1
    @pytest.mark.v4_20
    @pytest.mark.parametrize("expected", testdata["sitemap"]["valid"])
    def test_valid(self, session, expected):
        """Test sitemap."""
        # Arrange
        url = f"{BASE_URL}/sitemap.xml"

        # Act
        resp = session.get(url)

        # Assert
        assert resp.status_code == 200
        # assert resp.encoding == expected["encoding"]
        assert resp.headers["Content-Type"] == expected["content-type"]

        # Cleanup
