# Dataverse Tests

Dataverse tests helps you to test the operational requirements of your [Dataverse](dataverse.org/) installation to maintane stability and low risk. It offers tests for integration, system and risk-based testing.

Tests are written in Python with pytest, requests and Selenium. They are easy to adapt and extend. They are Open Source and well documented. The tests do not contain common frontend or backend unit tests, which is part of Dataverse development.

In addition to the tests, `utils` helps you with your test preparation.

**Features**

Tests (`testing/`)

* Modular test architecture, optimized for use on Jenkins or similar build/testing tools
* Supports Firefox and Chrome
* Tests: Login (normal + Shibboleth), Data Completeness, Create Dataverse Frontend, Installation / Server, Search, OAI-PMH, Sitemap, robots.txt, Terms of Use
* Tested with Dataverse 4.18.1, 5.2, 5.6 and 5.7

Helper functions (`utils/`)

* CLI integration
* Collect (all) data of your installation: Dataverses, Datasets, Datafiles
* Upload defined set of testdata
* Remove (all) testdata
* Create users

General

* Settings management
* Flexible and easy to use for your own Dataverse instance
* Integration of [dataverse_testdata](https://github.com/AUSSDA/dataverse_testdata/)
* Integration of [dataverse-sample-data](https://github.com/IQSS/dataverse-sample-data/)
* Open Source (MIT)

**Use-Cases**

* Installation: Test a fresh, customized Dataverse installation
* Upgrade: Test configuration and data completeness after upgrade
* Monitoring: Frequent testing during operation

## Install

**Pre-requisites**

Python >= 3.6

Python packages:

* [pydantic](https://pydantic-docs.helpmanual.io/)
* [pyDataverse](https://github.com/gdcc/pyDataverse)
* [pytest-selenium](https://pytest-selenium.readthedocs.io/)
* [typer](https://typer.tiangolo.com/)

Browser engine(s) (optional for Selenium-based tests):

* Geckodriver (Firefox)
* Chromedriver

**Clone repository**

```shell
git clone https://github.com/gdcc/dataverse_tests.git
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

### 1. Set up .env-file

Before you can start with ether `testing` or `utils`, you have to configure the settings management. You need to create an `.env`-file for each Dataverse installation, and set the needed variables in it. Start by using the `env-config/example.env` template. The `.env` file filename is your central identifier for works done with your Dataverse installation and then later on used for other naming purposes, so use a descriptive one (e. g. `ORGANISATION_INSTALLATION.env` =>  `aussda_production.env`). Once setup, you have to set the `ENV_FILE` environment variable in your terminal to your absolute path of your `.env`-file.

Note: Environment variables set via command line will overwrite the ones defined in an `.env`-file.

Find the used environment variables documented in `src/dvtests/settings.py`.

## 2. Create user JSON**

For some tests and utils functions, you need at least one user who has proper rights to do API requests, create Datasets, to login or do other stuff. These user credentials are stored inside a JSON file under `user/`.

The user JSON file consists of user specific information to be used both for testing and utils functionality. We recommend to copy `user/example.json`, rename it after your instance (e. g. `aussda_production`) and add all your users with their credentials.

Beware: This file consist of secret, critical data and should not be versioned or shared with anybody.

### 3. Testing

**3.a. Find tests**

The tests can be found inside `src/dvtests/testing/`. They are seperated into:

* `default/`: basic tests applicable to a normal Dataverse installation with default cofiguration
* `custom/`: tests to verify installation specific customizations of a Dataverse installation

**3.b. Setup browser engines (only if Selenium tests are used)**

To run selenium tests, you have to have at least one browser engine running and be callable by [pytest-selenium](<https://pytest-selenium.readthedocs.io/>).

For this, set the `PATH` environment variable in the terminal. You have to add the directories for all the browserengines you want to use (e. g. geckodriver,  [chromedriver](https://chromedriver.chromium.org/)) to your path. Check out [pytest-selenium](https://pytest-selenium.readthedocs.io/en/latest/) for supported browserengines. Example: `export PATH=$PATH:/folder/to/your/browser/engine/`

Note: The browserengine file must be executable

**3.c. Create test configs**

A test normally works like this: You define the test input and the expected result and the test resolves to true if the actual result equals the expected one.

As the test input and expected results differ from installation to installation, you need to define them before you can execute the tests. These test-configs can be found in the `config/installations/` directory, inside a sub-directory named after your .env-file (e. g. `aussda_production/`). Inside this must be a directory named `testing/`, in which all the core tests are placed inside the `default/` folder. Example path: `configs/installations/aussda_production/testing/default/`.

Inside there, you then have to place for each test a config file. They all have the `test_` prefix and are written in JSON. If you want to find out how the configs work, you best check out first the tests and/or other test-configs.

Best Practice: Start by copying the `config/installations/aussda_production` folder, rename it to your .env-filename and adapt the test-configs to your own setup.

**3.d. Run test**

Tests are executed by [pytest](https://docs.pytest.org/en/stable/).

```
pytest -v src/dvtests/testing/default/test_api.py
```


If you want to use a Selenium frontend test, you have to pass the browserengine:

```
pytest -v --driver Firefox src/dvtests/testing/default/test_create-frontend_dataverse.py
```

We have defined several markers for the tests, which you can find out about in `setup.cfg`. Most markers tell you, if the test was already used with a specific  Dataverse version, or if it uses utils or selenium to run properly.

```shell
pytest -v -m "v5_6" src/dvtests/testing/default/test_shibboleth.py
```

**3.e. Optional: Adapt shibboleth login function**

As every Shibboleth login works differently, you have to adapt/overwrite `custom_shibboleth_institution_login` inside `src/dvtests/testing/conftest.py` to your own Shibboleth login procedure to use it.

**3.f. Optional: Collect data with utils to data completeness**

If you want to test the data completeness of your installation (e. g. after an upgrade or migration), you first need to collect the data from the existing/old Dataverse installation. Find out more at utils create-testdata.

### 4. Utils

Utils intends to offer helpful functions for your testing workflow - like collecting all data before an migration, uploading testdata for automated and/or manual testing or cleaning up after testing. These functions can be called by command line.

Note: Execute step 1. and 2. before you start using utils.

**Commands**

* `collect`
* `generate`
* `create-testdata`
* `remove-testdata`
* `create-user`

Find out more about the functionalities in the docstrings inside `src/dvtests/utils/__init__.py`.

Generally, you can call them like this

```shell
cd src/dvtests
python utils FUNCTION_NAME
```

#### 4.a. Create testdata

Create testdata uses a JSON file to know, which data should be created how, in which order and by whom.

**Call**

```shell
python src/dvtests create-testdata FILENAME
```

`FILENAME` is the path to the JSON file with the orders, e. g.:

```shell
python src/dvtests create-testdata configs/installations/localhost_docker/utils/create_testdata_01.json
```

**JSON format**

Actions are executed in sequential order.

* `action`: defines, which kind of action should be done (`create`,`publish`, `upload`)
* `user-handle`: defines by which user it should be done (user must be defined in users JSON)
* `parent-id`: id of the parent to wich the data should be attached
* `parent-type`: data type of the parent (`dataverse`,`dataset` or `datafile`)
* `metadata`: data related to the metadata
  * `update`: list of metadata attributes from the metadata file, which should be updated before further steps.

See how the named actions differ in detail:

Create Dataverse:

```json
{
  "data-type": "dataverse",
  "action": "create",
  "parent-id": ":root",
  "parent-type": "alias",
  "user-handle": "dataverseAdmin",
  "metadata": {
    "filename": "dataverse_testdata/metadata/json/dataverse/dataverse_upload_full_01.json",
    "update": {
      "alias": "test_create_testdata",
      "name": "Test Create Testdata"
    }
  }
},
```

Publish Dataverse:

```json
{
  "id": "test_create_testdata",
  "id-type": "alias",
  "data-type": "dataverse",
  "action": "publish",
  "user-handle": "dataverseAdmin"
},
```

Create Dataset:

```json
{
  "id": "harvard-open-source-1",
  "data-type": "dataset",
  "action": "create",
  "metadata": {
    "filename": "dataverse-sample-data/data/dataverses/open-source-at-harvard/dataverses/dataverse-project/datasets/dataverse-irc-metrics/dataverse-irc-metrics.json"
  },
  "parent-id": "dataverse-project",
  "parent-type": "alias",
  "user-handle": "dataverseAdmin"
},
```

Publish Dataset:

```json
{
  "id": "harvard-open-source-1",
  "id-type": "dvtests",
  "data-type": "dataset",
  "action": "publish",
  "release-type": "major",
  "user-handle": "dataverseAdmin"
},
```

Upload Datafile:

```json
{
  "data-type": "datafile",
  "action": "upload",
  "metadata": {
    "filename": "dataverse_testdata/metadata/json/datafile/datafile_upload_full_01.json"
  },
  "filename": "dataverse_testdata/files/dta/10002_da_de_v0_9.dta",
  "id-type": "dvtests",
  "parent-id": "harvard-open-source-1",
  "parent-type": "dataset",
  "user-handle": "dataverseAdmin",
  "update": {
    "filename": "10002_da_de_v0_9.dta"
  }
},
```

**Help**

To get all information for the CLI integration, add `--help`. It lists all commands.

**Best Practice**

We recommend using the JSON files `configs/installations/aussda_production/utils/` to find out how it works and adapt it to your needs.

## Roadmap

The next steps for the project are:

1. Get it used by the broader communiy
2. Add compatibility with missing Dataverse version
3. Extend existing tests
4. Add new tests

**Financial Sustainability**

As for now, there is no ongoing, steady funding available, so no actual developments are planned. If you have feature requests or other ideas or concerns regarding the future of dataverse_tests, please contact GDCC.

## Contributor Guide

See [CONTRIBUTING.rst](CONTRIBUTING.rst).

**Possible Contributions**

Please have a look at the [issues](https://github.com/gdcc/dataverse_tests/issues) to already submitted requests.

Helpful tests to be developed by the community could be:

* Verify Metadata of a Dataverse via API
* Create a Dataset via Frontend
* Verify Metadata of a Dataset via API
* Upload a Datafile via Frontend
* Verify Metadata of a Datafile via API
* Verify access of a Datafile

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

Copyright Stefan Kasberger, 2020-2022.

Distributed under the terms of the MIT license, Dataverse Tests is free and open source software.

Full License Text: [LICENSE.txt](LICENSE.txt)
