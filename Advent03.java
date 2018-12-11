import java.util.*;
import java.util.regex.*;
import java.util.stream.*;

public class Advent03 extends Advent {

  private List<List<Integer>> instructions = new LinkedList<>();
  private Map<Point, Integer> claims = new HashMap<>();
  private Pattern p = Pattern.compile("#(\\d+) @ (\\d+),(\\d+): (\\d+)x(\\d+)");

  public Advent03() {
    super(3);
  }

  @Override
  protected void parseInput() {
    for (String line : input) {
      parseLine(line);
    }
  }

  private void parseLine(String line) {
    Matcher m = p.matcher(line);
    if (m.find()) {
      int num = Integer.parseInt(m.group(1));
      int topX = Integer.parseInt(m.group(2));
      int topY = Integer.parseInt(m.group(3));
      int width = Integer.parseInt(m.group(4));
      int height = Integer.parseInt(m.group(5));
      instructions.add(Arrays.asList(num, topX, topY, width, height));
    }
  }

  @Override
  protected String part1() {
    for (List<Integer> line : instructions) {
      populateFabric(line);
    }
    return "" + countX();
  }

  private void populateFabric(List<Integer> ints) {
    for (int x = ints.get(1); x < ints.get(1) + ints.get(3); x++) {
      for (int y = ints.get(2); y < ints.get(2) + ints.get(4); y++) {
        Point point = new Point(x, y);
        Integer existing = claims.getOrDefault(point, 0);
        claims.put(point, existing + 1);
      }
    }
  }

  private long countX() {
    return claims.values()
                 .stream()
                 .mapToInt(Integer::intValue)
                 .filter(i -> i > 1)
                 .count();
  }

  @Override
  protected String part2() {
    for (List<Integer> line : instructions) {
      if (!overlaps(line)) {
        return "" + line.get(0);
      }
    }
    return "Failed";
  }

  private boolean overlaps(List<Integer> current) {
    int num = current.get(0);
    int curX = current.get(1);
    int curY = current.get(2);
    int curW = current.get(3);
    int curH = current.get(4);
    for (List<Integer> other : instructions) {
      if (other.get(0) == num) continue;
      int otherX = other.get(1);
      int otherY = other.get(2);
      int otherW = other.get(3);
      int otherH = other.get(4);
      // Test whether any corner of the current area falls within the other area
      if ((curX >= otherX && curX < otherX + otherW) && (curY >= otherY && curY < otherY + otherH)) return true;
      if ((curX + curW >= otherX && curX < otherX + otherW) && (curY >= otherY && curY < otherY + otherH)) return true;
      if ((curX >= otherX && curX < otherX + otherW) && (curY + curH >= otherY && curY < otherY + otherH)) return true;
      if ((curX + curW >= otherX && curX < otherX + otherW) && (curY + curH >= otherY && curY < otherY + otherH)) return true;
    }
    return false;
  }
}
