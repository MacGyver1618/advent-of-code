import java.util.*;
import java.util.regex.*;
import java.util.stream.*;

public class Advent17 extends Advent {

  Pattern pattern = Pattern.compile("([xy])=(\\d+), [xy]=(\\d+)..(\\d+)");

  Map<Point, Character> grid = new TreeMap<>();

  int xMin = 500;
  int xMax = 500;
  int yMin = Integer.MAX_VALUE;
  int yMax = Integer.MIN_VALUE;

  Point spring = new Point(500,0);
  Set<Point> drips = new TreeSet<>();
  Set<Point> newDrips = new TreeSet<>();
  Set<Point> deadDrips = new TreeSet<>();

  public Advent17() {
    super(17);
  }

  @Override
  protected void parseInput() {
    grid.put(spring, '+');
    for (String line : input) {
      Matcher m = pattern.matcher(line);
      m.find();
      char first = m.group(1).charAt(0);
      int a = Integer.parseInt(m.group(2));
      int b = Integer.parseInt(m.group(3));
      int c = Integer.parseInt(m.group(4));
      if (first == 'x') {
        parseVein(a, a, b, c);
      } else {
        parseVein(b, c, a, a);
      }
    }
  }

  private void parseVein(int x0, int x1, int y0, int y1) {
    for (int x = x0; x <= x1; x++) {
      if (x > xMax) xMax = x;
      if (x < xMin) xMin = x;
      for (int y = y0; y <= y1; y++) {
        if (y > yMax) yMax = y;
        if (y < yMin) yMin = y;
        Point p = new Point(x,y);
        grid.put(p, '#');
      }
    }
  }

  @Override
  protected String part1() {
    long stillWater = 0;
    long previousStill = Integer.MIN_VALUE;
    long flowingWater = 0;
    long previousFlowing = Integer.MIN_VALUE;
    drips.add(spring);
    while (stillWater != previousStill || flowingWater != previousFlowing) {
      drips.addAll(newDrips);
      drips.removeAll(deadDrips);
      newDrips.clear();
      deadDrips.clear();
      for (Point drip : drips) {
        drip(drip);
      }
      previousStill = stillWater;
      stillWater = stillWater();
      previousFlowing = flowingWater;
      flowingWater = flowingWater();
    }
    return "" + countWater();
  }

  private long countWater() {
    return stillWater() + flowingWater();
  }

  private long stillWater() {
    return countWater('~');
  }

  private long flowingWater() {
    return countWater('|');
  }

  private long countWater(char match) {
    return grid.entrySet()
               .parallelStream()
               .filter(e -> e.getKey().y >= yMin)
               .filter(e -> e.getValue() == match)
               .count();
  }

  private void drip(Point drip) {
    if (below(drip) == '~') {
      deadDrips.add(drip);
      return;
    }
    Point cursor = drip;
    while (below(cursor) != '#' && below(cursor) != '~' ) {
      if (cursor.y > yMax) {
        return;
      }
      if (at(cursor) == '.') {
        grid.put(cursor, '|');
      }
      cursor = down(cursor);
    }
    Point le = edgeToLeft(cursor);
    Point re = edgeToRight(cursor);
    if (at(le) == '#' && at(re) == '#') {
      fill(right(le), re);
    } else {
      if (at(le) == '#') le = right(le);
      if (at(re) != '#') re = right(re);
      overFlow(le, re);
    }
  }

  private Point edgeToLeft(Point p) {
    Point left = left(p);
    while (!atEdge(left)) {
      left = left(left);
      if (left.x < xMin) xMin = left.x;
    }
    return left;
  }

  private Point edgeToRight(Point p) {
    Point right = right(p);
    while (!atEdge(right)) {
      right = right(right);
      if (right.x > xMax) xMax = right.x;
    }
    return right;
  }

  private boolean atEdge(Point p) {
    return below(p) == '.' || below(p) == '|' || at(p) == '#';
  }

  private void fill(Point start, Point end) {
    Point cursor = start;
    while (!cursor.equals(end)) {
      grid.put(cursor, '~');
      cursor = right(cursor);
    }
  }

  private void overFlow(Point start, Point end) {
    Point cursor = start;
    if (below(start) == '.') {
      newDrips.add(start);
    }
    if (below(left(end)) == '.') {
      newDrips.add(left(end));
    }
    while (!cursor.equals(end)) {
      grid.put(cursor, '|');
      cursor = right(cursor);
    }
  }

  private char above(Point p) {
    return at(up(p));
  }

  private char below(Point p) {
    return at(down(p));
  }

  private char leftOf(Point p) {
    return at(left(p));
  }

  private char rightOf(Point p) {
    return at(right(p));
  }

  private char at(Point p) {
    return grid.getOrDefault(p, '.');
  }

  private Point up(Point p) {
    return p.add(new Point(0,-1));
  }

  private Point down(Point p) {
    return p.add(new Point(0,1));
  }

  private Point left(Point p) {
    return p.add(new Point(-1,0));
  }

  private Point right(Point p) {
    return p.add(new Point(1,0));
  }

  @Override
  protected String part2() {
    return "" + stillWater();
  }
}
