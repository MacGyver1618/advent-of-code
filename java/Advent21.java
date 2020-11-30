import java.util.*;
import java.util.stream.*;

public class Advent21 extends Advent {

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

  public Advent21() {
    super(21);
  }

  @Override
  protected void parseInput() {
    memory = Arrays.stream(input.get(0).split(","))
      .mapToLong(Long::valueOf)
      .toArray();
    machine = new IntCodeMachine(memory);
    grid = new TreeMap<>();
    machine = new IntCodeMachine(memory);
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

  @Override
  protected Object part1() {
    putInstruction("NOT A J");
    putInstruction("NOT C T");
    putInstruction("OR T J");
    putInstruction("AND D J");
    putInstruction("WALK");
    machine.run();
    return machine.output();
  }

  private void putInstruction(String instruction) {
    instruction.chars()
      .forEach(c -> machine.input((long) c));
    machine.input((long)'\n');
  }

  void printOutput() {
    machine.programOutputs.forEach(l -> sop((char)l.longValue()));
  }

  @Override
  protected Object part2() {
    machine = new IntCodeMachine(memory);
    putInstruction("NOT A J");
    putInstruction("NOT B T");
    putInstruction("OR T J");
    putInstruction("NOT C T");
    putInstruction("OR T J");
    putInstruction("AND H J");
    putInstruction("OR E J");
    putInstruction("AND D J");
    putInstruction("RUN");
    machine.run();
    return machine.output();
  }
}
