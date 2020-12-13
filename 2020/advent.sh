#!/usr/bin/env bash
clear
cd java
javac Advent*.java
java -Xmn1G Advent $*
rm *.class
