@echo off
cls
javac Advent*.java
java -Xmn1G Advent %*
del *.class
