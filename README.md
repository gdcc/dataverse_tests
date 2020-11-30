# AUSSDA Tests

Python Tests for Jenkins to test different Dataverse instances, plus our website. Tests are written with pytest and Selenium - easy to adapt and extend, and Open Source.

**Features**

* Basic tests for Dataverse (mostly Selenium)
* `utils` functions to help you with creating needed data for the tests
  * create and remove testdata via API
  * collect all Dataverses, Datasets and Datafiles via API and store the response in JSON files to test the completeness of your data
  * CLI integration
* flexible and easy to use for your own Dataverse instance
* easy to add new tests
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
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

### Tests

The tests focus on requirements for DevOps activitites on running instances. This includes customizuations (header, homepage, footer), user activitites (login, register, logout), datacreation via Frontend and API, data integrity (all Dataverses, Datasets and Datafiles accessible), SEO (sitemap, robots.txt) and legal issues (Privacy Policy, Cookie Rollbar). They are not planned to contain classic frontend or backend testing, which is done by the developers, and we rely upon.

The folder `tests/` contains all the tests. They are seperated into `dataverse/` and `website/`.

Tests are executed with pytest:

```shell
pytest -v
```

**Environment variables**

Set via Bash:
* `INSTANCE`: Dataverse instance to be tested. There are three AUSSDA instances used and configured so far: `dataverse_production`, `dataverse_dv03` and `dataverse_localhost_t550`.
* `PATH`: You have to add the directories of your browserengines used (e. g. firefox gecko, chrome) to your path.
  * e. g. `export PATH=$PATH:/folder/to/your/browser/engine/`
  * Hint: the browserengine file must be executable!

Set via `.env`-files inside `env-config/`:
* `HEADLESS`: Executes Selenium tests with or without browser window opening ( default = `true` -> without browser window).
* `TEST_USER_NORMAL`: Username for normal login.
* `TEST_USER_NORMAL_NAME`: Real name of user normal login.
* `TEST_USER_NORMAL_PWD`: Password of user normal login.

### Utils

The utils intend to offer helpful functions to prepare tests - like creating needed data and uploading/removing test data. The functions can be called via command line. CLI integration is done with [typer](https://typer.tiangolo.com/).

**Environment variables**

Set via Bash:
* `INSTANCE`: Dataverse instance to which the calls should be executed. There are three AUSSDA instances configured so far: `dataverse_production`, `dataverse_dv03` and `dataverse_localhost_t550`.

Set via `.env` files (so far placed in the repo root directory - will move later to private submodule):
* You can use `.env.sample` as a template
* `BASE_URL`: Base URL of the instance without trailing slash (e. g. `https://data.aussda.at`).
* `API_TOKEN`: API Token of a Dataverse user with proper rights.

#### Commands

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

## Adapt to your own Dataverse instance

Some requirements to use all the functionality available need additional resources. Here is a short guide, how to adapt the repository, so you can use it for your own Dataverse instance(s).

**Environment Variables**

Both, the tests and the utils functions need environment variables to be run. We use `.env`-files for this, which are loaded by the `config.py` modules inside `utils/` and `tests/`.

To adapt the `.env`-files:

* copy the `.env.sample` file, name it after your instance (e. g. `.env.dataverse_production`) and place it inside `env-config/` (create it in the root directory if not already done).
* add your own credentials
* add an own config class in the respective `config.py` to load the `.env`-file
* add the class to `get_config()`
* load the settings in your modules. :)

**Utils**

* Add for each instance an `.env`-file (see above).
* test data:
  * to use `python utils create-testdata`, you have to provide metadata and/or data for the upload of Dataverses, Datasets and Datafiles via the API.
  * So far the AUSSDA test data repository, used by default in the scripts, are not public.
  * to setup your own test data directory:
    * define your own test data needed (files and metadata for Dataverses, Datasets and Datafiles)
    * adapt `create_testdata()` to your own test data setup
    * adapt `remove_testdata()` to your own test data setup

**Tests**

To use the tests for your own Dataverse instance, you have to:
* Add for each instance an `.env`-file (see above).
* Create for each instance a folder inside `tests/data/instances/` with `dataverse_` as prefix. In there should all the needed data be stored:
  * `test-data.json` (required):
    * Needed data for test execution of one Dataverse instance.
    * We recommend copying an existing one from AUSSDA and adapt it to your needs (e. g. `tests/data/instances/dataverse_production/test-data.json`). Beware: The schema for `test-data.json` is under development and so far not documented and not stable.
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
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements/development.txt
pip install -e .
pre-commit install
```

**Extend**

If you have added a test, fixed a bug, improved the documentation or contributed in any other way to this, please don't forget to create a Pull Request, so the work can be shared with the rest of the Dataverse community. Thank you!

* Add tests: simply add a pytest function, class or module to the existing structure inside `tests/`.
* Add test data: tell us, if you have publicly available test data!

## Resources

* [pyDataverse](https://github.com/AUSSDA/pyDataverse)
* [AUSSDA test-data](https://github.com/AUSSDA/aussda_test-data)
