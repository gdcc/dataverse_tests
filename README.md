# AUSSDA Tests

Python Tests for Jenkins.

See internal: https://wiki.univie.ac.at/display/AUSSDA/Testing

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

* `BASE_URL`: Base URL of the Dataverse instance. Required for many Dataverse tests.
* `API_TOKEN`: API Token of a Dataverse user with proper rights.
* `HEADLESS`: `true` executes Selenium tests without browser window opening, `false` otherwise.
* `TEST_CONFIG`: `jenkins` is default and for use by calls from a jenkins instance, `development` for development purpose. So far, there is no difference in the settings between these two.

### Utils

The folder `utils/` contains helper scripts to create the needed data for the tests. These are implemented with [typer](https://typer.tiangolo.com/). 

**Collect**

Collects the complete data of a Dataverse instance in a tree structure with all containing Dataverse, Datasets and Datafiles. The generated `tree.json` file is stored inside the `utils/` folder.

```shell
python utils collect
```

**Generate**

Generates lists of Dataverse, Datasets and Datafiles from the tree structure. The lists are then used for tests (`test_all_dataverses()`, `test_all_datasets()`, `test_all_datafiles()`). The generated JSON files are stored inside the `utils/` folder.

```shell
python utils generate
```

**Help**

To get all information for the CLI integration, use `python utils --help`. It lists all commands.

## Development

**Install**

Setup the virtual environment, install packages, install this package and install pre-commit.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -e .
pre-commit install
```

**Setup**

Set the environment variables, as listed above.

```shell
export TEST_CONFIG="development"
```

**Add browser engines**

To use selenium tests locally, you have to add the browserengines to `PATH`. Hint: the browserengine file must be executable!

```shell
export PATH=$PATH:/path/to/the/browserengine/
```

## Resources

* [pyDataverse](https://github.com/AUSSDA/pyDataverse)
* [AUSSDA test-data](https://github.com/AUSSDA/aussda_test-data)
