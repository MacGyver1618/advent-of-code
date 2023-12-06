#!/usr/bin/env bash
export PYTHONPATH=$PYTHONPATH:`pwd`
year="$1"
day="$2"
cd "$year/python"
python3 "advent_$(seq -f %02g $day $day).py"
