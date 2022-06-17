import os
from time import sleep

import pytest
from pyDataverse.api import NativeApi
from pyDataverse.models import Dataverse
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from ..conftest import DEFAULT_DATAVERSE_CONFIG_DIR
from ..conftest import INSTALLATION_TESTING_CONFIG_DIR
from ..conftest import read_json


test_config = read_json(
    os.path.join(
        INSTALLATION_TESTING_CONFIG_DIR, "default/test_create-frontend_dataverse.json"
    )
)


class TestCreateFrontend:
    @pytest.mark.v4_20
    @pytest.mark.v5_2
    @pytest.mark.v5_6
    @pytest.mark.selenium
    @pytest.mark.parametrize(
        "homepage_logged_in",
        test_config["create-frontend"]["valid"]["users"],
        indirect=True,
    )
    @pytest.mark.parametrize(
        "testdata",
        test_config["create-frontend"]["valid"]["metadata-filenames"],
        indirect=True,
    )
    @pytest.mark.parametrize(
        "test_input,expected", test_config["create-frontend"]["valid"]["input-expected"]
    )
    def test_valid(
        self,
        config,
        homepage_logged_in,
        xpaths,
        users,
        native_api,
        testdata,
        test_input,
        expected,
    ):
        """Test create a minimum Dataverse via frontend."""
        # Arrange
        is_created = False
        selenium, user_handle = homepage_logged_in
        wait = WebDriverWait(selenium, config.MAX_WAIT_TIME)
        dv = Dataverse()
        dv.set(testdata)
        form_cfg = read_json(
            os.path.join(
                DEFAULT_DATAVERSE_CONFIG_DIR, "form-data_create-dataverse.json",
            )
        )
        attr_single = []
        attr_multiple = []
        for key, val in dv.get().items():
            if type(val) == str:
                attr_single.append(key)
            elif type(val) == list:
                attr_multiple.append(key)
        # dv.set({"hostdataverse": test_input["host-dataverse"]})
        # Act
        wait.until(
            EC.element_to_be_clickable((By.XPATH, xpaths["add-data-button"]))
        ).click()
        wait.until(
            EC.element_to_be_clickable((By.XPATH, xpaths["add-data-button-dataverse"]))
        ).click()

        for attr in test_input["clean-default-values"]:
            md_form_mapping = form_cfg[attr]
            input_field = wait.until(
                EC.visibility_of_element_located((By.XPATH, md_form_mapping["xpath"]))
            )
            input_field.click()
            input_field.clear()

        for attr, pdv_data in dv.get().items():
            md_form_mapping = form_cfg[attr]
            # prepare form_data
            if type(pdv_data) == list:
                form_data = []
                for item in pdv_data:
                    if type(item[md_form_mapping["metadata-child-name"]]) == str:
                        form_data.append(item[md_form_mapping["metadata-child-name"]])
            else:
                form_data = pdv_data
            # fill out form
            if md_form_mapping["form-type"] == "text":
                input_field = wait.until(
                    EC.element_to_be_clickable((By.XPATH, md_form_mapping["xpath"]))
                )
                input_field.click()
                input_field.clear()
                input_field.send_keys(form_data)
            elif md_form_mapping["form-type"] == "select":
                input_field = wait.until(
                    EC.visibility_of_element_located(
                        (By.XPATH, md_form_mapping["xpath"])
                    )
                )
                select = Select(input_field)
                select.select_by_value(form_data)
            elif md_form_mapping["form-type"] == "add-item":
                for count, val in enumerate(form_data):
                    input_field = wait.until(
                        EC.element_to_be_clickable(
                            (
                                By.XPATH,
                                "("
                                + md_form_mapping["xpath"]
                                + md_form_mapping["input"]["xpath"]
                                + ")["
                                + str(count + 1)
                                + "]",
                            )
                        )
                    )
                    input_field.click()
                    input_field.clear()
                    input_field.send_keys(val)
                    if count + 1 < len(form_data):
                        btn_add_item = wait.until(
                            EC.element_to_be_clickable(
                                (
                                    By.XPATH,
                                    "("
                                    + md_form_mapping["xpath"]
                                    + md_form_mapping["add-item"]["xpath"]
                                    + "[contains(@data-original-title, 'Add')])["
                                    + str(count + 1)
                                    + "]",
                                )
                            )
                        )
                        btn_add_item.click()
            elif md_form_mapping["form-type"] == "checkbox":
                # TODO: implement
                pass
        sleep(3)
        try:
            wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, xpaths["create-dataverse-button-save"])
                )
            ).click()
            is_created = True
            wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, xpaths["create-dataverse-note-alert-success"])
                )
            )
            alert = selenium.find_element(
                By.XPATH, xpaths["create-dataverse-note-alert-success"]
            )
            # Assert
            # verify alert box
            assert "Success!" in alert.text
            assert selenium.find_element(
                By.XPATH, xpaths["create-dataverse-note-alert-success-text"],
            )

            url = f'{config.BASE_URL}/dataverse/{dv.get()["alias"]}'
            # verify dataverse URL
            selenium.get(url)
            assert selenium.current_url == url
            # verify header title
            dv_header_unpublished = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, xpaths["dataverse-header-unpublished"])
                )
            )
            assert dv_header_unpublished.text == "Unpublished"
            if "name" in dv.get():
                dv_header_name = wait.until(
                    EC.visibility_of_element_located(
                        (By.XPATH, xpaths["dataverse-header-name"],)
                    )
                )
                assert dv_header_name.text == dv.get()["name"]
            if "affiliation" in dv.get():
                dv_header_affiliation = wait.until(
                    EC.visibility_of_element_located(
                        (By.XPATH, xpaths["dataverse-header-affiliation"],)
                    )
                )
                assert dv_header_affiliation.text == f'({dv.get()["affiliation"]})'
            # verify with API response
            api = NativeApi(config.BASE_URL, users[user_handle]["api-token"])
            dv_api = api.get_dataverse(dv.get()["alias"]).json()["data"]
            for attr in attr_single:
                assert dv_api[attr] == dv.get()[attr]
            for count, attr in enumerate(attr_multiple):
                dict_multiple = {}
                dict_multiple[attr] = []
                for ele in dv_api[attr]:
                    dict_multiple[attr].append(
                        ele[form_cfg[attr]["metadata-child-name"]]
                    )
            for attr in attr_multiple:
                for ele in dv.get()[attr]:
                    assert (
                        ele[form_cfg[attr]["metadata-child-name"]]
                        in dict_multiple[attr]
                    )
        finally:
            # Cleanup
            if is_created:
                api = NativeApi(config.BASE_URL, users[user_handle]["api-token"])
                api.delete_dataverse(dv.get()["alias"])
