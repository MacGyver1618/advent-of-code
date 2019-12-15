import java.util.*;
import java.util.function.*;
import java.util.stream.*;

public class Advent15 extends Advent {

  boolean visual = true;
  int frameInterval = 20;

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
    droid = new Point(0,0);
    target = droid; //TODO : Remove
    grid.put(droid, SPACE);
    populateGrid();
    var path = pathFrom(new Point(0,0), target);
    return path.size() - 1;
  }

  private void populateGrid() {
    machine.run();
    Point p = droid;
    Queue<Point> queue = new LinkedList<>();
    queue.addAll(fringe(p));
    while (!queue.isEmpty()) {
      p = queue.poll();
      if (grid.containsKey(p)) {
        continue;
      }
      int tile = explore(p);
      queue.addAll(fringe(droid));
      if (visual) {
        IntStream.rangeClosed(1, 46-xmax+xmin)
          .forEach(e -> sopl());
        printGrid();
        halt(frameInterval);
      }
    }
  }

  private int explore(Point destination) {
    var path = pathFrom(droid, destination, p -> p.manhattanDistance(destination) == 1);
    path.add(destination);
    path.remove(0);
    int result = -1;
    for (Point point : path) {
      int input = nextInput(point);
      machine.input(input);
      machine.run();
      result = (int) machine.output();
      switch (result) {
        case WALL: break;
        case OXYGEN:
          target = point;
          result = SPACE;
          // fallthrough
        case SPACE:
          droid = point;
          break;
      }
      grid.put(point, result);
      if (visual) {
        printGrid();
        halt(frameInterval);
      }
    }
    return result;
  }

  private int nextInput(Point destination) {
    Point difference = destination.subtract(droid);
    switch (difference.toString()) {
      case "(0,-1)": return NORTH;
      case "(0,1)": return SOUTH;
      case "(-1,0)": return WEST;
      case "(1,0)": return EAST;
      default: throw new UnsupportedOperationException();
    }
  }

  private List<Point> fringe(Point p) {
    return Arrays.asList(NORTH, SOUTH, EAST, WEST).stream()
      .map(d -> directions.get(d).add(p))
      .filter(n -> grid.getOrDefault(n, UNEXPLORED) == UNEXPLORED)
      .collect(Collectors.toList());
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
        if (current.equals(droid)) {
          screenBuffer.append("D ");
          continue;
        }
        if (current.equals(target)) {
          screenBuffer.append("O ");
          continue;
        }
        switch (grid.getOrDefault(current, UNEXPLORED)) {
          case WALL: screenBuffer.append('#'); break;
          case SPACE: screenBuffer.append(' '); break;
          case OXYGEN: screenBuffer.append('O'); break;
          case UNEXPLORED: screenBuffer.append('.'); break;
        }
        screenBuffer.append(' ');
      }
      screenBuffer.append("\n");
    }
    sopl(screenBuffer.toString());
  }

  private List<Point> pathFrom(Point start, Point goal, Predicate<Point> stopCondition) {
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
      if (stopCondition.test(current)) {
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
    return Collections.emptyList();
  }

  private List<Point> pathFrom(Point start, Point goal) {
    return pathFrom(start, goal, p -> p.equals(goal));
  }

  private List<Point> neighbors(Point p) {
    return Arrays.asList(NORTH, SOUTH, EAST, WEST).stream()
      .map(d -> directions.get(d).add(p))
      .filter(n -> grid.getOrDefault(n, UNEXPLORED) == SPACE)
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
      if (visual) {
        sopl();sopl();
        printGrid();
        halt(frameInterval);
      }
      minutes++;
    }
    return minutes - 1;
  }

  private boolean fullyOxygenated() {
    return grid.values().stream().noneMatch(i -> i == SPACE);
  }
}
