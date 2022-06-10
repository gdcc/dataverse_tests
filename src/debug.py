from dvtests.utils import create_testdata
from dvtests.utils import remove_testdata


if __name__ == "__main__":
    print("START --------------------------")

    if False:
        # Localhost Docker
        create_testdata("configs/localhost_docker/utils/create_testdata_01.json", False)
        remove_testdata("dataverseAdmin", "test_create_testdata", remove_parent=True)

    if True:
        # DV02
        create_testdata("configs/aussda_dv02/utils/create_testdata_01.json", False)
        # remove_testdata("dataverseAdmin", "test_create_testdata_3", remove_parent=True)

    print("END ----------------------------")
