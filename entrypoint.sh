#!/usr/bin/env bash

echo "...updating repository ..."
pwd
git reset --hard HEAD
git clean -f
git pull

echo "...evaluation launch_script..."

if [ $# -eq 0 ]
  then
    source run_evaluation.sh
else
    source run_evaluation.sh "$@"
fi