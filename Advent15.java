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
    parseElfPower(3);
  }

  private void parseElfPower(int power) {
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
          unit.power = c == 'E' ? power : 3;
          units.add(unit);
        }
      }
    }
  }

  @Override
  protected String part1() {
    String result = playGame(false);
    return "" + Integer.parseInt(result.substring(1))*hitPointsRemaining();
  }

  private String playGame(boolean throwOnElfDeath) {
    int rounds = 0;
    try {
      while (true) {
        for (Unit unit : units()) {
          if (unit.hp < 1) continue;
          if (!canFight(unit)) {
            moveTowardTarget(unit);
          }
          attackClosest(unit, throwOnElfDeath);
        }
        rounds++;
      }
    } catch (RuntimeException e) {
      return e.getMessage() + rounds;
    }
  }

  private List<Unit> units() {
    return units.stream()
                .filter(u -> u.hp > 0)
                .sorted(Unit.comparator())
                .collect(Collectors.toList());
  }

  private boolean canFight(Unit unit) {
    char opponent = unit.c == 'E' ? 'G' : 'E';
    return adjacent(unit.position).stream()
                                  .map(p -> grid[p.x][p.y])
                                  .anyMatch(c -> c == opponent);
  }

  private void moveTowardTarget(Unit unit) {
    List<Unit> targets = findTargets(unit);
    if (targets.isEmpty()) {
      throw new RuntimeException("" + unit.c);
    }
    Point nextStep = nextStep(unit, targets);
    if (nextStep == null) {
      return;
    }
    grid[unit.position.x][unit.position.y] = '.';
    unit.position = nextStep;
    grid[unit.position.x][unit.position.y] = unit.c;
  }

  private List<Unit> findTargets(Unit unit) {
    return units().stream()
                  .filter(u -> u.c != unit.c)
                  .collect(Collectors.toList());
  }

  private Point nextStep(Unit unit, List<Unit> targets) {
    List<Point> pointsInRange = pointsInRange(targets);
    pointsInRange.sort(Comparator.comparing(p -> p.manhattanDistance(unit.position)));
    List<Point> shortestPath = findShortestPath(unit.position, pointsInRange);
    return findBestOrigin(shortestPath);
  }

  private List<Point> pointsInRange(List<Unit> targets) {
    Set<Point> set = new TreeSet<>(Point.yComparator());
    targets.forEach(target -> set.addAll(freeAdjacentTo(target.position)));
    return new ArrayList<>(set);
  }

  private List<Point> findShortestPath(Point origin, List<Point> destinations) {
    List<Point> shortestPath = null;
    Point closestDestination = null;
    int minDistance = Integer.MAX_VALUE;
    for (Point destination : destinations) {
      List<Point> path = pathFrom(origin, destination, minDistance);
      if (path != null) {
        int length = path.size();
        Point end = path.get(length - 1);
        if (closestDestination == null || length < minDistance) {
          minDistance = length;
          closestDestination = end;
          shortestPath = path;
        } else if (length == minDistance) {
          if (Point.yComparator().compare(end, destination) < 0) {
            destination = end;
            shortestPath = path;
          }
        }
      }
    }
    return shortestPath;
  }

  private Point findBestOrigin(List<Point> path) {
    if (path == null) {
      return null;
    }
    int length = path.size();
    Point origin = path.get(0);
    Point destination = path.get(length - 1);
    return freeAdjacentTo(origin).stream()
                                 .map(p -> pathFrom(p, destination))
                                 .filter(l -> l != null && l.size() == length - 1)
                                 .map(l -> l.get(0))
                                 .sorted(Point.yComparator())
                                 .findFirst()
                                 .orElse(null);
  }

  private Set<Point> freeAdjacentTo(Point point) {
    return adjacent(point).stream()
                          .filter(p -> charAt(p) == '.')
                          .collect(Collectors.toSet());
  }

  private void attackClosest(Unit unit, boolean throwOnElfDeath) {
    List<Unit> opponents = adjacentOpponents(unit);
    if (!opponents.isEmpty()) {
      opponents.sort(Comparator.comparing((Unit u) -> u.hp)
                               .thenComparing((Unit u) -> u.position.y)
                               .thenComparing((Unit u) -> u.position.x));
      Unit opponent = opponents.get(0);
      opponent.hp -= unit.power;
      if (opponent.hp < 1) {
        if (throwOnElfDeath && opponent.c == 'E') {
          throw new RuntimeException("G");
        }
        grid[opponent.position.x][opponent.position.y] = '.';
      }
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

  private long hitPointsRemaining() {
    return units().stream()
                  .mapToInt(u -> u.hp)
                  .filter(i -> i > 0)
                  .sum();
  }

  private Unit unitAt(Point p) {
    return units().stream().filter(u -> u.position.equals(p)).findFirst().orElse(null);
  }

  private char charAt(Point p) {
    return grid[p.x][p.y];
  }

  private List<Unit> opponents(Unit unit) {
    return units().stream()
                  .filter(u -> u.c != unit.c)
                  .collect(Collectors.toList());
  }

  @Override
  protected String part2() {
    String result;
    char c = '\0';
    int power = 3;
    do {
      power++;
      parseElfPower(power);
      result = playGame(true);
      c = result.charAt(0);
    } while(c != 'E');
    int rounds = Integer.parseInt(result.substring(1));
    return "" + rounds*hitPointsRemaining();
  }

  static class Unit {

    static Comparator<Unit> comparator =
      Comparator.comparing((Unit u) -> u.position.y)
                .thenComparing((Unit u) -> u.position.x);

    char c;
    int hp;
    Point position;
    int power;

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

  private List<Point> pathFrom(Point start, Point goal) {
    return pathFrom(start, goal, Integer.MAX_VALUE);
  }

  private List<Point> pathFrom(Point start, Point goal, int maxLength) {
    Set<Point> closedSet = new TreeSet<>(Point.yComparator());
    Set<Point> openSet = new TreeSet<>(Point.yComparator());
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
      if (gScore.getOrDefault(current, Integer.MAX_VALUE) > maxLength) {
        return null;
      }

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

  private Set<Point> neighbors(Point point, Point goal) {
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

  private Set<Point> adjacent(Point point) {
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
