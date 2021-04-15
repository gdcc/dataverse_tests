import re

import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


def find_version(*file_paths):
    """Find package version from file."""
    with open("src/dvtests/__init__.py", "r", encoding="utf-8") as fh:
        version_file = fh.read()
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M,
    )
    if version_match:
        return version_match.group(1)

    raise RuntimeError("Unable to find version string.")


INSTALL_REQUIREMENTS = [
    # A string or list of strings specifying what other distributions need to
    # be installed when this one is.
    "pytest==6.1.2",
    "selenium==3.141.0",
    "requests==2.25.0",
    "pydantic[dotenv]==1.7.2",
    "typer==0.3.2",
    "pyDataverse==0.3.1",
]

setuptools.setup(
    name="dvtests",  # Replace with your own username
    version=find_version("src", "dataverse_tests", "__init__.py"),
    author="Stefan Kasberger",
    author_email="stefan.kasberger@univie.ac.at",
    description="Dataverse tests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AUSSDA/dataverse_tests",
    project_urls={
        "Issue Tracker": "https://github.com/AUSSDA/dataverse_tests/issues",
        "Changelog": "https://github.com/AUSSDA/dataverse_tests/CHANGELOG.rst",
        "Source": "https://github.com/AUSSDA/dataverse_tests/",
    },
    classifiers=[
        # How mature is this project? Common values are
        #   2 - Pre-Alpha
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Natural Language :: English",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    keywords=["dataverse", "testing", "selenium", "pyDataverse"],
    install_requires=INSTALL_REQUIREMENTS,
    # entry_points = {
    #     'console_scripts': ['utils=dvtests.utils:main'],
    # }
)
