import os

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ..conftest import CONFIG
from ..conftest import INSTALLATION_TESTING_CONFIG_DIR
from ..conftest import read_json
from ..conftest import UTILS_DATA_DIR


testdata = read_json(os.path.join(UTILS_DATA_DIR, "public", CONFIG.FILENAME_DATASETS,))
test_config = read_json(
    os.path.join(INSTALLATION_TESTING_CONFIG_DIR, "default/test_all-datasets.json")
)


class TestAccess:
    @pytest.mark.v4_20
    @pytest.mark.v5_2
    @pytest.mark.v5_6
    @pytest.mark.utils
    @pytest.mark.parametrize("test_input", testdata)
    def test_pid_url_not_logged_in(self, config, session, test_input):
        """Test all Dataset XHTML URL's as not-logged-in user."""
        # Arrange
        url = f"{config.BASE_URL}/dataset.xhtml?persistentId={test_input['pid']}"
        # Act
        resp = session.get(url)
        # Assert
        assert resp.status_code == 200
        assert (
            resp.headers["Content-Type"]
            == test_config["test-pid-url-not-logged-in"]["header-content-type"]
        )
        assert resp.url == url
        # Cleanup

    @pytest.mark.v4_20
    @pytest.mark.v5_2
    @pytest.mark.v5_6
    @pytest.mark.utils
    @pytest.mark.parametrize("test_input", testdata)
    def test_doiorg_url(self, config, session, test_input):
        """Test all doi.org URL's."""
        # Arrange
        url_start = f"https://doi.org/{test_input['pid']}"
        url_end = f"{config.BASE_URL}/dataset.xhtml?persistentId={test_input['pid']}"
        # Act
        resp = session.get(url_start)
        # Assert
        assert resp.status_code == 200
        assert (
            resp.headers["Content-Type"]
            == test_config["test-doiorg-url"]["header-content-type"]
        )
        assert resp.url == url_end
        # Cleanup


class TestSidebar:
    @pytest.mark.v4_20
    @pytest.mark.v5_2
    @pytest.mark.v5_6
    @pytest.mark.selenium
    @pytest.mark.utils
    @pytest.mark.parametrize(
        "test_input,expected",
        test_config["sidebar"]["facet-not-logged-in"]["input-expected"],
    )
    def test_facet_not_logged_in(self, config, homepage, xpaths, test_input, expected):
        """Test all Datasets in facet as not-logged-in user."""
        # Arrange
        selenium = homepage
        wait = WebDriverWait(selenium, config.MAX_WAIT_TIME)
        # Act
        selenium.get(config.BASE_URL)
        wait = WebDriverWait(selenium, config.MAX_WAIT_TIME)
        wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["div-sidebar"])))
        facet_dataset = selenium.find_element(By.XPATH, xpaths["sidebar-facet-dataset"])
        # Assert
        assert facet_dataset.text == f"Datasets ({expected['num-datasets']})"
        # Cleanup
