import java.util.*;
import java.util.stream.*;

public class Advent15 extends Advent {

  int attackPower = 3;
  int initialHp = 200;

  int xMax;
  int yMax;
  char[][] grid;
  List<Unit> units;

  public Advent15() {
    super(15);
  }

  @Override
  protected void parseInput() {
    //debug = true;
    xMax = input.get(0).length();
    yMax = input.size();
    grid = new char[xMax][yMax];
    units = new LinkedList<Unit>();
    for (int y = 0; y < yMax; y++) {
      String line = input.get(y);
      for (int x = 0; x < xMax; x++) {
        char c = line.charAt(x);
        grid[x][y] = c;
        if (c == 'E' || c == 'G') {
          Unit unit = new Unit();
          unit.hp = initialHp;
          unit.c = c;
          unit.position = new Point(x,y);
          units.add(unit);
        }
      }
    }
  }

  private void printGrid() {
    for (int x = 0; x < xMax; x++) {
      if (x % 5 == 0 && x / 10 > 0) {
        sop(x / 10);
      } else {
        sop(' ');
      }
    }
    sopl();
    for (int x = 0; x < xMax; x++) {
      if (x % 5 == 0) {
        sop(x % 10);
      } else {
        sop(' ');
      }
    }
    sopl();
    for (int y = 0; y < yMax; y++) {
      for (int x = 0; x < xMax; x++) {
        char c = grid[x][y];
        sop(c == '.' ? ' ' : c);
      }
      sopl(" " + y);
    }
  }

  @Override
  protected String part1() {
    printAndPause("Initial state");
    int fullRounds = 0;
    while (bothFactionsAlive()) {
      for (Unit unit : units()) {
        if (!bothFactionsAlive()) {
          fullRounds--;
          break;
        }
        if (unit.hp < 1) continue;
        if (!canFight(unit)) {
          move(unit);
        }
        attackClosest(unit);
      }
      fullRounds++;
      printAndPause("After ", fullRounds, " full rounds");
    }
    units().forEach(Advent::sopl);
    return "" + fullRounds*hitPointsRemaining();
  }

  private void printAndPause() {
    printAndPause(new Object[0]);
  }

  private void printAndPause(Object... args) {
    if (debug) {
      printGrid();
      if (args.length != 0) {
        sopl(args);
      }
      pause();
    }
  }

  private long hitPointsRemaining() {
    return units().stream()
                  .mapToInt(u -> u.hp)
                  .filter(i -> i > 0)
                  .sum();
  }

  private boolean bothFactionsAlive() {
    return units().stream()
                  .map(u -> u.c)
                  .distinct()
                  .count() == 2;
  }

  private boolean canFight(Unit unit) {
    char opponent = unit.c == 'E' ? 'G' : 'E';
    return adjacent(unit.position).stream()
                                  .map(p -> grid[p.x][p.y])
                                  .anyMatch(c -> c == opponent);
  }

  private void attackClosest(Unit unit) {
    List<Unit> opponents = adjacentOpponents(unit);
    if (!opponents.isEmpty()) {
      opponents.sort(Comparator.comparing((Unit u) -> u.hp));
                               //.thenComparing((Unit u) -> u.position.y)
                               //.thenComparing((Unit u) -> u.position.x));
      attack(unit, opponents.get(0));
    }
  }

  private void attack(Unit unit, Unit opponent) {
    printAndPause(unit, " attacking ", opponent);
    opponent.hp -= attackPower;
    if (opponent.hp < 1) {
      grid[opponent.position.x][opponent.position.y] = '.';
      printAndPause(opponent, " died!");
    }
  }

  private List<Unit> adjacentOpponents(Unit unit) {
    List<Unit> result = new LinkedList<>();
    for (Point p : adjacent(unit.position)) {
      Unit other = unitAt(p);
      if (other == null || other.c == unit.c) {
        continue;
      }
      result.add(other);
    }
    return result;
  }

  private Unit unitAt(Point p) {
    return units().stream().filter(u -> u.position.equals(p)).findFirst().orElse(null);
  }

  private char charAt(Point p) {
    return grid[p.x][p.y];
  }

