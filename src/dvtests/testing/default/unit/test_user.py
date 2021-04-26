import json
import os

import pytest

from ..conftest import INSTANCE
from ..conftest import ROOT_DIR


with open(
    os.path.join(
        ROOT_DIR,
        "src/dvtests/testing/data",
        INSTANCE,
        "default/unit/testdata_user.json",
    )
) as json_file:
    testdata = json.load(json_file)


class TestApi:
    @pytest.mark.v5_2
    @pytest.mark.parametrize("expected", testdata["api"]["valid"])
    def test_valid(self, native_api, expected):
        """

        Input
        * base url

        Expected result
        * base url

        """
        """Test user endpoint.

        Does not work below Dataverse 5.3 or 5.2
        """
        # Arrange
        # Act
        resp = native_api.get_user()
        print(resp)
        r_data = resp.json()["data"]

        # Assert
        assert r_data["message"] == expected["url"]

        # Cleanup
