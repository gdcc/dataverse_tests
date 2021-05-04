import json
import os

import pytest

from ..conftest import TESTING_DATA_DIR


with open(
    os.path.join(TESTING_DATA_DIR, "default/unit/testdata_sitemap.json",)
) as json_file:
    testdata = json.load(json_file)


class TestSitemap:
    @pytest.mark.v4_20
    @pytest.mark.parametrize("expected", testdata["sitemap"]["valid"])
    def test_valid(self, config, session, expected):
        """Test sitemap."""
        # Arrange
        url = f"{config.BASE_URL}/sitemap.xml"
        # Act
        resp = session.get(url)
        # Assert
        assert resp.status_code == 200
        # assert resp.encoding == expected["encoding"] # TODO
        assert resp.headers["Content-Type"] == expected["content-type"]
        # Cleanup
