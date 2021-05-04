import json
import os

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ..conftest import DATA_DIR
from ..conftest import TESTING_DATA_DIR


with open(os.path.join(DATA_DIR, "dataverses.json",)) as json_file:
    testdata = json.load(json_file)


with open(
    os.path.join(TESTING_DATA_DIR, "default/system/testdata_dataverses.json",)
) as json_file:
    test_config = json.load(json_file)


class TestAllDataverses:
    @pytest.mark.v4_20
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

    @pytest.mark.v4_20
    @pytest.mark.selenium
    @pytest.mark.parametrize(
        "expected", test_config["all-dataverses"]["facet-not-logged-in"]
    )
    def test_facet_not_logged_in(self, config, selenium, expected):
        """Test all Dataverse collections in facet as not-logged-in user."""
        # Arrange
        wait = WebDriverWait(selenium, config.MAX_WAIT_TIME)
        # Act
        selenium.get(config.BASE_URL)
        wait = WebDriverWait(selenium, config.MAX_WAIT_TIME)
        wait.until(EC.visibility_of_element_located((By.ID, "dv-sidebar")))
        facet_dataverse = selenium.find_element(By.CLASS_NAME, "facetTypeDataverse")
        # Assert
        assert facet_dataverse.text == f"Dataverses ({expected['num-dataverses']})"
        # Cleanup
