import os

import pytest

from ..conftest import INSTALLATION_TESTING_CONFIG_DIR
from ..conftest import read_json


test_config = read_json(
    os.path.join(INSTALLATION_TESTING_CONFIG_DIR, "default/test_sitemap.json",)
)


class TestSitemap:
    @pytest.mark.v4_20
    @pytest.mark.v5_2
    @pytest.mark.v5_6
    @pytest.mark.parametrize(
        "test_input,expected", test_config["sitemap"]["valid"]["input-expected"]
    )
    def test_valid(self, config, session, test_input, expected):
        """Test sitemap."""
        # Arrange
        url = f"{config.BASE_URL}/sitemap.xml"
        # Act
        resp = session.get(url)
        # Assert
        assert resp.status_code == 200
        assert resp.headers["Content-Type"] == expected["content-type"]
        # Cleanup
