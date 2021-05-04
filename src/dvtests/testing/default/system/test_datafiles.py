import json
import os

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ..conftest import DATA_DIR
from ..conftest import TESTING_DATA_DIR


with open(os.path.join(DATA_DIR, "datafiles.json",)) as json_file:
    testdata = json.load(json_file)


with open(
    os.path.join(TESTING_DATA_DIR, "default/system/testdata_datafiles.json",)
) as json_file:
    test_config = json.load(json_file)


class TestAllDatafiles:
    @pytest.mark.v4_20
    @pytest.mark.parametrize("test_input", testdata)
    def test_fileid_url_not_logged_in(self, config, session, test_input):
        """Test all Datafile File ID URL's as not-logged-in user."""
        # Arrange
        url = f"{config.BASE_URL}/file.xhtml?fileId={test_input['datafile_id']}&version=:latest"
        # Act
        resp = session.get(url)
        # Assert
        assert resp.status_code == 200
        assert resp.headers["Content-Type"] == "text/html;charset=UTF-8"
        assert resp.url == url
        # Cleanup

    @pytest.mark.v4_20
    @pytest.mark.selenium
    @pytest.mark.parametrize("test_input", testdata)
    def test_page_not_logged_in(self, config, selenium, test_input):
        """Test all Datafile Pages as not-logged-in user."""
        # Arrange
        url = f"{config.BASE_URL}/file.xhtml?fileId={test_input['datafile_id']}&version=:latest"
        # Act
        selenium.get(url)
        wait = WebDriverWait(selenium, config.MAX_WAIT_TIME)
        header_title = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "file-title-label"))
        )
        # Assert
        assert header_title.text == test_input["label"]
        assert selenium.current_url == url
        # Cleanup

    @pytest.mark.v4_20
    @pytest.mark.selenium
    @pytest.mark.parametrize(
        "expected", test_config["all-datafiles"]["facet-not-logged-in"]
    )
    def test_facet_not_logged_in(self, config, selenium, expected):
        """Test all Datafiles in facet as not-logged-in user."""
        # Arrange
        wait = WebDriverWait(selenium, config.MAX_WAIT_TIME)
        # Act
        selenium.get(config.BASE_URL)
        wait = WebDriverWait(selenium, config.MAX_WAIT_TIME)
        wait.until(EC.visibility_of_element_located((By.ID, "dv-sidebar")))
        facet_datafile = selenium.find_element(By.CLASS_NAME, "facetTypeFile")

        # Assert
        assert facet_datafile.text == f"Files ({expected['num-datafiles']})"
        # Cleanup
