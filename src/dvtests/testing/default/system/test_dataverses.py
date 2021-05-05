import os

import pytest
from pyDataverse.api import NativeApi
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from ..conftest import custom_click_cookie_rollbar
from ..conftest import DATA_DIR
from ..conftest import login_normal
from ..conftest import read_json
from ..conftest import TESTING_DATA_DIR


all_dataverses = read_json(os.path.join(DATA_DIR, "dataverses.json"))
test_config = read_json(
    os.path.join(TESTING_DATA_DIR, "default/system/testdata_dataverses.json")
)

FORM_DATA_CREATE_DATASET_DV_4_20 = {
    "name": {"form-name": "name", "form-type": "text", "data-name": "name"},
    "alias": {"form-name": "identifier", "form-type": "text", "data-name": "alias"},
    "category": {
        "form-name": "dataverseCategory",
        "form-type": "select",
        "data-name": "dataverseType",
    },
    "storage": {
        "form-name": "dataverseStorage",
        "form-type": "select",
        "data-name": "",
    },
    "affiliation": {
        "form-name": "affiliation",
        "form-type": "text",
        "data-name": "affiliation",
    },
    "parent-dataverse": {
        "form-name": "selectHostDataverse",
        "form-type": "text",
        "data-name": "",
    },
    "description": {
        "form-name": "description",
        "form-type": "text",
        "data-name": "description",
    },
    "contactEmail": {
        "form-name": "j_idt259:0:contactEmail",
        "form-type": "text",
        "data-name": ["dataverseContacts", 0, "contactEmail"],
    },
}


class TestCreateDataverse:
    @pytest.mark.v4_20
    @pytest.mark.parametrize("test_input", test_config["create-dataverse"]["min-valid"])
    def test_min_valid(
        self, config, selenium, native_api, users, dataverse_upload_min_01, test_input
    ):
        """Test create a minimum Dataverse via frontend."""
        # Arrange
        wait = WebDriverWait(selenium, config.MAX_WAIT_TIME)
        dv = dataverse_upload_min_01
        selenium = login_normal(
            selenium,
            config.BASE_URL,
            config.LOGIN_OPTIONS,
            test_input["user-handle"],
            users[test_input["user-handle"]]["password"],
            config.MAX_WAIT_TIME,
        )
        form_fields = ["name", "alias", "contactEmail", "category"]
        custom_click_cookie_rollbar(selenium, config.MAX_WAIT_TIME)
        # Act
        wait.until(EC.element_to_be_clickable((By.ID, "addDataForm"))).click()
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "New Dataverse"))).click()

        for ff in form_fields:
            fd = FORM_DATA_CREATE_DATASET_DV_4_20[ff]
            input_field = wait.until(
                EC.visibility_of_element_located(
                    (By.ID, f'dataverseForm:{fd["form-name"]}')
                )
            )
            if type(fd["data-name"]) == str:
                field_data = dv[fd["data-name"]]
            elif type(fd["data-name"]) == list:
                field_data = dv
                for idx in fd["data-name"]:
                    field_data = field_data[idx]
            if fd["form-type"] == "text":
                input_field.click()
                input_field.clear()
                input_field.send_keys(field_data)
            elif fd["form-type"] == "select":
                select = Select(input_field)
                select.select_by_value(field_data)
        if "affiliation" not in form_fields:
            input_field = wait.until(
                EC.visibility_of_element_located((By.ID, f"dataverseForm:affiliation"))
            )
            input_field.click()
            input_field.clear()
        try:
            wait.until(
                EC.element_to_be_clickable((By.ID, "dataverseForm:save"))
            ).click()
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "alert")))
            alert = selenium.find_element(By.CLASS_NAME, "alert")
            # Assert
            assert "Success!" in alert.text
            assert alert.find_element(By.CLASS_NAME, "glyphicon-ok-sign")

            url = f'{config.BASE_URL}/dataverse/{dv["alias"]}'
            selenium.get(url)

            assert selenium.current_url == url

            dv_header_unpublished = wait.until(
                EC.visibility_of_element_located((By.CLASS_NAME, "label-unpublished"))
            )
            assert dv_header_unpublished.text == "Unpublished"

            if "name" in form_fields:
                dv_header_name = wait.until(
                    EC.visibility_of_element_located(
                        (By.CLASS_NAME, "dataverseHeaderDataverseName")
                    )
                )
                assert dv_header_name.text == dv["name"]

            if "affiliation" in form_fields:
                dv_header_affiliation = wait.until(
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, ".dataverseHeaderName:first-child")
                    )
                )
                assert dv_header_affiliation.text == f'({dv["affiliation"]})'
        finally:
            # Cleanup
            api = NativeApi(
                config.BASE_URL, users[test_input["user-handle"]]["api-token"]
            )
            resp = api.delete_dataverse(dv["alias"])


class TestAllDataverses:
    @pytest.mark.v4_20
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
