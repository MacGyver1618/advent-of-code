#!/bin/bash
cd python
python3 "advent_$(seq -f %02g $1 $1).py"
