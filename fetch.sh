#!/bin/bash

function fetch() {
    day=$1
    day2="$(seq -f %02g $day $day)"
    year=$2
    curl -vv --create-dirs --header "Cookie: $(cat aoc.cookie)" "https://adventofcode.com/$year/day/$day/input" -o "$year/input/$day2.txt"
}

if [ $# -eq 0 ]; then
  fetch "$(date +%-d)" "$(date +%Y)"
else
  fetch "$1" "$2"
fi
