#!/bin/bash

function fetch() {
    day=$1
    day2="$(seq -f %02g $day $day)"
    year=$2
    curl -s --create-dirs --header "Cookie: $(cat aoc.cookie)" "https://adventofcode.com/$year/day/$day/input" | tee "$year/input/$day2.txt"
}

if [ $# -eq 0 ]; then
  fetch "$(date +%-d)" "$(date +%Y)"
else
  year="$1"
  shift
  for day in $*
  do
    fetch "$day" "$year"
  done
fi
