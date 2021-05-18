# Dataverse Tests

Dataverse tests for operation of your Dataverse installation. It focuses on Dataverses most important functionality for it's operation on your institution (e. g. settings, customizations, endpoints, login and other critical core functionalities) - to test Dataverse after a fresh installation, an upgrade or for frequent checks during runtime. The tests do not contain common frontend or backend tests, which is part of Dataverse development.

Tests are written in Python with Pytest, Requests and Selenium. They are easy to adapt and extend - and Open Source.

In addition to the tests, `utils` helps you with your test preparation. It makes collection, creation and removal of data and users easy.

**Features**

* Tests (`testing`)
  * flexibility through XPATH
  * Modular test architecture, optimized for use on Jenkins or similar build/testing tools
  * Supports Firefox and Chrome
  * Tests: Login (normal + Shibboleth), Data Completeness, Create Dataverse Frontend, Installation / Server, Search, OAI PMH, Sitemap, robots.txt,
  * tested on a Dataverse 4.20 installation
* Helper functions (`utils`)
  * Collect (all) data of your installation: Dataverses, Datasets, Datafiles
  * Upload testdata
  * Remove testdata
  * Create users
  * CLI integration
* Settings management
* Flexible and easy to use for your own Dataverse instance
* Open Source (MIT)

**Use-Cases**

* Installation: Test fresh, customized installation after setup
* Upgrade: Test configuration and data completeness after upgrade
* Monitoring: Frequent testing during operation

**Roadmap**

* Add tests
  * Verify Metadata of a Dataverse
  * Create a Dataset via Frontend
  * Verify Metadata of a Dataset
  * Upload a Datafile via Frontend
  * Verify Metadata of a Datafile
* Add new Dataverse version: add/update tests to work with as many as possible Dataverse versions.
* Transfer repository to GDCC
* Release 0.1.0
* Get people involved
  * Test on your own Dataverse installations
  * Create issues
  * Create pull requests

## Install

**Pre-requisites**

Python >= 3.6

Python packages:

