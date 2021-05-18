import os

import pytest

from ..conftest import read_json
from ..conftest import TESTING_CONFIG_DIR


test_config = read_json(
    os.path.join(TESTING_CONFIG_DIR, "default/unit/test-config_sitemap.json",)
)


class TestSitemap:
    @pytest.mark.v4_20
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
        # assert resp.encoding == expected["encoding"] # TODO
        assert resp.headers["Content-Type"] == expected["content-type"]
        # Cleanup
