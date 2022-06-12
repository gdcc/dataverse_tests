import os

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ..conftest import DEFAULT_DATAVERSE_CONFIG_DIR
from ..conftest import INSTALLATION_TESTING_CONFIG_DIR
from ..conftest import read_file
from ..conftest import read_json
from ..conftest import ROOT_DIR


test_config = read_json(
    os.path.join(INSTALLATION_TESTING_CONFIG_DIR, "default/test_registration.json",)
)


class TestTerms:
    @pytest.mark.v4_18_1
    @pytest.mark.v4_20
    @pytest.mark.v5_2
    @pytest.mark.v5_6
    @pytest.mark.parametrize(
        "test_input,expected", test_config["terms"]["valid"]["input-expected"],
    )
    def test_terms_valid(self, config, homepage, xpaths, test_input, expected):
        """Test Shibboleth interface."""
        # Arrange
        selenium = homepage
        wait = WebDriverWait(selenium, config.MAX_WAIT_TIME)
        selenium.get(f'{config.BASE_URL}{test_input["url"]}')
        # Act
        term_of_use_selenium = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, xpaths["register-div-terms-of-use"])
            )
        )
        selenium_html = (
            term_of_use_selenium.get_attribute("innerHTML").replace("\n ", "").strip()
        )
        if "terms-filename" in expected:
            tou_html = read_file(os.path.join(ROOT_DIR, expected["terms-filename"]))
        else:
            tou_html = read_file(
                os.path.join(DEFAULT_DATAVERSE_CONFIG_DIR, "terms-of-use.html")
            )
        tou_html = tou_html.replace("\n", "")

        # Assert
        assert selenium_html == tou_html
        # Cleanup
