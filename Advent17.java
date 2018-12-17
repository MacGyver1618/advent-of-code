import java.util.*;
import java.util.regex.*;
import java.util.stream.*;

public class Advent17 extends Advent {

  Pattern xVein = Pattern.compile("x=(\\d+), y=(\\d+)..(\\d+)");
  Pattern yVein = Pattern.compile("y=(\\d+), x=(\\d+)..(\\d+)");

  int Y_MIN = Integer.MAX_VALUE;
  int Y_MAX = Integer.MIN_VALUE;
  int X_MIN = 500;
  int X_MAX = 500;

  Point spring = new Point(500,0);
  Set<Point> cursors = new TreeSet<>();
  Map<Point, Character> ground = new TreeMap<>(Point.yComparator());

  public Advent17() {
    super(17);
  }

  @Override
  protected void readInput() {
    //readExample();
    super.readInput();
  }

  @Override
  protected void parseInput() {
    ground.clear();
    ground.put(spring, '+');
    for (String line : input) {
      Matcher xMatcher = xVein.matcher(line);
      Matcher yMatcher = yVein.matcher(line);
      if (xMatcher.find()) {
        populateVein(xMatcher, 'X');
      } else if (yMatcher.find()) {
        populateVein(yMatcher, 'Y');
      }
    }
  }

  private void populateVein(Matcher m, char dim) {
    int dConst = Integer.parseInt(m.group(1));
    int dMin = Integer.parseInt(m.group(2));
    int dMax = Integer.parseInt(m.group(3));
    if (dim == 'X') {
      drawVein(dConst, dConst, dMin, dMax);
    } else {
      drawVein(dMin, dMax, dConst, dConst);
    }
  }

  private void drawVein(int xStart, int xEnd, int yStart, int yEnd) {
    for (int y = yStart; y <= yEnd; y++) {
      if (y < Y_MIN) Y_MIN = y;
      if (y > Y_MAX) Y_MAX = y;
      for (int x = xStart; x <= xEnd; x++) {
        if (x < X_MIN) X_MIN = x;
        if (x > X_MAX) X_MAX = x;
        Point p = new Point(x,y);
        ground.put(p, '#');
      }
    }
  }

  @Override
  protected String part1() {
    sopl("X=", X_MIN, "..", X_MAX, ", Y=", Y_MIN, "..", Y_MAX);
    //printGround(0,81);
    cursors.add(spring);
    int tick = 0;
    int start = 0, end = 81;
    String command = "";
    while (cursorsInRange(cursors)) {
      tick++;
      cursors = tick();
    }
    return "" + countWater();
  }

  private long countWater() {
    return ground.entrySet()
                 .stream()
                 .filter(e -> e.getKey().y >= Y_MIN && e.getKey().y <= Y_MAX)
                 .map(e -> e.getValue())
                 .filter(c -> c == '~' || c == '|')
                 .count();
  }

  private boolean cursorsInRange(Set<Point> cursors) {
    return cursors.stream().anyMatch(p -> p.y <= Y_MAX);
  }

  private Set<Point> tick() {
    Set<Point> result = new TreeSet<>();
    cursors.forEach(c -> result.addAll(tick(c)));
    return result;
  }

  private Set<Point> tick(Point cursor) {
    Set<Point> result = new TreeSet<>(Point.yComparator().reversed());
    if (cursor.x > X_MAX) X_MAX = cursor.x;
    if (cursor.x < X_MIN) X_MIN = cursor.x;
    Point down = down(cursor);
    if (down.y > Y_MAX) return result;
    char below = ground.getOrDefault(down, '.');
    if (below == '.') {
      ground.put(down, '|');
      result.add(down);
    } else if (below == '|') {
      ground.put(cursor, '|');
    } else if (overFlow(down)) {
      ground.put(cursor, '|');
    } else if (below == '#'|| below == '~') {
      Set<Point> horizontalCursors = spreadHorizontal(cursor);
      if (horizontalCursors.isEmpty()) {
        result.addAll(findFlowPoints(cursor));
      } else {
        result.addAll(horizontalCursors);
      }
    }
    return result;
  }

  private boolean overFlow(Point cursor) {
    return overFlowLeft(left(cursor)) || overFlowRight(right(cursor));
  }

  private boolean overFlowLeft(Point cursor) {
    if (cursor.x < X_MIN) return false;
    char c = ground.getOrDefault(cursor, '.');
    if (c == '#') return false;
    return c == '|' || overFlowLeft(left(cursor));
  }

  private boolean overFlowRight(Point cursor) {
    if (cursor.x > X_MAX) return false;
    char c = ground.getOrDefault(cursor, '.');
    if (c == '#') return false;
    return c == '|' || overFlowRight(right(cursor));
  }

