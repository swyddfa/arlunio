#!/bin/bash

echo -e "==> Creating virtual environment and installing dependencies\n"
pipenv install --dev

echo -e "\n\n==> Running a few tests and building the documentation"
echo -e "    This can take a few minutes\n"
pipenv run tox -e docs-build