* [pydantic](https://pydantic-docs.helpmanual.io/)
* [pyDataverse](https://github.com/gdcc/pyDataverse)
* [pytest-selenium](https://pytest-selenium.readthedocs.io/)
* [typer](https://typer.tiangolo.com/)

Browser engine(s) (optional for selenium tests):

* Chromedriver
* Geckodriver (Firefox)

**Clone repository**

```shell
git clone https://github.com/AUSSDA/dataverse_tests.git
cd dataverse_tests/
```

**Install requirements**

```bash
pipenv install
```

**Activate virtual environment**


```shell
pipenv shell
```

## Basic Usage

### Settings Management

Before you can start with ether `testing` or `utils`, you have to configure the settings management. Create an `.env`-file for each Dataverse installation, and set all your variables inside it. Use `env-config/example.env` as a template. The `.env` file filename is then used for the Dataverse installation, so use a descriptive one (`ORGANISATION_INSTALLATION.env`, e. g. `aussda_production.env`). You can then define the absolute path to your `.env`-file as `ENV_FILE` environment variable in your terminal.

Environment variables set via command line will overwrite the ones defined in the `.env`-file.

Find the used environment variables documented in `src/dvtests/settings.py`.

### Tests

**Find tests**

The tests can be found inside `src/dvtests/testing/`. They are seperated into:

* `default/`: basic tests applicable to a clean, fresh Dataverse installation with default cofiguration (deliverd as by IQSS)
* `custom/`: tests to verify installation specific customizations of a Dataverse installation

Both consist of:

* `unit/`: unit tests
* `system/`: system tests

**Setup browser engines**

For this, we forward to you the documentation of:

* [pytest-selenium](https://pytest-selenium.readthedocs.io/)
* [chromedriver](https://chromedriver.chromium.org/)
* [selenium-python](https://selenium-python.readthedocs.io/)

To run selenium tests, you have to have at least one browser engine running and be callable by `pytest-selenium`.

**Set Environment variables**

Set these environment variables in the terminal:

* `ENV_FILE`: see "Settings Management"
* `PATH`: You have to add the directories for all the browserengines you want to use (e. g. geckodriver, chromedriver) in the selenium tests to your path. Check out [pytest-selenium](https://pytest-selenium.readthedocs.io/en/latest/) for supported browserengines.
  * The browserengine file must be executable
  * E. g. `export PATH=$PATH:/folder/to/your/browser/engine/`

**Create test configs**

For most tests, aspecific test configuration is needed, which is automatically loaded in the tests from pre-defined JSON files located inside the directories in `config/INSTANCE/testing/`, with the prefix `test-config_`. The directory structure is the same as from the tests and must be used for the auto-loading to work.

Inside the `config/INSTANCE/testing/` directories, there are also files with the prefix `installation-config_`, which define general installation-specific configurations, like the list of used XPATH's to create a Dataverse via the frontend.

We recommend copying `config/aussda_production/testing/` and adaping the content to your needs to start testing your own installation.

**Create user JSON file**

The user JSON file consists of user specific information to be used both for testing and utils functionality. We recommend to copy `user/example.json`, rename it after your instance (e. g. `aussda_production`) and add all your users with their credentials.

Beware: This file consist of secret, critical data and should not be versioned or shared with anybody.

**Optional: Adapt shibboleth login function**

If you want to use Shibboleth login, you have to adapt or overwrite `custom_shibboleth_institution_login` inside `src/dvtests/testing/conftest.py` to your own Shibboleth login procedure.

**Optional: Collect data with utils**

If you want to use the utils

**Run test**

Tests are executed with pytest:

Example:

```shell
pytest -v tests/dataverse/test_api.py
```

You always have to pass the browserengine use to pytest.

```shell
pytest -v --driver Firefox src/dvtests/testing/default/unit/test_api.py
```

We have defined several markers inside `setup.cfg`, which helps to select tests.

```shell
pytest -v -m "v4_20 and not utils" src/dvtests/testing/default/system/test_dataverses.py
```

### Utils

Utils intends to offer helpful functions to prepare or clean up testing activities - like collecting data, uploading test data or removing test data after testing. The functions can be called via command line.

**Environment variables**

Set via command line:

* `ENV_FILE`: see "Settings Management"

**Prepare**

* Create for each instance an `.env`-file (see "Settings Management").

#### Commands

Find out more about the functionalities in the docstrings inside `src/dvtests/utils/__init__.py`.

You can call the functions by

```shell
cd src/dvtests
python utils FUNCTION_NAME
```

Functions:

* `collect`
* `generate`
* `create-testdata`
* `remove-testdata`
* `create-user`

**Create testdata**

Create testdata uses a config JSON file to know, which data should be created how and by whom.

We recommend using the JSON files `configs/aussda_production/` with the prefix `create_testdata_` to find out how it works.

**Help**

To get all information for the CLI integration, add `--help`. It lists all commands.

## Contributor Guide

See [CONTRIBUTING.rst](CONTRIBUTING.rst).

## Resources

* [pyDataverse](https://github.com/gdcc/pyDataverse)
* Testdata
  * [Dataverse Testdata @ AUSSDA](https://github.com/AUSSDA/dataverse_testdata)
  * [Dataverse Sample Data @ IQSS](https://github.com/IQSS/dataverse-sample-data)

## Thanks

To everyone who has contributed to this project - with an idea, an issue, a pull request, developing an application, sharing it with others or by any other means: **Thank you for your support!**

Open Source projects live from the cooperation of the many and Dataverse Tests is no exception to that, so to say thank you is the least that can be done.

Special thanks to all Slava Tykhonov from DANS and all the people who do an amazing job by developing Dataverse at IQSS.

Dataverse Tests is funded by [AUSSDA - The Austrian Social Science Data Archive](https://aussda.at/) and through the EU Horizon2020 programme [SSHOC - Social Sciences & Humanities Open Cloud (T5.2)](https://www.sshopencloud.eu/about-sshoc).

## License

Copyright Stefan Kasberger, 2020-2021.

Distributed under the terms of the MIT license, Dataverse Tests is free and open source software.

Full License Text: [LICENSE.txt](LICENSE.txt)
