import os

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ..conftest import read_json
from ..conftest import TESTING_DATA_DIR
from ..conftest import UTILS_DATA_DIR


testdata = read_json(os.path.join(UTILS_DATA_DIR, "datafiles.json",))
test_config = read_json(
    os.path.join(TESTING_DATA_DIR, "default/system/test-config_datafiles.json",)
)


class TestAllDatafiles:
    @pytest.mark.v4_20
    @pytest.mark.utils
    @pytest.mark.parametrize("datafiles", testdata)
    def test_fileid_url_not_logged_in(self, config, session, datafiles):
        """Test all Datafile File ID URL's as not-logged-in user."""
        # Arrange
        url = f"{config.BASE_URL}/file.xhtml?fileId={datafiles['datafile_id']}&version=:latest"
        # Act
        resp = session.get(url)
        # Assert
        assert resp.status_code == 200
        assert resp.headers["Content-Type"] == "text/html;charset=UTF-8"
        assert resp.url == url
        # Cleanup

    @pytest.mark.v4_20
    @pytest.mark.utils
    @pytest.mark.selenium
    @pytest.mark.parametrize("datafiles", testdata)
    def test_page_not_logged_in(self, config, selenium, datafiles):
        """Test all Datafile Pages as not-logged-in user."""
        # Arrange
        url = f"{config.BASE_URL}/file.xhtml?fileId={datafiles['datafile_id']}&version=:latest"
        # Act
        selenium.get(url)
        wait = WebDriverWait(selenium, config.MAX_WAIT_TIME)
        header_title = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//span[@class='file-title-label']")
            )
        )
        # Assert
        assert header_title.text == datafiles["label"]
        assert selenium.current_url == url
        # Cleanup

    @pytest.mark.v4_20
    @pytest.mark.utils
    @pytest.mark.selenium
    @pytest.mark.parametrize(
        "test_input,expected",
        test_config["all-datafiles"]["facet-not-logged-in"]["input-expected"],
    )
    def test_facet_not_logged_in(self, config, selenium, test_input, expected):
        """Test all Datafiles in facet as not-logged-in user."""
        # Arrange
        wait = WebDriverWait(selenium, config.MAX_WAIT_TIME)
        # Act
        selenium.get(config.BASE_URL)
        wait = WebDriverWait(selenium, config.MAX_WAIT_TIME)
        wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[@id='dv-sidebar']"))
        )
        facet_datafile = selenium.find_element(
            By.XPATH, "//span[@class='facetTypeFile']"
        )
        # Assert
        assert facet_datafile.text == f"Files ({expected['num-datafiles']})"
        # Cleanup
