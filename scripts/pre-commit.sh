#!/bin/bash

# A precommit hook that runs the black code formatter on the codebase
pipenv run black stylo
pipenv run black tests