#!/bin/bash

SCRIPT=$1
PARAMS=$2

if [ -z "$SCRIPT" ] || [ -z "$PARAMS" ]; then
    echo "Usage: ./run.sh <script_name> <params>"
    exit 1
fi

docker exec -it my_python_app python main.py "$SCRIPT" "$PARAMS"
