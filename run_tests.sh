#!/bin/sh

pychess_UNITTEST=true PYTHONPATH=lib python3 -m unittest discover -s testing -p "*.py" -v
