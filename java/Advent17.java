import java.util.*;
import java.util.stream.*;

public class Advent17 extends Advent {

  boolean visual = false;
  int frameInterval = 50;

  static final int NORTH = 1;
  static final int SOUTH = 2;
  static final int WEST = 3;
  static final int EAST = 4;

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
  char[][] ascii;

  Point position;
  Point droid;
  Point target;

  int xmin = Integer.MAX_VALUE;
  int xmax = Integer.MIN_VALUE;
  int ymin = Integer.MAX_VALUE;
  int ymax = Integer.MIN_VALUE;

  public Advent17() {
    super(17);
  }

  @Override
  protected void parseInput() {
    memory = Arrays.stream(input.get(0).split(","))
      .mapToLong(Long::valueOf)
      .toArray();
    machine = new IntCodeMachine(memory);
    grid = new TreeMap<>();
    //position = new Point(0,0);
    //grid.put(position, 1);
  }

  @Override
  protected Object part1() {
    populateGrid();
    int checksum = 0;
    for (var point : grid.keySet()) {
      if (isIntersection(point)) {
        checksum += point.x * point.y;
      }
    }
    return checksum;
  }

  private boolean isIntersection(Point p) {
    if (grid.get(p) != '#') {
      return false;
    }
    return directions.values().stream()
      .map(d -> d.add(p))
      .map(d -> grid.getOrDefault(d, '.'))
      .allMatch(d -> d == '#');
  }

  private void populateGrid() {
    machine.run();
    int x = 0, y = 0;
    for (long output : machine.programOutputs) {
      char c = (char) output;
      if (c == '\n') {
        y++;
        x = 0;
        continue;
      }
      Point point = new Point(x,y);
      checkBounds(point);
      grid.put(point, c);
      x++;
    }
  }

  private void checkBounds(Point p) {
    if (p.x < xmin) xmin = p.x;
    if (p.x > xmax) xmax = p.x;
    if (p.y < ymin) ymin = p.y;
    if (p.y > ymax) ymax = p.y;
  }

  @Override
  protected Object part2() {
    memory[0] = 2;
    machine = new IntCodeMachine(memory);
    machine.run();
    if (visual) {
      machine.programOutputs
        .stream()
        .limit(47*48+1)
        .forEach(l -> sop((char) l.longValue(), " "));
    }
    putInstruction("A,B,B,C,B,C,B,C,A,A");
    putInstruction("L,6,R,8,L,4,R,8,L,12");
    putInstruction("L,12,R,10,L,4");
    putInstruction("L,12,L,6,L,4,L,4");
    machine.run();
    machine.programOutputs.clear();
    putInstruction(visual ? "y" : "n");
    machine.run();
    long output = machine.output();
    if (visual) {
      animate();
    }
    return output;
  }

  private void animate() {
    int screenSize = (ymax+1)*(xmax+2)+1;
    StringBuffer screenBuffer = new StringBuffer();
    for (int i = 0; i < machine.programOutputs.size() - 1; i++) {
      long current = machine.programOutputs.get(i);
      screenBuffer.append((char) current);
      if ((i % screenSize) % (xmax+2) != 0) {
        screenBuffer.append(' ');
      }
      if (i % screenSize == 0) {
        sopl(screenBuffer.toString());
        screenBuffer = new StringBuffer();
        halt(frameInterval);
      }
    }
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

  private void putInstruction(String instruction) {
    instruction.chars()
      .forEach(c -> machine.input((long) c));
    machine.input((long)'\n');
  }
}
