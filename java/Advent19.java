import java.util.*;
import java.util.stream.*;

public class Advent19 extends Advent {

  boolean visual = true;
  int frameInterval = 50;

  static final int NORTH = 1;
  static final int SOUTH = 2;
  static final int WEST = 3;
  static final int EAST = 4;

  List<Point> limits = Arrays.asList(new Point(0,-99), new Point(99,0), new Point(99,-99));

  Map<Integer, Point> directions = new HashMap<>() {{
    put(NORTH, new Point(0,-1));
    put(SOUTH, new Point(0,1));
    put(WEST, new Point(-1,0));
    put(EAST, new Point(1,0));
  }};

  StringBuffer screenBuffer;
  long[] memory;
  IntCodeMachine machine;
  Map<Point, Character> grid;


  Point position;
  Point droid;
  Point target;

  int xmin = Integer.MAX_VALUE;
  int xmax = Integer.MIN_VALUE;
  int ymin = Integer.MAX_VALUE;
  int ymax = Integer.MIN_VALUE;

  public Advent19() {
    super(19);
  }

  @Override
  protected void parseInput() {
    memory = Arrays.stream(input.get(0).split(","))
      .mapToLong(Long::valueOf)
      .toArray();
    machine = new IntCodeMachine(memory);
    grid = new TreeMap<>();
  }

  private void populateGrid() {
    for (int y = 0; y < 100; y++) {
      if (y < ymin) ymin = y;
      if (y > ymax) ymax = y;
      for (int x = 0; x < 100; x++) {
        if (x < xmin) xmin = x;
        if (x > xmax) xmax = x;
        machine = new IntCodeMachine(memory);
        machine.input(x);
        machine.input(y);
        machine.run();
        long val = machine.output();
        Point p = new Point(x,y);
        if (val == 1) {
          grid.put(p, '#');
        } else {
          grid.put(p, ' ');
        }
      }
    }
  }

  @Override
  protected Object part1() {
    int total = 0;
    for (int y = 0; y < 50; y++) {
      for (int x = 0; x < 50; x++) {
        if (probe(new Point(x,y)) == '#') {
          total++;
        }
      }
    }
    return total;
  }

  @Override
  protected Object part2() {
    int y = 10;
    int x = findXStart(y, 0);
    while (true) {
      Point p = new Point(x,y);
      if (canFit(p)) {
        return p.x*10_000 + p.y-99;
      }
      y++;
      x = findXStart(y, x);
    }
  }

  int findXStart(int y, int oldX) {
    for (int x = oldX; ; x++) {
      Point p = new Point(x,y);
      if (probe(p) == '#')
        return p.x;
    }
  }

  private boolean canFit(Point p) {
    if (probe(p) != '#') return false;
    for (Point l : limits) {
      if (probe(p.add(l)) != '#') {
        return false;
      }
    }
    return true;
  }

  private char probe(Point p) {
    Character c = grid.get(p);
    if (c == null) {
      machine = new IntCodeMachine(memory);
      machine.input(p.x);
      machine.input(p.y);
      machine.run();
      long val = machine.output();
      if (val == 1) {
        c = '#';
      } else {
        c = ' ';
      }
      grid.put(p, c);
    }
    return c;
  }

  private void printGrid() {
    for (int y = ymin; y <= ymax; y++) {
      for (int x = xmin; x <= xmax; x++) {
        char c = grid.getOrDefault(new Point(x,y), '.');
        sop(c);
      }
      sopl();
    }
  }
}
