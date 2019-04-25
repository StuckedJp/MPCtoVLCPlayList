#! /bin/bash

PYTHON_VENV_NAME=Mpc2Vlc
PYTHON_VERSION=3.7.3

pyenv virtualenvs | grep $PYTHON_VENV_NAME > /dev/null
found=$?

if [ $found -ne 0 ]; then
    pyenv virtualenv $PYTHON_VERSION $PYTHON_VENV_NAME
fi

pyenv activate $PYTHON_VENV_NAME
