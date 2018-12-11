# Advent of Code 2018

These are my solutions for AoC 2018, done in Java on Windows.

## Scaffolding

The entrypoint is `advent.bat`. It takes 0..n arguments, each of which corresponds
to a day. It then compiles and runs all of the specified days, or all in the
range 1..25, if the argument list is empty.

## Utility functions

These are mainly used for debugging purposes. Most of them are just less verbose
shorthands for Java standard library methods.

*`sop(Object...)`* prints out all the arguments to System.out.

*`sopl()`* prints a line change to System.out.

*`sopl(Object...)`* prints out all the arguments to System.out, followed by a newline.

*`pause()`* waits for user input, and throws it away. Handy for examining what's
happening inside a loop.

*`readString()`* does exactly what you'd expect.

*`readInt()`* does the same as above, but parses it into an int.

There's other stuff there, but this is most of what I actually use.
