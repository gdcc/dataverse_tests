# AUSSDA Tests

Python Tests for Jenkins to test different Dataverse instances, plus our website. Tests are written with pytest and Selenium - easy to adapt and extend, and Open Source.

**Features**

* Basic tests for Dataverse (mostly Selenium)
  * Supports Firefox and Chrome
  * easy to add new tests
* `utils` functions to help you with creating needed data for the tests
  * create and remove testdata via API
  * collect all Dataverses, Datasets and Datafiles via API and store the response in JSON files to test the completeness of your data
  * CLI integration
* flexible and easy to use for your own Dataverse instance
* Open Source (MIT)

## Install

**Pre-requisites**

Python >= 3.6

Python modules (see `requirements.txt`):

* [pyDataverse](https://github.com/AUSSDA/pyDataverse) ([#3b040ff23b665ec2650bebcf4bd5478de6881af0](https://github.com/AUSSDA/pyDataverse/commit/3b040ff23b665ec2650bebcf4bd5478de6881af0))
* [pytest](https://docs.pytest.org/en/stable/)
* [selenium](https://selenium-python.readthedocs.io/)
* [pydantic](https://pydantic-docs.helpmanual.io/)

Additional data:

Some modules use data, which are and/or can not be provided by this repository. To see how to adapt the repository to your own Dataverse instance, see below.


**Clone repository**

```shell
git clone https://github.com/AUSSDA/aussda_tests.git
cd aussda_tests/
```

**Install requirements**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

### Settings management

Before you can start, you have to decide how you want to manage the settings. We recommend to create an `.env`-file, and set all your variables inside it. Use `sample.env` as a template. You can then define the path to your `.env`-file via `ENV_FILE`. We recommend to use the absolute path, so the pytest calls are independent of your actual working directory you are in. When you don't define `ENV_FILE`, the configuration loading expects an `.env`-file in the root directory.

Environment variables set via command line will overwrite the ones defined in the `.env`-file.

You can find all possible settings listed up in `config.py`.

### Tests

The tests focus on requirements for DevOps activitites on running Dataverse instances. This includes customizuations (header, homepage, footer), user activitites (login, register, logout), datacreation via Frontend and API, data integrity (all Dataverses, Datasets and Datafiles accessible), SEO (sitemap, robots.txt) and legal issues (Privacy Policy, Cookie Rollbar). They are not planned to contain classic frontend or backend testing, which is done by the developers, and we rely upon.

The folder `tests/` contains all the tests. They are seperated into `dataverse/` and `website/`.

Tests are executed with pytest:

```shell
pytest -v tests/dataverse/test_api.py
```

Tests will always be collected, but depending on your `test-config.json` settings, the ones where `test` = `false` will be skipped and marked as this in the pytest results.

**Environment variables**

Set via command line:
* `ENV_FILE`: see above
* `PATH`: You have to add the directories for all your browserengines (e. g. firefox gecko, chrome) to your path.
  * e. g. `export PATH=$PATH:/folder/to/your/browser/engine/`
  * Hint: the browserengine file must be executable!

Set via `.env`-file:
* `INSTANCE`: Descriptive name for your instance to be tested. This must be also the folder name, where your test data is stored in (e. g. `dataverse_production`). There are three AUSSDA instances used and configured so far, as you can see in `tests/data/instances/`: `dataverse_production`, `dataverse_dv03` and `dataverse_localhost_t550` for Dataverse, and `website` as our website.
* `USER_AGENT`: Sets a user-agent. This allows to exclude http requests done by the tests tracked by your web-analytics tool (e. g. Matomo, Google Analytics). To work, you have to tell your web-analytics tool to exlude all visits with the defined user-agent string (e. g. `SELENIUM-TEST`).
* `HEADLESS`: Executes Selenium tests with or without browser window opening ( default = `true` -> without browser window).
* `TEST_USER_NORMAL`: Username for normal login.
* `TEST_USER_NORMAL_NAME`: Real name of user normal login.
* `TEST_USER_NORMAL_PWD`: Password of user normal login.
* `BROWSER`: valid JSON str of a list of browser engine names. Available: `firefox` and `chrome`.

### Utils

The utils intend to offer helpful functions to prepare tests - like preparing data or uploading/removing test data. The functions can be called via command line.

**Environment variables**

Set via command line:
* `ENV_FILE`: see above

Set via `.env`-file:
* `INSTANCE`: Descriptive name for your instance to be tested. This must be also a valid folder name, as your generated data will be stored in a sub-directory called as it inside `utils/data/instances/` (e. g. `utils/data/instances/dataverse_production`).
* `BASE_URL`: Base URL of the instance without trailing slash (e. g. `https://data.aussda.at`).
* `API_TOKEN`: API Token of a Dataverse user with proper rights.
* `PRODUCTION`: If `true`, the creation and removal of test-data is not activated. This is important to set to `true`, if this represents a production instance, as you don't want to create or delete data on production. If you are To allow creation or removal on a production instance, you have to pass `--force` to the function call.

#### Commands

**Collect**

Collects the complete data of a Dataverse instance in a tree structure (`tree.json`), containing all Dataverses, Datasets and Datafiles. The file is stored in your instance directory (e. g. `utils/data/instances/dataverse_production`).

```shell
python utils collect
```

**Generate**

Generates lists of Dataverses (`dataverses.json`), Datasets (`datasets.json`) and Datafiles (`datafiles.json`) from the tree structure (`tree.json`). The created lists are then used for tests (`test_all_dataverses()`, `test_all_datasets()`, `test_all_datafiles()`). The generated JSON files are stored inside `utils/` in the related instance folder.

```shell
python utils generate
```

**create-testdata**

Creates a pre-defined set of testdata on your instance. By default, the function uses the AUSSDA test data repository, which is so far not publicly available. If `PRODUCTION` is `true`, this function will not execute, as long as you not add `--force` to the function call. This is to protect from unwanted changes on a production instance.

```shell
python utils create-testdata
```

**remove-testdata**

Removes all data created by `create-testdata`. It recursively collects all Dataverses and Datasets from a passed Dataverse down (by default = `science`). If `PRODUCTION` is `true`, this function will not execute, as long as you not add `--force` to the function call. This is to protect from unwanted changes on a production instance.

```shell
python utils remove-testdata
```

**Help**

To get all information for the CLI integration, use `python utils --help`. It lists all commands.

## Adapt setup for your own Dataverse instance

Some requirements to use all the functionality available need additional resources not present in the repository. Here is a short guide, how to adapt the setup, so you can use it for your own instance(s).

**1. Environment variables**

* Create for each instance an `.env`-file (see above).

**2a. Utils**

* Create for each instance an `.env`-file (see above).
* create test data:
  * To use `python utils create-testdata` to upload a set of data to your Dataverse instance, you have to provide metadata and/or data for the upload of Dataverses, Datasets and Datafiles via the API.
  * So far the AUSSDA test data repository, used by default in the scripts, are not public.
  * To setup your own test data directory:
    * Define your own test data needed (files and metadata for Dataverses, Datasets and Datafiles)
    * Adapt `create_testdata()` so your own metadata and datafiles are loaded
    * Adapt `remove_testdata()` so the data created by `create_testdata()` on your Dataverse instance will be deleted.

**2b. Tests**

To use the tests for your own Dataverse instance, you have to:
* Create for each instance an `.env`-file (see above).
* Create for each instance a folder inside `tests/data/instances/` with `dataverse_` as prefix. The folder name must later be used for `INSTANCE`.
* Store all the needed data in it:
  * `test-config.json` (required):
    * Consist of test configuration for one Dataverse instance.
    * We recommend copying `tests/data/instances/dataverse_production/test-config.json` from the AUSSDA production instance and adapt it to your needs. Info: The schema for `test-config.json` is under development and so far not documented and not stable.
    * `instance`: instance specific data
    * `tests`: This steers the test behaviour. Only tests with `test` = `true` will be executed.
    * `dataverses`: Number of Dataverses, which will be tested in `test_dataverses.py`
    * `search`: List of search queries to be tested in `test_search.py`
    * `metadata-server`: List of metadata server resources to be tested
    * `external-resources`: External resources for test purposes.
    * `resources`: Collection of resources (URL's) to be tested in `test_resources.py`
  * `dataverses.json` (optional):
    * List of Dataverses created via `python utils generate` to test the completeness of the Dataverses.
  * `datasets.json` (optional):
    * List of Datasets created via `python utils generate` to test the completeness of the Datasets.
  * `datafiles.json` (optional):
    * List of Datafiles created via `python utils generate` to test the completeness of the Datafiles.
  * `metadata.json` (optional):
    * Aggregated data from `dataverses.json`, `datasets.json` and `datafiles.json`, created by `python utils generate`.
* Execute the tests as shown above.

## Development

**Install**

Setup the virtual environment, install packages, install this package and install pre-commit.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
pre-commit install
```

**Extend**

If you have added a test, fixed a bug, improved the documentation or contributed in any other way to this, please don't forget to create a Pull Request, so the work can be shared with the rest of the Dataverse community. Thank you!

* Add tests: simply add a pytest function, class or module to the existing structure inside `tests/`.
* Add test data: tell us, if you have publicly available test data. We at AUSSDA will try to make our own test data public as soon as possible.

## Resources

* [pyDataverse](https://github.com/AUSSDA/pyDataverse)
* [AUSSDA test-data](https://github.com/AUSSDA/aussda_test-data)
