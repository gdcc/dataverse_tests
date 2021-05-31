import os

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ..conftest import read_file
from ..conftest import read_json
from ..conftest import ROOT_DIR
from ..conftest import TESTING_CONFIG_DIR


test_config = read_json(
    os.path.join(TESTING_CONFIG_DIR, "default/unit/test-config_registration.json",)
)


class TestTerms:
    @pytest.mark.v4_20
    @pytest.mark.parametrize(
        "test_input,expected", test_config["terms"]["valid"]["input-expected"],
    )
    def test_terms_valid(self, config, homepage, test_input, expected):
        """Test Shibboleth interface."""
        # Arrange
        selenium = homepage
        wait = WebDriverWait(selenium, config.MAX_WAIT_TIME)
        selenium.get(f'{config.BASE_URL}{test_input["url"]}')
        # Act
        term_of_use_selenium = wait.until(
            EC.visibility_of_element_located((By.XPATH, test_input["xpath"]))
        )
        selenium_html = (
            term_of_use_selenium.get_attribute("innerHTML").replace("\n ", "").strip()
        )
        file_html = read_file(os.path.join(ROOT_DIR, expected["terms-filename"]))
        # Assert
        assert selenium_html == file_html
        # Cleanup
