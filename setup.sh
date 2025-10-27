#!/bin/sh

# Ensure pip is installed
python -m ensurepip --upgrade
python -m pip install --upgrade pip setuptools wheel

# Install requirements
python -m pip install -r requirements.txt
