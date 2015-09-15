#!/bin/bash
if [ ! -d venv ]; then
    virtualenv .venv
fi
alias activate=". .venv/bin/activate"
activate && pip install -r 'requirements.txt'
