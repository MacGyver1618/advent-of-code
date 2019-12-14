import java.util.*;
import java.util.stream.*;

public class Advent10 extends Advent {

  char[][] grid;
  int ymax, xmax;

  List<Point> asteroids;
  Point station;

  public Advent10() {
    super(10);
  }

  @Override
  protected void parseInput() {
    ymax = input.size();
    xmax = input.get(0).length();
    grid = new char[xmax][ymax];
    asteroids = new ArrayList<>();
    for (int y = 0; y < ymax; y++) {
      for (int x = 0; x < xmax; x++) {
        grid[x][y] = input.get(y).charAt(x);
        if (grid[x][y] == '#') {
          asteroids.add(new Point(x, y));
        }
      }
    }
  }

  @Override
  protected Object part1() {
    station = asteroids.stream()
      .sorted(Comparator.comparing(this::asteroidsVisibleFrom)
                        .reversed())
      .findFirst()
      .orElseThrow(NoSuchElementException::new);
    return asteroidsVisibleFrom(station);
  }

  private int asteroidsVisibleFrom(Point o) {
    return slopesFrom(o).size();
  }

  private Set<Point> slopesFrom(Point o) {
    return asteroids.stream()
      .filter((Point p) -> !o.equals(p))
      .map((Point p) -> findSlope(o, p))
      .collect(Collectors.toSet());
  }

  private Point findSlope(Point p1, Point p2) {
    return reduceSlope(p2.x - p1.x, p2.y - p1.y);
  }

  private Point reduceSlope(int xdiff, int ydiff) {
    if (xdiff == 0 || ydiff == 0) {
      return new Point(sign(xdiff), sign(ydiff));
    }
    int xabs = Math.abs(xdiff);
    int yabs = Math.abs(ydiff);
    int max = Math.max(xabs, yabs);
    int min = Math.min(xabs, yabs);
    int div = gcd(max, min);
    return new Point(xdiff / div, ydiff / div);
  }

  private int sign(int n) {
    return n == 0 ? 0 : n > 0 ? 1 : -1;
  }

  private int gcd(int x, int y) {
    if (y == 0) {
        return x;
    }
    return gcd(y, x % y);
  }

  @Override
  protected Object part2() {
    Point vertical = new Point(0,-1);
    List<Point> slopesInOrder = slopesFrom(station)
      .stream()
      .sorted(Comparator.comparingDouble((Point p) -> angleBetween(vertical, p)))
      .collect(Collectors.toList());
    Point destroyed = null, currentSlope = null;
    for (int i = 0, count = 0; count < 200; i++) {
      currentSlope = slopesInOrder.get(i % slopesInOrder.size());
      destroyed = destroy(station, currentSlope);
      if (destroyed != null) {
        count++;
      }
    }
    return destroyed.x*100 + destroyed.y;
  }

  private double angleBetween(Point p1, Point p2) {
    double angle = Math.atan2(p2.y, p2.x) - Math.atan2(p1.y, p1.x);
    if (angle < 0) {
      angle = 2*Math.PI + angle;
    }
    return angle;
  }

  private Point destroy(Point origin, Point slope) {
    for (Point current = origin.add(slope); inBounds(current); current = current.add(slope)) {
      if (asteroids.contains(current)) {
        asteroids.remove(current);
        return current;
      }
    }
    return null;
  }

  private boolean inBounds(Point p) {
    return p.x >= 0 && p.x < xmax && p.y >= 0 && p.y < ymax;
  }
}
