#!/bin/bash
if [ $# -eq 0 ]; then
  curl -s --header "Cookie: $(cat aoc.cookie)" "https://adventofcode.com/2019/day/$(date +%-d)/input" > "input/$(date +%d).txt"
else
  for day in $* 
  do
    curl -s --header "Cookie: $(cat aoc.cookie)" "https://adventofcode.com/2019/day/$day/input" > "input/$(seq -f %02g $day $day).txt"
  done
fi
