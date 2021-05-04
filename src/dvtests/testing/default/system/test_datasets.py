import json
import os

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ..conftest import DATA_DIR
from ..conftest import TESTING_DATA_DIR

with open(os.path.join(DATA_DIR, "datasets.json",)) as json_file:
    testdata = json.load(json_file)


with open(
    os.path.join(TESTING_DATA_DIR, "default/system/testdata_datasets.json",)
) as json_file:
    test_config = json.load(json_file)


class TestAllDatasets:
    @pytest.mark.v4_20
    @pytest.mark.parametrize("test_input", testdata)
    def test_pid_url_not_logged_in(self, config, session, test_input):
        """Test all Dataset XHTML URL's as not-logged-in user."""
        # Arrange
        url = f"{config.BASE_URL}/dataset.xhtml?persistentId={test_input['pid']}"
        # Act
        resp = session.get(url)
        # Assert
        assert resp.status_code == 200
        assert resp.headers["Content-Type"] == "text/html;charset=UTF-8"
        assert resp.url == url
        # Cleanup

    @pytest.mark.v4_20
    @pytest.mark.parametrize("test_input", testdata)
    def test_doiorg_url(self, config, session, test_input):
        """Test all doi.org URL's."""
        # Arrange
        url_start = f"https://doi.org/{test_input['pid'][4:]}"
        url_end = f"{config.BASE_URL}/dataset.xhtml?persistentId={test_input['pid']}"
        # Act
        resp = session.get(url_start)
        # Assert
        assert resp.status_code == 200
        assert resp.headers["Content-Type"] == "text/html;charset=UTF-8"
        assert resp.url == url_end
        # Cleanup

    @pytest.mark.v4_20
    @pytest.mark.selenium
    @pytest.mark.parametrize(
        "expected", test_config["all-datasets"]["facet-not-logged-in"]
    )
    def test_facet_not_logged_in(self, config, selenium, expected):
        """Test all Datasets in facet as not-logged-in user."""
        # Arrange
        wait = WebDriverWait(selenium, config.MAX_WAIT_TIME)
        # Act
        selenium.get(config.BASE_URL)
        wait = WebDriverWait(selenium, config.MAX_WAIT_TIME)
        wait.until(EC.visibility_of_element_located((By.ID, "dv-sidebar")))
        facet_dataset = selenium.find_element(By.CLASS_NAME, "facetTypeDataset")

        # Assert
        assert facet_dataset.text == f"Datasets ({expected['num-datasets']})"
        # Cleanup
