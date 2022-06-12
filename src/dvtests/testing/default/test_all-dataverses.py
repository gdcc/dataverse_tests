import os

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ..conftest import CONFIG
from ..conftest import INSTALLATION_TESTING_CONFIG_DIR
from ..conftest import read_json
from ..conftest import UTILS_DATA_DIR


testdata = read_json(os.path.join(UTILS_DATA_DIR, "public", CONFIG.FILENAME_DATAVERSES))
test_config = read_json(
    os.path.join(INSTALLATION_TESTING_CONFIG_DIR, "default/test_all-dataverses.json")
)


class TestAccess:
    @pytest.mark.v4_20
    @pytest.mark.v5_2
    @pytest.mark.v5_6
    @pytest.mark.utils
    @pytest.mark.parametrize("test_input", testdata)
    def test_xhtml_url_not_logged_in(self, config, session, test_input):
        """Test all Dataverse collection XHTML URL's as not-logged-in user."""
        # Arrange
        url = f"{config.BASE_URL}/dataverse.xhtml?alias={test_input['dataverse_alias']}"
        # Act
        resp = session.get(url)
        # Assert
        assert resp.status_code == 200
        assert resp.headers["Content-Type"] == "text/html;charset=UTF-8"
        assert resp.url == url
        # Cleanup

    @pytest.mark.v4_20
    @pytest.mark.v5_2
    @pytest.mark.v5_6
    @pytest.mark.utils
    @pytest.mark.parametrize("test_input", testdata)
    def test_clean_url_not_logged_in(self, config, session, test_input):
        """Test all Dataverse collection clean URL's as not-logged-in user."""
        # Arrange
        url = f"{config.BASE_URL}/dataverse/{test_input['dataverse_alias']}"
        # Act
        resp = session.get(url)
        # Assert
        assert resp.status_code == 200
        assert resp.headers["Content-Type"] == "text/html;charset=UTF-8"
        assert resp.url == url
        # Cleanup


class TestSidebar:
    @pytest.mark.v4_20
    @pytest.mark.v5_2
    @pytest.mark.v5_6
    @pytest.mark.utils
    @pytest.mark.selenium
    @pytest.mark.parametrize(
        "test_input,expected",
        test_config["sidebar"]["facet-not-logged-in"]["input-expected"],
    )
    def test_facet_not_logged_in(self, config, homepage, xpaths, test_input, expected):
        """Test all Dataverse collections in facet as not-logged-in user."""
        # Arrange
        selenium = homepage
        wait = WebDriverWait(selenium, config.MAX_WAIT_TIME)
        # Act
        selenium.get(config.BASE_URL)
        wait = WebDriverWait(selenium, config.MAX_WAIT_TIME)
        wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["div-sidebar"])))
        facet_dataverse = selenium.find_element(
            By.XPATH, xpaths["sidebar-facet-dataverse"]
        )
        # Assert
        assert facet_dataverse.text == f"Dataverses ({expected['num-dataverses']})"
        # Cleanup
