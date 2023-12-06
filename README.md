# Advent of Code

I started this repo in 2018. I started Advent of Code in 2015 when it first launched,
but put my solutions online only in 2018. I did Java only 2015-2017, and in 2018 I started 
doing Python and Clojure alongside Java. I switched to fully Python in 2020. I started 
redoing years 2015-2019 in Python at the same time.

## Scaffolding

I primarily run these in IntelliJ IDEA, but there's a shell script `fetch.sh` that fetches
the input using the syntax `./fetch.sh <year> <day>`. It requires the session cookie stored
in the root directory as `aoc.cookie`.

## Utility functions

### Python

Some of the stuff is based on Python 3.7 so e.g. `advent_lib.product` is redundant
as `math.prod` replaced it, but I haven't gotten around to removing the old stuff. 

*`read_lines(day_number)`* does pretty much what you'd expect, reads the input file
and tokenizes it to lines separated by `\n`. If the day is unlocked but the file is 
absent, it delegates to `fetch.sh` to get the input.

Other useful ones like general-purpose search algorithms `bfs`, `dfs`, `dijkstra`,
`a_star`. These can be used in conjuction with `adjacent` and `adjacent_diag` that
generate grid-based neighbors using NumPy.

For computationally intensive problems there are `ProgressBar` and `Spinner` that 
indicate whether something is happening while you're waiting for the program to 
complete.

### Java

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
