import java.util.*;
import java.util.function.*;
import java.util.regex.*;
import java.util.stream.*;

public class Advent23 extends Advent {

  Pattern pattern = Pattern.compile("pos=<(-?\\d+),(-?\\d+),(-?\\d+)>, r=(\\d+)");
  List<Nanobot> bots;

  public Advent23() {
    super(23);
  }

  @Override
  protected void parseInput() {
    bots = new ArrayList<>(input.size());
    for (String line : input) {
      bots.add(parseBot(line));
    }
  }

  private Nanobot parseBot(String s) {
    Matcher m = pattern.matcher(s);
    m.find();
    int x = Integer.parseInt(m.group(1));
    int y = Integer.parseInt(m.group(2));
    int z = Integer.parseInt(m.group(3));
    int r = Integer.parseInt(m.group(4));
    return new Nanobot(new Point3(x,y,z), r);
  }

  @Override
  protected String part1() {
    Nanobot bestRange = bots.stream()
                            .sorted(Comparator.comparing((Nanobot b) -> b.range).reversed())
                            .findFirst()
                            .orElseThrow(IllegalStateException::new);
    return "" + bots.stream()
                    .filter(b -> b.position.manhattanDistance(bestRange.position) <= bestRange.range)
                    .count();
  }

  @Override
  protected String part2() {
    int r = maxDimension();
    Point3 origin = new Point3(0,0,0);
    Set<Point3> candidates = Set.of(origin);
    while (r > 0) {
      r = r/2;
      candidates = findCandidates(candidates, r);
    }
    return "" + candidates.stream()
                          .mapToInt(p -> p.manhattanDistance(origin))
                          .min()
                          .getAsInt();
  }

  private int maxDimension() {
    return bots.stream()
               .map(b -> b.position)
               .mapToInt(p -> Math.max(Math.abs(p.x), Math.max(Math.abs(p.y), Math.abs(p.z))))
               .max()
               .getAsInt();
  }

  private Set<Point3> findCandidates(Set<Point3> current, int range) {
    Set<Point3> result = new TreeSet<>();
    current.forEach(p -> result.addAll(pointsAtDistance(p, range)));
    int mostBotsInRange = result.stream().mapToInt((Point3 p) -> botsInRange(p, range).size()).max().getAsInt();
    result.removeIf(p -> botsInRange(p, range).size() != mostBotsInRange);
    return result;
  }

  private Set<Point3> pointsAtDistance(Point3 p, int d) {
    Set<Point3> result = new TreeSet<>();
    for (int i = -1; i < 2; i++) {
      for (int j = -1; j < 2; j++) {
        for (int k = -1; k < 2; k++) {
          result.add(new Point3(p.x + d*i, p.y + d*j, p.z + d*k));
        }
      }
    }
    return result;
  }

  private Set<Nanobot> botsInRange(Point3 point, int range) {
    return bots.stream()
               .filter(bot -> bot.position.manhattanDistance(point) <= range + bot.range)
               .collect(Collectors.toSet());
  }

  class Nanobot {
    Point3 position;
    int range;

    Nanobot(Point3 position, int range) {
      this.position = position;
      this.range = range;
    }

    public boolean inRange(Nanobot other) {
      return this.position.manhattanDistance(other.position) <= this.range;
    }

    public boolean inRange(Point3 other) {
      return this.position.manhattanDistance(other) <= this.range;
    }

    public String toString() {
      return "pos=<" + position.x + "," + position.y + "," + position.z +">, r=" + range;
    }
  }

  static class Point3 implements Comparable<Point3> {
    int x, y, z;

    Point3(int x, int y, int z) {
      this.x = x;
      this.y = y;
      this.z = z;
    }

    @Override
    public boolean equals(Object other) {
      Point3 that = (Point3) other;
      return this.x == that.x && this.y == that.y && this.z == that.z;
    }

    @Override
    public int hashCode() {
      return 1_000_000*x + 1_000*y + z;
    }

    @Override
    public String toString() {
      return "(" + x + "," + y + "," + z + ")";
    }

    int manhattanDistance(Point3 other) {
      return Math.abs(this.x-other.x) + Math.abs(this.y-other.y) + Math.abs(this.z-other.z);
    }

    public int compareTo(Point3 other) {
      int xDiff = this.x - other.x;
      int yDiff = this.y - other.y;
      int zDiff = this.z - other.z;
      int coordDiff = xDiff + yDiff + zDiff;
      return coordDiff != 0 ? coordDiff : xDiff != 0 ? xDiff : yDiff != 0 ? yDiff : zDiff;
    }
  }
}
