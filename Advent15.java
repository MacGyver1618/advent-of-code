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
          unit.power = c == 'E' ? power : 3;
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
    int fullRounds = 0;
    while (bothFactionsAlive()) {
      for (Unit unit : units()) {
        if (unit.hp < 1) continue;
        if (!canFight(unit)) {
          List<Unit> targets = findTargets(unit);
          if (targets.isEmpty()) {
            return "" + fullRounds*hitPointsRemaining();
          }
          Set<Point> pointsInRange = pointsInRange(targets);
          printReplacing(pointsInRange, '?', "In range");
          Set<Point> reachablePoints = pointsInRange.stream()
                                                    .filter(p -> pathFrom(unit.position, p) != null)
                                                    .collect(Collectors.toSet());
          if (reachablePoints.isEmpty()) {
            continue;
          }
          printReplacing(reachablePoints, '@', "Reachable");
          Set<List<Point>> paths = reachablePoints.stream()
                                                  .map(p -> pathFrom(unit.position, p))
                                                  .collect(Collectors.toSet());
          int minDistance = paths.stream()
                                 .mapToInt(l -> l.size())
                                 .min()
                                 .orElseThrow(IllegalStateException::new);
          Set<List<Point>> shortestPaths = paths.stream()
                                                 .filter(p -> p.size() == minDistance)
                                                 .collect(Collectors.toSet());
          Set<Point> nearestPoints = shortestPaths.stream()
                                                  .map(l -> l.get(l.size() -1))
                                                  .collect(Collectors.toSet());
          printReplacing(nearestPoints, '!', "Nearest");
          Point chosenPoint = nearestPoints.stream()
                                           .sorted(Point.yComparator())
                                           .findFirst()
                                           .orElse(null);
          printReplacing(Set.of(chosenPoint), '+', "Chosen");
          Set<Point> freeNeighbors = freeAdjacentTo(unit.position);
          printDistancesTo(chosenPoint, freeNeighbors);
          Point nextStep = freeNeighbors.stream()
                                        .filter(p -> {
                                          List<Point> l = pathFrom(p, chosenPoint);
                                          return l != null && l.size() == minDistance - 1;
                                        })
                                        .sorted(Point.yComparator())
                                        .findFirst()
                                        .orElse(null);
          printReplacing(new TreeSet<Point>(pathFrom(nextStep, chosenPoint)), '*', "Chosen path");
          grid[unit.position.x][unit.position.y] = '.';
          unit.position = nextStep;
          grid[unit.position.x][unit.position.y] = unit.c;
        }
        attackClosest(unit);
      }
      fullRounds++;
      printGrid();
      sopl("Round ", fullRounds);
      printAndPause("After ", fullRounds, " full rounds");
    }
    sopl();
    units().forEach(Advent::sopl);
    return "" + fullRounds*hitPointsRemaining();

  }

  private void printDistancesTo(Point to, Set<Point> froms) {
    if (!debug) return;
    Map<Point, Character> chars = new TreeMap<>(Point.yComparator());
    Map<Character, Integer> dists = new TreeMap<>();
    char c = 'A';
    for (Point from : froms) {
      var path = pathFrom(from, to);
      if (path == null) continue;
      grid[from.x][from.y] = c;
      dists.put(c, path.size());
      c++;
    }
    sopl("Distances");
    sopl(dists);
    printAndPause();
    for (Point point : froms) {
      grid[point.x][point.y] = '.';
    }
  }

  private void printReplacing(Set<Point> points, char c, String message) {
    if (!debug) return;
    for (Point point : points) {
      grid[point.x][point.y] = c;
    }
    sopl(message);
    printAndPause();
    for (Point point : points) {
      grid[point.x][point.y] = '.';
    }
  }

  private List<Unit> findTargets(Unit unit) {
    return units().stream()
                  .filter(u -> u.c != unit.c)
                  .collect(Collectors.toList());
  }

  private Set<Point> pointsInRange(List<Unit> targets) {
    Set<Point> result = new TreeSet<>(Point.yComparator());
    for (Unit target : targets) {
      result.addAll(freeAdjacentTo(target.position));
    }
    return result;
  }

  private Set<Point> freeAdjacentTo(Point point) {
    return adjacent(point).stream()
                          .filter(p -> charAt(p) == '.')
                          .collect(Collectors.toSet());
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
    opponent.hp -= unit.power;
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

  private void move(Unit unit, Set<Point> destinations) {
    Set<List<Point>> shortestPaths = new TreeSet<>();
    for (Point point : freeAdjacentTo(unit.position)) {
      List<Point> path = findShortestPath(point, destinations);
    }
    List<Point> path = shortestPaths.stream()
                                    .filter(l -> l != null)
                                    .sorted(Comparator.comparing((List<Point> l) -> l.size())
                                                      .thenComparing((List<Point> l) -> l.get(0).y)
                                                      .thenComparing((List<Point> l) -> l.get(0).x))
                                    .findFirst()
                                    .orElse(null);
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

  private List<Point> findShortestPath(Point start, Set<Point> targets) {
    Point closestPoint = null;
    List<Point> path;
    List<Point> shortestPath = null;
    for (Point finish : targets) {
      if (closestPoint == null) {
        closestPoint = finish;
      }
      path = pathFrom(start, finish);
      if (path == null) {
        continue;
      }
      if (shortestPath == null || path.size() < shortestPath.size()) {
        shortestPath = path;
      } else if (path.size() == shortestPath.size() && path.size() > 0) {
        if (finish.y < closestPoint.y || finish.y == closestPoint.y && finish.x < closestPoint.x) {
          closestPoint = finish;
          shortestPath = path;
        }
      }
    }
    return shortestPath;
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
    String result;
    char c = '\0';
    int power = 16;
    do {
      power++;
      parseElfPower(power);
      result = playGame();
      c = result.charAt(0);
      sopl((c == 'G' ? "Goblins" : "Elves"), " win with elf power ", power);
    } while(c != 'E');
    int rounds = Integer.parseInt(result.substring(1));
    return "" + rounds*hitPointsRemaining();
  }

  private String playGame() {
    int rounds = 0;
    try {
      while (bothFactionsAlive()) {
        for (Unit unit : units()) {
          if (unit.hp < 1) continue;
          if (!canFight(unit)) {
            List<Unit> targets = findTargets(unit);
            if (targets.isEmpty()) {
              return "" + unit.c + rounds;
            }
            Set<Point> pointsInRange = pointsInRange(targets);
            Set<Point> reachablePoints = pointsInRange.stream()
                                                      .filter(p -> pathFrom(unit.position, p) != null)
                                                      .collect(Collectors.toSet());
            if (reachablePoints.isEmpty()) {
              continue;
            }
            Set<List<Point>> paths = reachablePoints.stream()
                                                    .map(p -> pathFrom(unit.position, p))
                                                    .collect(Collectors.toSet());
            int minDistance = paths.stream()
                                   .mapToInt(l -> l.size())
                                   .min()
                                   .orElseThrow(IllegalStateException::new);
            Set<List<Point>> shortestPaths = paths.stream()
                                                   .filter(p -> p.size() == minDistance)
                                                   .collect(Collectors.toSet());
            Set<Point> nearestPoints = shortestPaths.stream()
                                                    .map(l -> l.get(l.size() -1))
                                                    .collect(Collectors.toSet());
            Point chosenPoint = nearestPoints.stream()
                                             .sorted(Point.yComparator())
                                             .findFirst()
                                             .orElse(null);
            Set<Point> freeNeighbors = freeAdjacentTo(unit.position);
            Point nextStep = freeNeighbors.stream()
                                          .filter(p -> {
                                            List<Point> l = pathFrom(p, chosenPoint);
                                            return l != null && l.size() == minDistance - 1;
                                          })
                                          .sorted(Point.yComparator())
                                          .findFirst()
                                          .orElse(null);
            grid[unit.position.x][unit.position.y] = '.';
            unit.position = nextStep;
            grid[unit.position.x][unit.position.y] = unit.c;
          }
          attackClosestThrowing(unit);
        }
        printGrid();
        sopl("Round ", ++rounds);
      }
    } catch (RuntimeException e) {
      return "G" + rounds;
    }
    return "";
  }

  private void attackClosestThrowing(Unit unit) {
    List<Unit> opponents = adjacentOpponents(unit);
    if (!opponents.isEmpty()) {
      opponents.sort(Comparator.comparing((Unit u) -> u.hp));
                               //.thenComparing((Unit u) -> u.position.y)
                               //.thenComparing((Unit u) -> u.position.x));
      attackThrowing(unit, opponents.get(0));
    }
  }

  private void attackThrowing(Unit unit, Unit opponent) {
    printAndPause(unit, " attacking ", opponent);
    opponent.hp -= unit.power;
    if (opponent.hp < 1) {
      if (opponent.c == 'E') {
        throw new RuntimeException("Elf dead");
      }
      grid[opponent.position.x][opponent.position.y] = '.';
      printAndPause(opponent, " died!");
    }
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

  List<Point> pathFrom(Unit unit, Unit opponent) {
    return pathFrom(unit.position, opponent.position);
  }

  List<Point> pathFrom(Point start, Point goal) {
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
