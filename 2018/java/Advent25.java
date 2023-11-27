import java.util.*;
import java.util.stream.*;

public class Advent25 extends Advent {

  List<Point4> points = new ArrayList<>();
  Set<Set<Point4>> constellations = new HashSet<>();
  Set<Point4> constellated = new TreeSet<>();
  Set<Point4> unconstellated = new TreeSet<>();

  public Advent25() {
    super(25);
  }

  @Override
  protected void readInput() {
    //readExample();
    super.readInput();
  }

  @Override
  protected void parseInput() {
    for (String line : input) {
      Point4 point = new Point4();
      String[] toks = line.split(",");
      point.x = Integer.parseInt(toks[0]);
      point.y = Integer.parseInt(toks[1]);
      point.z = Integer.parseInt(toks[2]);
      point.t = Integer.parseInt(toks[3]);
      points.add(point);
    }
  }

  @Override
  protected String part1() {
    unconstellated.addAll(points);
    for (Point4 point : points) {
      if (canConstellate(point)) {
        Set<Set<Point4>> constellables = findConstellable(point);
        constellations.removeAll(constellables);
        Set<Point4> newConstellation = union(constellables);
        newConstellation.add(point);
        constellations.add(newConstellation);
        constellated.add(point);
        unconstellated.remove(point);
      } else {
        Set<Point4> constellation = findConstellation(point);
        if (constellation.size() > 0) {
          constellations.add(constellation);
          constellated.addAll(constellation);
          unconstellated.removeAll(constellation);
        }
      }
    }
    return "" + constellations.size();
  }

  private boolean canConstellate(Point4 point) {
    return constellations.stream().anyMatch(c -> canConstellate(point, c));
  }

  private boolean canConstellate(Point4 point, Set<Point4> constellation) {
    return constellation.stream().anyMatch(p -> point.manhattanDistance(p) <= 3);
  }

  private Set<Set<Point4>> findConstellable(Point4 point) {
    return constellations.stream()
                         .filter(s -> canConstellate(point, s))
                         .collect(Collectors.toSet());
  }

  private Set<Point4> union(Set<Set<Point4>> sets) {
    Set<Point4> union = new TreeSet<>();
    sets.forEach(s -> union.addAll(s));
    return union;
  }

  private Set<Point4> findConstellation(Point4 point) {
    Set<Point4> constellation = new TreeSet<>();
    constellation.add(point);
    for (Point4 other : unconstellated) {
      if (other.equals(point)) continue;
      if (point.manhattanDistance(other) <= 3) {
        constellation.add(other);
      }
    }
    constellated.addAll(constellation);
    unconstellated.removeAll(constellation);
    return constellation;
  }

  @Override
  protected String part2() {
    return "Finished!";
  }

  class Point4 implements Comparable<Point4> {
    int x, y, z, t;
    Comparator<Point4> comparator = Comparator.comparingInt((Point4 p) -> p.x + p.y + p.z + p.t).thenComparingInt((Point4 p) -> p.x).thenComparingInt((Point4 p) -> p.y).thenComparingInt((Point4 p) -> p.z).thenComparingInt((Point4 p) -> p.t);

    int manhattanDistance(Point4 other) {
      return Math.abs(this.x - other.x)
           + Math.abs(this.y - other.y)
           + Math.abs(this.z - other.z)
           + Math.abs(this.t - other.t);
    }

    public int hashCode() {
      return 100*(t + 100*(z + 100*(y + 100*x)));
    }

    public boolean equals(Object o) {
      Point4 other = (Point4) o;
      return this.x == other.x
          && this.y == other.y
          && this.z == other.z
          && this.t == other.t;
    }

    public String toString() {
      StringBuilder sb = new StringBuilder();
      sb.append("(")
        .append(x).append(",")
        .append(y).append(",")
        .append(z).append(",")
        .append(t)
        .append(")");
      return sb.toString();
    }

    public int compareTo(Point4 other) {
      return comparator.compare(this, other);
    }
  }
}
