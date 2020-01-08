#!/usr/bin/env bash

export PYTHONPATH=$PYTHONPATH:$(pwd)/src:$(pwd)/evaluation

echo "...evaluation launch_script..."

if [ $# -eq 0 ]
  then
    source run_evaluation.sh
else
    source run_evaluation.sh "$@"
fi