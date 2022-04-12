#!/bin/bash
pip3 install virtualenv
python3 -m venv venv
source venv/bin/activate

python3 -m pip install --upgrade
pip3 install pre-commit mypy flake8 autoflake
pre-commit install
pip3 install -r requirements.txt
