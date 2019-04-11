import java.util.*;
import java.util.stream.*;

public class Advent09 extends Advent {

  String stream;
  int curDepth = 0;
  int groups = 0;
  int points = 0;
  int garbageChars = 0;
  boolean garbage;

  public Advent09() {
    super(9);
  }

  @Override
  protected void parseInput() {
    stream = input.get(0);
  }

  @Override
  protected String part1() {
    char[] chars = stream.toCharArray();
    char c;
    for (int i = 0; i < chars.length; i++) {
      c = chars[i];
      if (c == '!') {
        i++;
        continue;
      }
      if (garbage) {
        if (c == '>') {
          garbage = false;
          continue;
        }
        garbageChars++;
        continue;
      }
      switch (c) {
        case '{':
          curDepth++;
          groups++;
          continue;
        case '}':
          points += curDepth;
          curDepth--;
          continue;
        case '<':
          garbage = true;
          continue;
      }
    }
    return "" + points;
  }

  @Override
  protected String part2() {
    return "" + garbageChars;
  }
}
