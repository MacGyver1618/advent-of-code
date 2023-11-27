import java.util.*;
import java.util.stream.*;

public class Advent05 extends Advent {

  public Advent05() {
    super(5);
  }

  @Override
  protected void parseInput() {

  }

  @Override
  protected String part1() {
    String polymer = input.get(0);
    return "" + reducePolymer(polymer).length();
  }

  private String reducePolymer(String polymer) {
    while (true) {
      String newPolymer = react(polymer);
      if (newPolymer.length() == polymer.length())
        break;
      polymer = newPolymer;
    }
    return polymer;
  }

  private String react(String old) {
    char[] chars = old.toCharArray();
    StringBuffer sb = new StringBuffer();
    for (int i = 0; i < old.length(); i++) {
      if (i >= old.length()) break;
      if (i == old.length() - 1) {
        sb.append(chars[i]);
        break;
      }
      char current = chars[i];
      char next = chars[i+1];
      if (canRemove(current, next)) {
        i++;
        continue;
      }
      sb.append(current);
    }
    return sb.toString();
  }

  private boolean canRemove(char a, char b) {
    return a != b && Character.toUpperCase(a) == Character.toUpperCase(b);
  }

  @Override
  protected String part2() {
    String polymer = input.get(0);
    int shortest = Integer.MAX_VALUE;
    for (char c = 'a'; c <= 'z'; c++) {
      String attempt = trimPolymer(polymer, c);
      String result = reducePolymer(attempt);
      if (result.length() < shortest) {
        shortest = result.length();
      }
    }
    return "" + shortest;
  }

  private String trimPolymer(String polymer, char c) {
    StringBuffer sb = new StringBuffer();
    c = Character.toUpperCase(c);
    for (char x : polymer.toCharArray()) {
      if (Character.toUpperCase(x) != c) {
        sb.append(x);
      }
    }
    return sb.toString();
  }
}