  private void move(Unit unit) {
    List<Point> path = findShortestPath(unit);
    if (path != null && !path.isEmpty()) {
      Point currentPosition = unit.position;
      Point nextPosition = path.get(0);
      grid[currentPosition.x][currentPosition.y] = '.';
      grid[nextPosition.x][nextPosition.y] = unit.c;
      unit.position = nextPosition;
      printAndPause(unit, " moved to ", nextPosition);
    } else {
      printAndPause(unit, " cannot move");
    }
  }

  private List<Point> findShortestPath(Unit unit) {
    List<Point> path;
    List<Point> shortestPath = null;
    for (Unit opponent : opponents(unit)) {
      path = pathFrom(unit, opponent);
      if (path == null) {
        continue;
      }
      path = path.subList(1, path.size() - 1);
      if (shortestPath == null || path.size() < shortestPath.size()) {
        shortestPath = path;
      } else if (path.size() == shortestPath.size() && path.size() > 0) {
        Point headCurrent = shortestPath.get(0);
        Point headOther = shortestPath.get(0);
        if (Point.yComparator().compare(headOther, headCurrent) < 0) {
          shortestPath = path;
        }
      }
    }
    return shortestPath;
  }

  private List<Unit> opponents(Unit unit) {
    return units().stream()
                  .filter(u -> u.c != unit.c)
                  .collect(Collectors.toList());
  }

  private List<Unit> units() {
    return units.stream()
                .filter(u -> u.hp > 0)
                .sorted(Unit.comparator())
                .collect(Collectors.toList());
  }

  @Override
  protected String part2() {
    return "";
  }

  static class Unit {

    static Comparator<Unit> comparator =
      Comparator.comparing((Unit u) -> u.position.y)
                .thenComparing((Unit u) -> u.position.x);

    char c;
    int hp;
    Point position;

    @Override
    public String toString() {
      StringBuilder sb = new StringBuilder();
      return sb.append(c == 'E' ? "Elf" : "Goblin")
               .append(" (" + hp + " hp)")
               .append(" at ")
               .append(position)
               .toString();
    }

    static Comparator<Unit> comparator() {
      return comparator;
    }
  }

  enum Direction {
    UP(new Point(0,-1)),
    LEFT(new Point(-1,0)),
    RIGHT(new Point(1,0)),
    DOWN(new Point(0,1));

    Point velocity;

    Direction(Point p) {
      this.velocity = p;
    }
  }

  List<Point> pathFrom(Unit unit, Unit opponent) {
    return pathFrom(unit.position, opponent.position);
  }

  List<Point> pathFrom(Point start, Point goal) {
    Set<Point> closedSet = new TreeSet<>(Point.yComparator());
    Queue<Point> openSet = new ArrayDeque<>();
    openSet.add(start);

    Map<Point, Point> cameFrom = new TreeMap<>(Point.yComparator());
    Map<Point, Integer> gScore = new TreeMap<>(Point.yComparator());
    gScore.put(start, 0);

    Map<Point, Integer> fScore = new TreeMap<>(Point.yComparator());
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

      for (Point neighbor : neighbors(current, goal)) {
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

  List<Point> reconstructPath(Map<Point, Point> cameFrom, Point current) {
    List<Point> totalPath = new LinkedList<>();
    totalPath.add(current);
    while (cameFrom.containsKey(current)) {
      current = cameFrom.get(current);
      totalPath.add(current);
    }
    Collections.reverse(totalPath);
    return totalPath;
  }

  Set<Point> neighbors(Point point, Point goal) {
    Set<Point> result = new TreeSet<>(Point.yComparator());
    for (Point adjacent : adjacent(point)) {
      if (canAdvanceTo(adjacent, goal)) {
        result.add(adjacent);
      }
    }
    return result;
  }

  private boolean canAdvanceTo(Point point, Point goal) {
    return goal.equals(point) || grid[point.x][point.y] == '.';
  }

  Set<Point> adjacent(Point point) {
    Set<Point> result = new TreeSet<>(Point.yComparator());
    for (Direction direction : Direction.values()) {
      Point candidate = point.add(direction.velocity);
      if (outOfBounds(candidate)) {
        continue;
      }
      result.add(candidate);
    }
    return result;
  }

  private boolean outOfBounds(Point p) {
    return p.x < 0 || p.x >= xMax || p.y <0 || p.y >= yMax;
  }
}
