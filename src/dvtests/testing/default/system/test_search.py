import json
import os

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ..conftest import DATA_DIR
from ..conftest import search_header
from ..conftest import search_navbar
from ..conftest import TESTING_DATA_DIR


with open(
    os.path.join(TESTING_DATA_DIR, "default/system/testdata_search.json",)
) as json_file:
    testdata = json.load(json_file)


class TestSearch:
    @pytest.mark.v4_18_1
    @pytest.mark.v4_20
    @pytest.mark.selenium
    @pytest.mark.parametrize(
        "test_input,expected", testdata["search"]["navbar-not-logged-in"]
    )
    def test_search_navbar_not_logged_in(self, config, selenium, test_input, expected):
        """Test navbar search."""
        # Arrange
        num_dataverses = expected["num-dataverses"]
        num_datasets = expected["num-datasets"]
        num_datafiles = expected["num-datafiles"]
        # Act
        selenium = search_navbar(selenium, config, test_input["query"])
        facet_dataverse = selenium.find_element(By.CLASS_NAME, "facetTypeDataverse")
        facet_dataset = selenium.find_element(By.CLASS_NAME, "facetTypeDataset")
        facet_datafile = selenium.find_element(By.CLASS_NAME, "facetTypeFile")
        # Assert
        assert selenium.current_url == expected["url"]
        assert facet_dataverse.text == f"Dataverses ({num_dataverses})"
        assert facet_dataset.text == f"Datasets ({num_datasets})"
        assert facet_datafile.text == f"Files ({num_datafiles})"
        # Cleanup
