import os

import pytest
from selenium.webdriver.common.by import By

from ..conftest import INSTALLATION_TESTING_CONFIG_DIR
from ..conftest import read_json
from ..conftest import search_navbar


test_config = read_json(
    os.path.join(INSTALLATION_TESTING_CONFIG_DIR, "default/test_search.json",)
)


class TestSearch:
    @pytest.mark.v4_18_1
    @pytest.mark.v4_20
    @pytest.mark.v5_2
    @pytest.mark.v5_6
    @pytest.mark.v5_7
    @pytest.mark.selenium
    @pytest.mark.parametrize(
        "test_input,expected",
        test_config["search"]["navbar-not-logged-in"]["input-expected"],
    )
    def test_search_navbar_not_logged_in(
        self, config, homepage, xpaths, test_input, expected
    ):
        """Test navbar search."""
        # Arrange
        selenium = homepage
        num_dataverses = expected["num-dataverses"]
        num_datasets = expected["num-datasets"]
        num_datafiles = expected["num-datafiles"]
        # Act
        selenium = search_navbar(selenium, config, xpaths, test_input["query"])
        facet_dataverse = selenium.find_element(
            By.XPATH, xpaths["sidebar-facet-dataverse"]
        )
        facet_dataset = selenium.find_element(By.XPATH, xpaths["sidebar-facet-dataset"])
        facet_datafile = selenium.find_element(
            By.XPATH, xpaths["sidebar-facet-datafile"]
        )
        # Assert
        assert selenium.current_url == expected["url"]
        assert facet_dataverse.text == f"Dataverses ({num_dataverses})"
        assert facet_dataset.text == f"Datasets ({num_datasets})"
        assert facet_datafile.text == f"Files ({num_datafiles})"
        # Cleanup
