#!/bin/bash
if [ $# -eq 0 ]; then
  curl -s --create-dirs --header "Cookie: $(cat aoc.cookie)" "https://adventofcode.com/2019/day/$(date +%-d)/input" -o "input/$(date +%d).txt"
else
  for day in $* 
  do
    curl -s --create-dirs --header "Cookie: $(cat aoc.cookie)" "https://adventofcode.com/2019/day/$day/input" -o "input/$(seq -f %02g $day $day).txt"
  done
fi
