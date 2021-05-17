import os

import pytest
from selenium.webdriver.common.by import By

from ..conftest import read_json
from ..conftest import search_navbar
from ..conftest import TESTING_CONFIG_DIR


test_config = read_json(
    os.path.join(TESTING_CONFIG_DIR, "default/system/test-config_search.json",)
)


class TestSearch:
    @pytest.mark.v4_20
    @pytest.mark.selenium
    @pytest.mark.parametrize(
        "test_input,expected",
        test_config["search"]["navbar-not-logged-in"]["input-expected"],
    )
    def test_search_navbar_not_logged_in(self, config, homepage, test_input, expected):
        """Test navbar search."""
        # Arrange
        selenium = homepage
        num_dataverses = expected["num-dataverses"]
        num_datasets = expected["num-datasets"]
        num_datafiles = expected["num-datafiles"]
        # Act
        selenium = search_navbar(selenium, config, test_input["query"])
        facet_dataverse = selenium.find_element(
            By.XPATH, "//span[@class='facetTypeDataverse']"
        )
        facet_dataset = selenium.find_element(
            By.XPATH, "//span[@class='facetTypeDataset']"
        )
        facet_datafile = selenium.find_element(
            By.XPATH, "//span[@class='facetTypeFile']"
        )
        # Assert
        assert selenium.current_url == expected["url"]
        assert facet_dataverse.text == f"Dataverses ({num_dataverses})"
        assert facet_dataset.text == f"Datasets ({num_datasets})"
        assert facet_datafile.text == f"Files ({num_datafiles})"
        # Cleanup
