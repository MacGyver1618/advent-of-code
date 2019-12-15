import java.util.*;
import java.util.stream.*;

public class Advent15 extends Advent {

  static final int WALL = 0;
  static final int SPACE = 1;
  static final int OXYGEN = 2;
  static final int UNEXPLORED = -1;

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
  Map<Point, Integer> grid;

  Point position;
  Point droid;
  Point target;

  int xmin = Integer.MAX_VALUE;
  int xmax = Integer.MIN_VALUE;
  int ymin = Integer.MAX_VALUE;
  int ymax = Integer.MIN_VALUE;

  public Advent15() {
    super(15);
  }

  @Override
  protected void parseInput() {
    memory = Arrays.stream(input.get(0).split(","))
      .mapToLong(Long::valueOf)
      .toArray();
    machine = new IntCodeMachine(memory);
    grid = new TreeMap<>();
    position = new Point(0,0);
    grid.put(position, 1);
  }

  @Override
  protected Object part1() {
    readGrid();
    /*
    findBounds();
    printGrid();
    */
    /*
    int direction;
    machine.run();
    printGrid();
    while (!machine.finished) {
      direction = readDirection();
      machine.input(direction);
      machine.run();
      updateGrid(direction);
      printGrid();
      sopl(position);
    }
    return machine.output();
    */
    var path = pathFrom(droid, target);
    return path.size() - 1;
  }

  private void readGrid() {
    readInput("15.grid");
    for (int y = 0; y < input.size(); y++) {
      String line = input.get(y);
      for (int x = 0; x < line.length(); x++) {
        char c = line.charAt(x);
        Point p = new Point(x,y);
        if (c == 'D') {
          droid = p;
          grid.put(p, SPACE);
        }
        if (c == 'O') {
          target = p;
          grid.put(p, SPACE);
        }
        if (c == '#') {
          grid.put(p, WALL);
        } else {
          grid.put(p, SPACE);
        }
      }
    }
  }

  private int readDirection() {
    while (true) {
      try {
        int result = readInt();
        if (result >= 1 && result <= 4) {
          return result;
        }
      } catch (Exception e) {}
    }
  }

  private void updateGrid(int direction) {
    Point nextPoint = position.add(directions.get(direction));
    int result = (int) machine.output();
    grid.put(nextPoint, result);
    if (result != WALL) {
      position = nextPoint;
    }
  }

  private void findBounds() {
    xmin = Integer.MAX_VALUE;
    xmax = Integer.MIN_VALUE;
    ymin = Integer.MAX_VALUE;
    ymax = Integer.MIN_VALUE;
    for (Point p : grid.keySet()) {
      if (p.x < xmin) xmin = p.x;
      if (p.x > xmax) xmax = p.x;
      if (p.y < ymin) ymin = p.y;
      if (p.y > ymax) ymax = p.y;
    }
  }

  private void printGrid() {
    screenBuffer = new StringBuffer();
    findBounds();
    for (int y = ymin; y <= ymax; y++) {
      for (int x = xmin; x <= xmax; x++) {
        Point current = new Point(x,y);
        if (current.equals(position)) {
          screenBuffer.append('D');
          continue;
        }
        switch (grid.getOrDefault(current, UNEXPLORED)) {
          case WALL: screenBuffer.append('#'); break;
          case SPACE: screenBuffer.append(' '); break;
          case OXYGEN: screenBuffer.append('O'); break;
          case UNEXPLORED: screenBuffer.append('.'); break;
        }
      }
      screenBuffer.append("\n");
    }
    sopl(screenBuffer.toString());
  }

  private List<Point> pathFrom(Point start, Point goal) {
    Set<Point> closedSet = new TreeSet<>();
    Set<Point> openSet = new TreeSet<>();
    openSet.add(start);

    Map<Point, Point> cameFrom = new TreeMap<>();
    Map<Point, Integer> gScore = new TreeMap<>();
    gScore.put(start, 0);

    Map<Point, Integer> fScore = new TreeMap<>();
    fScore.put(start, start.manhattanDistance(goal));

    while (!openSet.isEmpty()) {
      Point current = openSet.stream()
                             .sorted(Comparator.comparing(p -> fScore.getOrDefault(p, Integer.MAX_VALUE)))
                             .findFirst()
                             .orElseThrow(IllegalStateException::new);
      if (current.equals(goal)) {
        return reconstructPath(cameFrom, current);
      }

      openSet.remove(current);
      closedSet.add(current);

      for (Point neighbor : neighbors(current)) {
        if (closedSet.contains(neighbor)) {
          continue;
        }
        int tentative_gScore = gScore.getOrDefault(current, Integer.MAX_VALUE-1) + 1;
        if (!openSet.contains(neighbor)) {
          openSet.add(neighbor);
        } else if (tentative_gScore >= gScore.getOrDefault(neighbor, Integer.MAX_VALUE-1)) {
          continue;
        }

        cameFrom.put(neighbor, current);
        gScore.put(neighbor, tentative_gScore);
        fScore.put(neighbor, gScore.get(neighbor) + neighbor.manhattanDistance(goal));
      }
    }
    return null;
  }

  private List<Point> neighbors(Point p) {
    return Arrays.asList(NORTH, SOUTH, EAST, WEST).stream()
      .map(d -> directions.get(d).add(p))
      .filter(n -> grid.get(n) == SPACE)
      .collect(Collectors.toList());
  }

  private List<Point> reconstructPath(Map<Point, Point> cameFrom, Point current) {
    List<Point> totalPath = new LinkedList<>();
    totalPath.add(current);
    while (cameFrom.containsKey(current)) {
      current = cameFrom.get(current);
      totalPath.add(current);
    }
    Collections.reverse(totalPath);
    return totalPath;
  }

  @Override
  protected Object part2() {
    int minutes = 0;
    Set<Point> currentRound = new TreeSet<>();
    Set<Point> nextRound = new TreeSet<>();
    currentRound.add(target);
    while (!fullyOxygenated()) {
      for (Point p : currentRound) {
        nextRound.addAll(neighbors(p));
        grid.put(p, OXYGEN);
      }
      currentRound = nextRound;
      nextRound = new TreeSet<>();
      /*
      sopl();sopl();
      printGrid();
      sopl(minutes, " min");
      try {
        Thread.sleep(20);
      } catch (Exception e) {}*/
      minutes++;
    }
    return minutes - 1;
  }

  private boolean fullyOxygenated() {
    return grid.values().stream().noneMatch(i -> i == SPACE);
  }
}
