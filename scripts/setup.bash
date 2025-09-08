#!/bin/bash

# ROS sets PYTHONPATH which includes system packages
# in the virtual environment causing issues
unset PYTHONPATH

if [[ ! -d ".venv" ]]; then
    python3 -m venv .venv
fi

source .venv/bin/activate

# Upgrade pip
pip3 install --upgrade pip

# Install Requirements
pip3 install -r requirements.txt
