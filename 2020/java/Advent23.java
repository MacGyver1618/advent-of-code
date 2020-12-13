import java.util.*;
import java.util.stream.*;

public class Advent23 extends Advent {

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
  Map<Integer, IntCodeMachine> machines;
  Map<Point, Character> grid;

  int xmin = Integer.MAX_VALUE;
  int xmax = Integer.MIN_VALUE;
  int ymin = Integer.MAX_VALUE;
  int ymax = Integer.MIN_VALUE;

  Point nat;
  Set<Long> sentValues;

  public Advent23() {
    super(23);
  }

  @Override
  protected void parseInput() {
    machines = new TreeMap<>();
    memory = Arrays.stream(input.get(0).split(","))
      .mapToLong(Long::valueOf)
      .toArray();
    for (int i = 0; i < 50; i++) {
      IntCodeMachine machine = new IntCodeMachine(memory);
      machine.input(i);
      machines.put(i, machine);
    }
    grid = new TreeMap<>();
    sentValues = new TreeSet<>();
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
    machines.values().forEach(IntCodeMachine::run);
    while (true) {
      processInputs();
      for (var machine : machines.values()) {
        if (machine.programOutputs.contains(255L)) {
          int index = machine.programOutputs.indexOf(255L);
          return machine.programOutputs.get(index+2);
        }
      }
      processOutputs();
    }
  }

  void processInputs() {
    for (var machine : machines.values()) {
      if (machine.programInputs.isEmpty()) {
        machine.input(-1);
      }
      machine.run();
    }
  }

  void processOutputs() {
    for (var machine : machines.values()) {
      if (!machine.programOutputs.isEmpty()) {
        sendPackets(machine);
        machine.programOutputs.clear();
      }
    }
  }

  void sendPackets(IntCodeMachine machine) {
    for (int i = 0; i < machine.programOutputs.size(); i += 3) {
      long address = machine.programOutputs.get(i);
      long x = machine.programOutputs.get(i + 1);
      long y = machine.programOutputs.get(i + 2);
      if (address == 255) {
        nat = new Point((int)x,(int)y);
        continue;
      }
      var target = machines.get((int)address);
      target.input(x);
      target.input(y);
    }
  }

  @Override
  protected Object part2() {
    parseInput();
    machines.values().forEach(IntCodeMachine::run);
    while (true) {
      if (machinesIdle()) {
        machines.get(0).input(nat.x);
        machines.get(0).input(nat.y);
        if (!sentValues.add((long)nat.y)) {
          return nat.y;
        }
      }
      processInputs();
      processOutputs();
    }
  }

  boolean machinesIdle() {
    return nat != null && machines.values().stream().allMatch(m -> m.programInputs.isEmpty());
  }
}
