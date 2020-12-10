import java.util.*;
import java.util.regex.Pattern;
import java.util.stream.*;

public class Advent02 extends Advent {

  public static final String REGEX = "(\\d+)-(\\d+) (.): (.+)";

  public Advent02() {
    super(2);
  }

  @Override
  protected void parseInput() {

  }

  @Override
  protected Object part1() {
    return "" + input.stream()
      .filter(this::isValid)
      .count();
  }

  boolean isValid(String s) {
    var p = Pattern.compile(REGEX);
    var m = p.matcher(s);
    m.find();
    var sCount = m.group(4).chars().filter(c -> c == m.group(3).charAt(0)).count();
    int min = Integer.parseInt(m.group(1));
    int max = Integer.parseInt(m.group(2));
    return sCount >= min && sCount <= max;
  }

  @Override
  protected Object part2() {
    return "" + input.stream()
      .filter(this::isValid2)
      .count();
  }

  boolean isValid2(String s) {
    try {
      var p = Pattern.compile(REGEX);
      var m = p.matcher(s);
      m.find();
      int min = Integer.parseInt(m.group(1));
      int max = Integer.parseInt(m.group(2));
      var pw = m.group(4);
      char c = m.group(3).charAt(0);
      return pw.charAt(min-1) == c ^ pw.charAt(max-1) == c;
    } catch (Exception e) {
      return false;
    }
  }
}
