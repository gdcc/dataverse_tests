# AUSSDA Tests

Python Tests for Jenkins to test our different Dataverse instances and our website. Tests are written with pytest and Selenium, easy to adapt and extend and Open Source.

**Features**

* flexible and easy, so can use it as fast as possible for your own Dataverse instance.
* easy to extend: add new tests (please create a PR!), add your own instance
* `utils` functions to help you with creating needed data for the tests
  * create and remove testdata
  * collect all Dataverse, Datasets and Datafiels store data in JSON files for completeness tests
  * CLI integration
* `tests` to execute basic tests for Dataverse (mostly Selenium)
* Open Source (MIT)

## Install

**Pre-requisites**

Python >= 3.6

Python modules (see `requirements.txt`):
* [pyDataverse](https://github.com/AUSSDA/pyDataverse) ([#3b040ff23b665ec2650bebcf4bd5478de6881af0](https://github.com/AUSSDA/pyDataverse/commit/3b040ff23b665ec2650bebcf4bd5478de6881af0))
* [pytest](https://docs.pytest.org/en/stable/)
* [selenium](https://selenium-python.readthedocs.io/)
* [pydantic](https://pydantic-docs.helpmanual.io/)

Repositories (included as submodules). These must be substituted/adapted for usage outside of AUSSDA.
* private (AUSSDA only)
  * [jenkins_private](https://github.com/AUSSDA/jenkins_private): stores secret Dataverse credentials needed for some tests.
  * [aussda_test-data](https://github.com/AUSSDA/aussda_test-data): AUSSDA specific test data. Real world and artifical data for the Social Sciences.
* public
  * [terms](https://github.com/AUSSDA/terms): Terms of Use, Terms of Access and licenses used by AUSSDA.

**Clone repository**

```shell
git clone https://github.com/AUSSDA/aussda_tests.git
cd aussda_tests/
```

**Install packages**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

### Tests

The folder `tests/` contains all tests. They are seperated into `dataverse/`, `website/` and `external-resources/`.

Tests are executed with pytest:

```shell
pytest -v
```

**Environment variables**

* `INSTANCE`: Dataverse instance to be tested. There are three AUSSDA instances used and configured so far: `dataverse_production`, `dataverse_dv03` and `dataverse_localhost_t550`.

Set via `.env` files (so far placed in the repo root directory, will move later to private submodule.):
* You can use `.env.sample` as a template
* `HEADLESS`: Executes Selenium tests with or without browser window opening (by default `true` -> without browser window).
* `TEST_USER_NORMAL`: User for normal login.
* `TEST_USER_NORMAL_NAME`: Real name of user normal login.
* `TEST_USER_NORMAL_PWD`: Password of user normal login.

**Adapt tests to your own Dataverse instance**

To use the tests for your own Dataverse instance, you have to:
* Add for each instance an `.env` file with the needed environment variables inside (see above).
* Add another subclass of `Config` in `tests/config.py`, where you call your `.env` file. Add the Class to the `get_config()` function.
* Create for each instance a folder with a `dataverse_` prefix inside `tests/data/instances/`, in which you then can add all needed files for your tests.
  * `test-data.json` (required):
    * Needed data for test execution of one Dataverse instance.
    * We recommend using an existing one from AUSSDA and adapt it to your needs (e. g. `tests/data/instances/dataverse_production/test-data.json`), as the schema is so far not documented and not stable. 
    * `instance`: instance specific data
    * `tests`: This steers the test behaviour. Only tests with `test` = `true` will be executed.
    * `dataverses`: Number of Dataverses, which will be tested in `test_dataverses.py`
    * `search`: List of search queries to be tested in `test_search.py`
    * `metadata-server`: List of metadata server resources to be tested
    * `external-resources`: External resources for test purposes.
    * `resources`: Collection of resources (URL's) to be tested in `test_resources.py`
  * `dataverses.json` (optional): 
    * List of Dataverses created via `utils` to test the completeness of the Dataverses.
  * `datasets.json` (optional): 
    * List of Datasets created via `utils` to test the completeness of the Datasets.
  * `datafiles.json` (optional): 
    * List of Datafiles created via `utils` to test the completeness of the Datafiles.
  * `metadata.json` (optional): 
    * Aggregated data from `dataverses.json`, `datasets.json` and `datafiles.json`.

### Utils

`utils/` contain helper scripts to create the needed data for the tests and use test data. CLI integration is done with [typer](https://typer.tiangolo.com/).

**Environment variables**

* `INSTANCE`: Dataverse instance to which the calls should be executed. There are three AUSSDA instances configured so far: `dataverse_production`, `dataverse_dv03` and `dataverse_localhost_t550`.

Set via `.env` files (so far placed in the repo root directory - will move later to private submodule):
* You can use `.env.sample` as a template
* `BASE_URL`: Base URL of the instance without trailing slash (e. g. `https://data.aussda.at`).
* `API_TOKEN`: API Token of a Dataverse user with proper rights.

**Collect**

Collects the complete data of a Dataverse instance in a tree structure with all containing Dataverses, Datasets and Datafiles. The generated `tree.json` file is stored inside `utils/` in the related instance folder.

```shell
python utils collect
```

**Generate**

Generates lists of Dataverses (`dataverses.json`), Datasets (`datasets.json`) and Datafiles (`datafiles.json`) from the tree structure (`tree.json`). The created lists are then used for tests (`test_all_dataverses()`, `test_all_datasets()`, `test_all_datafiles()`). The generated JSON files are stored inside `utils/` in the related instance folder.

```shell
python utils generate
```

**create-testdata**

Creates on your instance a pre-defined set of testdata. It uses the AUSSDA test data repository, which is so far private.

```shell
python utils create-testdata
```

**remove-testdata**

Removes all data created by `create-testdata`. It recursively collects all Dataverses and Datasets from a passed Dataverse down.

```shell
python utils remove-testdata
```

**Help**

To get all information for the CLI integration, use `python utils --help`. It lists all commands.

**Adapt utils to your own Dataverse instance**

To use the tests for your own Dataverse instance, you have to:
* Add for each instance an `.env` file with the needed environment variables inside (see above).
* Add another subclass of `Config` in `utils/config.py`, where you call your `.env` file. Add the Class to the `get_config()` function.
* Create for each instance a folder with prefix `dataverse_` inside `utils/data/instances/`, in which you then can add all needed files for your tests.
* Adapt `create-testdata.py` to use your own test data.

## Development

**Install**

Setup the virtual environment, install packages, install this package and install pre-commit.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements/development.txt
pip install -e .
pre-commit install
```

**Add browser engines**

To use selenium tests locally, you have to add the browserengines to `PATH`. Hint: the browserengine file must be executable!

```shell
export PATH=$PATH:/path/to/the/browserengine/
```

**Extend**

If you have added a test, fixed a bug or contributed in any other way to this, please don't forget to create a Pull Request, so we can collectively 

## Resources

* [pyDataverse](https://github.com/AUSSDA/pyDataverse)
* [AUSSDA test-data](https://github.com/AUSSDA/aussda_test-data)
