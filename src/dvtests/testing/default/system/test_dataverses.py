import os

import pytest
from pyDataverse.api import NativeApi
from pyDataverse.models import Dataverse
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from ..conftest import read_json
from ..conftest import TESTING_CONFIG_DIR
from ..conftest import UTILS_DATA_DIR


all_dataverses = read_json(os.path.join(UTILS_DATA_DIR, "dataverses.json"))
test_config = read_json(
    os.path.join(TESTING_CONFIG_DIR, "default/system/test-config_dataverses.json")
)


class TestCreateDataverse:
    @pytest.mark.v4_20
    @pytest.mark.selenium
    @pytest.mark.parametrize(
        "homepage_logged_in",
        test_config["create-dataverse"]["min-valid"]["users"],
        indirect=True,
    )
    def test_min_valid(
        self, config, homepage_logged_in, users, dataverse_upload_min_01,
    ):
        """Test create a minimum Dataverse via frontend."""
        # Arrange
        is_created = False
        selenium, user_handle = homepage_logged_in
        wait = WebDriverWait(selenium, config.MAX_WAIT_TIME)
        form_fields = ["name", "alias", "contactEmail", "category"]
        dv = Dataverse()
        dv.set(dataverse_upload_min_01)
        # Act
        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//form[@id='addDataForm']/div[1]/button")
            )
        ).click()
        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//form[@id='addDataForm']/div[1]/ul/li[1]/a")
            )
        ).click()

        for ff in form_fields:
            fd = read_json(
                os.path.join(
                    TESTING_CONFIG_DIR,
                    "default/system/installation-config_form-data_create-dataverse.json",
                )
            )[ff]
            input_field = wait.until(
                EC.visibility_of_element_located((By.XPATH, fd["xpath"]))
            )
            if type(fd["content"]) == str:
                field_data = dv.get()[fd["content"]]
            elif type(fd["content"]) == list:
                field_data = dv.get()
                for idx in fd["content"]:
                    field_data = field_data[idx]
            if fd["type"] == "text":
                input_field.click()
                input_field.clear()
                input_field.send_keys(field_data)
            elif fd["type"] == "select":
                select = Select(input_field)
                select.select_by_value(field_data)
        if "affiliation" not in form_fields:
            input_field = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//input[@id='dataverseForm:affiliation']")
                )
            )
            input_field.click()
            input_field.clear()
        try:
            wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[@id='dataverseForm:save']")
                )
            ).click()
            is_created = True
            wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//div[contains(@class, 'alert-success')]")
                )
            )
            alert = selenium.find_element(
                By.XPATH, "//div[contains(@class, 'alert-success')]"
            )
            # Assert
            assert "Success!" in alert.text
            assert selenium.find_element(
                By.XPATH,
                "//div[contains(@class, 'alert-success')]/strong[text()='Success!']",
            )

            url = f'{config.BASE_URL}/dataverse/{dv.get()["alias"]}'
            selenium.get(url)

            assert selenium.current_url == url

            dv_header_unpublished = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//span[contains(@class, 'label-unpublished')]")
                )
            )
            assert dv_header_unpublished.text == "Unpublished"

            if "name" in form_fields:
                dv_header_name = wait.until(
                    EC.visibility_of_element_located(
                        (
                            By.XPATH,
                            "//a[contains(@class, 'dataverseHeaderDataverseName')]",
                        )
                    )
                )
                assert dv_header_name.text == dv.get()["name"]

            if "affiliation" in form_fields:
                dv_header_affiliation = wait.until(
                    EC.visibility_of_element_located(
                        (
                            By.XPATH,
                            "//div[contains(@class, 'dataverseHeaderName')]/span[1]",
                        )
                    )
                )
                assert dv_header_affiliation.text == f'({dv.get()["affiliation"]})'
        finally:
            # Cleanup
            if is_created:
                api = NativeApi(config.BASE_URL, users[user_handle]["api-token"])
                api.delete_dataverse(dv.get()["alias"])


class TestAllDataverses:
    @pytest.mark.v4_20
    @pytest.mark.utils
    @pytest.mark.parametrize("test_input", all_dataverses)
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
    @pytest.mark.utils
    @pytest.mark.parametrize("test_input", all_dataverses)
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
    @pytest.mark.utils
    @pytest.mark.selenium
    @pytest.mark.parametrize(
        "test_input,expected",
        test_config["all-dataverses"]["facet-not-logged-in"]["input-expected"],
    )
    def test_facet_not_logged_in(self, config, homepage, test_input, expected):
        """Test all Dataverse collections in facet as not-logged-in user."""
        # Arrange
        selenium = homepage
        wait = WebDriverWait(selenium, config.MAX_WAIT_TIME)
        # Act
        selenium.get(config.BASE_URL)
        wait = WebDriverWait(selenium, config.MAX_WAIT_TIME)
        wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[@id='dv-sidebar']"))
        )
        facet_dataverse = selenium.find_element(
            By.XPATH, "//span[@class='facetTypeDataverse']"
        )
        # Assert
        assert facet_dataverse.text == f"Dataverses ({expected['num-dataverses']})"
        # Cleanup
