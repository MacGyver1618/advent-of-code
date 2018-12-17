import java.util.*;
import java.util.stream.*;

public class Advent02 extends Advent {

  public Advent02() {
    super(2);
  }

  @Override
  protected void parseInput() {}

  @Override
  protected String part1() {
    return "" + countN(2)*countN(3);
  }

  private long countN(int n) {
    return input.stream()
                .map(Advent::charFreqs)
                .filter(m -> m.containsValue(n))
                .count();
  }

  @Override
  protected String part2() {
    for (String line : input) {
      String match = countD1(line);
      if (match != null) {
        return findCommon(line, match);
      }
    }
    return "There was no match";
  }

  private String countD1(String s1) {
    return input.stream()
                .filter(s2 -> hammingDistance(s1, s2) == 1)
                .findFirst()
                .orElse(null);
  }

  private int hammingDistance(String s1, String s2) {
    int distance = 0;
    for (int i = 0; i < s1.length(); i++) {
      if (s1.charAt(i) != s2.charAt(i))
        distance++;
    }
    return distance;
  }

  private String findCommon(String s1, String s2) {
    StringBuilder result = new StringBuilder();
    for (int i = 0; i < s1.length(); i++) {
      if (s1.charAt(i) == s2.charAt(i)) {
        result.append(s1.charAt(i));
      }
    }
    return result.toString();
  }
}
