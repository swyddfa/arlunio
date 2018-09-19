#!/bin/bash
set -e

echo "==> Checking if you have a compatible version of python installed."
ver=$(python scripts/version_check.py)

if [ $? -gt 0 ]; then
    echo -e "\nERROR! You must have Python installed with version >= 3.6"
    exit 2
fi

echo -e "    Found Python v$ver.\n"

sed -i.bk "s/VERSION/$ver/" .pre-commit-config.yaml

echo -e "==> Checking if you have pipenv installed"
which pipenv > /dev/null 2> /dev/null

if [ $? -eq 0 ]; then
    echo -e "    Ok.\n"
else
    echo -e "    pipenv not found: checking for pip..."
    which pip 2> /dev/null > /dev/null

    if [ $? -eq 0 ]; then
        echo -e "    pip found: installing pipenv"
        pip install --user pipenv
    else
        echo -e "    ERROR! pip not found. Please install pip and rerun this script."
        exit 2
    fi
fi

echo "==> Creating virtual environment and installing dependencies"
echo -e "    This can take a few minutes.\n"

pipenv install --dev

echo -e "\n==> Setting up pre commit hooks.\n"
pipenv run pre-commit install

echo -e "\n\n==> Running a few tests and building the documentation"
echo -e "    This can take a few minutes\n"
pipenv run tox -e docs-build

echo -e "\n\n\n==> All done! Thank you for taking the time to contribute! :)"