  private Set<Point> findFlowPoints(Point cursor) {
    Set<Point> result = new TreeSet<>();
    Point candidate = up(cursor);
    char atCandidate = ground.getOrDefault(candidate, '.');
    if (atCandidate == '|') {
      result.add(candidate);
    }
    result.addAll(flowLeft(candidate));
    result.addAll(flowRight(candidate));
    return result;
  }

  private Set<Point> flowLeft(Point p) {
    Set<Point> result = new TreeSet<>();
    Point candidate = left(p);
    if (candidate.x < X_MIN) return result;
    char atCandidate = ground.getOrDefault(candidate, '.');
    if (atCandidate == '#') {
      return result;
    }
    if (atCandidate == '|') {
      result.add(candidate);
    }
    result.addAll(flowLeft(candidate));
    return result;
  }

  private Set<Point> flowRight(Point p) {
    Set<Point> result = new TreeSet<>();
    Point candidate = right(p);
    if (candidate.x > X_MAX) return result;
    char atCandidate = ground.getOrDefault(candidate, '.');
    if (atCandidate == '#') {
      return result;
    }
    if (atCandidate == '|') {
      result.add(candidate);
    }
    result.addAll(flowRight(candidate));
    return result;
  }

  private Set<Point> spreadHorizontal(Point p) {
    Set<Point> result = new TreeSet<>();
    ground.put(p, '~');
    result.addAll(spreadLeft(left(p)));
    result.addAll(spreadRight(right(p)));
    return result;
  }

  private Set<Point> spreadLeft(Point p) {
    Set<Point> result = new TreeSet<>();
    char current = ground.getOrDefault(p, '.');
    if (current == '#') return result;
    char below = ground.getOrDefault(down(p), '.');
    if (below == '.') {
      ground.put(p, '|');
      setOverFlow(p);
      result.add(p);
    } else if (below == '|') {
      ground.put(p, '|');
    } else {
      if (current != '|') {
        ground.put(p, '~');
      }
      result.addAll(spreadLeft(left(p)));
    }
    return result;
  }

  private Set<Point> spreadRight(Point p) {
    Set<Point> result = new TreeSet<>();
    char current = ground.getOrDefault(p, '.');
    if (current == '#') return result;
    char below = ground.getOrDefault(down(p), '.');
    if (below == '.') {
      ground.put(p, '|');
      setOverFlow(p);
      result.add(p);
    } else if (below == '|') {
      ground.put(p, '|');
    } else {
      if (current != '|') {
        ground.put(p, '~');
      }
      result.addAll(spreadRight(right(p)));
    }
    return result;
  }

  private void setOverFlow(Point p) {
    setOverFlowLeft(left(p));
    setOverFlowRight(right(p));
  }

  private void setOverFlowLeft(Point p) {
    char current = ground.getOrDefault(p, '.');
    char below = ground.getOrDefault(down(p), '.');
    if (below == '|' || current == '#' || below == '.') return;
    ground.put(p, '|');
    setOverFlowLeft(left(p));
  }

  private void setOverFlowRight(Point p) {
    char current = ground.getOrDefault(p, '.');
    char below = ground.getOrDefault(down(p), '.');
    if (below == '|' || current == '#' || below == '.') return;
    ground.put(p, '|');
    setOverFlowRight(right(p));
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

  private void printGround() {
    printGround(Y_MIN, Y_MAX);
  }

  private void printGround(int yStart, int yEnd) {
    StringBuilder sb = new StringBuilder();
    for (int y = yStart; y <= yEnd; y++) {
      for (int x = X_MIN; x <= X_MAX; x++) {
        Point p = new Point(x,y);
        char c = ground.getOrDefault(p, ' ');
        sb.append(c);
      }
      sb.append('\n');
    }
    sop(sb.toString());
  }

  @Override
  protected String part2() {
    int tick = 0;
    int start = 0;
    int end = 82;
    while (tick < 0) {
      printStillGround(Math.max(start, 0), Math.min(end,Y_MAX));
      sopl("Tick ", tick, ": ", cursors);
      switch(readString()) {
        case "p":
          start -= 83;
          end -= 83;
          break;
        case "n":
          start += 83;
          end += 83;
          break;
        case "q":
          tick = 5001;
      }
    }
    printStillGround(0,Y_MAX);
    return "" + countStillWater();
  }

  private void printStillGround(int yStart, int yEnd) {
    sopl(stillGround(yStart, yEnd));
  }

  private String stillGround(int yStart, int yEnd) {
    StringBuilder sb = new StringBuilder();
    for (int y = yStart; y <= yEnd; y++) {
      for (int x = X_MIN; x <= X_MAX; x++) {
        Point p = new Point(x,y);
        char c = ground.getOrDefault(p, ' ');
        sb.append(c == '|' ? ' ' : c);
      }
      sb.append('\n');
    }
    return sb.toString();
  }

  private long countStillWater() {
    return ground.values()
                 .stream()
                 .filter(c -> c == '~')
                 .count();
  }
}
