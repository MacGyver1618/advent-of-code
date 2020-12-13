import java.util.*;
import java.util.stream.*;

public class Advent20 extends Advent {

  Map<Point, Character> grid;
  Map<Point, String> portals;
  Map<Point, Set<Point>> neighbors;

  Point startPosition;

  static final int NORTH = 1;
  static final int SOUTH = 2;
  static final int WEST = 3;
  static final int EAST = 4;

  static Map<Integer, Point> directions = new HashMap<>() {{
    put(NORTH, new Point(0,-1));
    put(SOUTH, new Point(0,1));
    put(WEST, new Point(-1,0));
    put(EAST, new Point(1,0));
  }};

  int xmin = Integer.MAX_VALUE;
  int xmax = Integer.MIN_VALUE;
  int ymin = Integer.MAX_VALUE;
  int ymax = Integer.MIN_VALUE;

  public Advent20() {
    super(20);
  }

  @Override
  protected void parseInput() {
    populateGrid();
    populatePortals();
    populateNeighbors();
  }

  void populateGrid() {
    grid = new TreeMap<>();
    for (int y = 0; y < input.size(); y++) {
      if (y < ymin)  ymin = y;
      if (y > ymax)  ymax = y;
      String line = input.get(y);
      for (int x = 0; x < line.length(); x++) {
        if (x < xmin)  xmin = x;
        if (x > xmax)  xmax = x;
        Point p = new Point(x,y);
        char c = line.charAt(x);
        grid.put(p, c);
      }
    }
  }

  void populatePortals() {
    portals = new TreeMap<>();
    for (Point p : grid.keySet()) {
      if (grid.get(p) == '.' && isPortal(p)) {
        String label = portalLabelOf(p);
        portals.put(p, label);
      }
    }
  }

  private boolean isPortal(Point p) {
    return immediateNeighbors(p).stream()
      .anyMatch(this::isLetter);
  }

  List<Point> immediateNeighbors(Point p) {
    return Arrays.asList(NORTH, SOUTH, EAST, WEST).stream()
      .map(d -> directions.get(d).add(p))
      .collect(Collectors.toList());
  }

  private String portalLabelOf(Point p) {
    Point neighbor = immediateNeighbors(p).stream()
        .filter(this::isLetter)
        .findFirst()
        .orElseThrow(IllegalStateException::new);
    Point difference = neighbor.subtract(p);
    Point next = neighbor.add(difference);
    if (difference.x < 0 || difference.y < 0) {
      return ""  + grid.get(next) + grid.get(neighbor);
    } else {
      return ""  + grid.get(neighbor) + grid.get(next);
    }
  }

  private boolean isLetter(Point p) {
    char fromGrid = grid.getOrDefault(p, '#');
    return fromGrid >= 'A' && fromGrid <= 'Z';
  }

  private void populateNeighbors() {
    neighbors = new TreeMap<>();
    for (var entry : grid.entrySet()) {
      if (entry.getValue() != '.') {
        continue;
      }
      Set<Point> result = new TreeSet<>();
      Point p = entry.getKey();
      if (portals.containsKey(p) && !portals.get(p).equals("AA") && !portals.get(p).equals("ZZ")) {
        result.add(portalPairOf(p));
      }
      result.addAll(immediateNeighbors(p).stream()
        .filter(n -> grid.get(n) == '.')
        .collect(Collectors.toList()));
      neighbors.put(p, result);
    }
  }

  private Point portalPairOf(Point p) {
    String label = portalLabelOf(p);
    return portals.entrySet().stream()
      .filter(n -> !n.getKey().equals(p))
      .filter(n -> n.getValue().equals(label))
      .map(n -> n.getKey())
      .findFirst()
      .orElseThrow(IllegalStateException::new);
  }

  private void printGrid() {
    StringBuffer sb = new StringBuffer();
    for (int y = ymin; y <= ymax; y++) {
      for (int x = xmin; x <= xmax; x++) {
        Point p = new Point(x,y);
        char c = grid.get(p);
        sb.append(c);
        sb.append(' ');
      }
      sb.append('\n');
    }
    sopl(sb.toString());
  }

  @Override
  protected Object part1() {
    Point start = pointByLabel("AA");
    Point goal = pointByLabel("ZZ");
    return shortestRoute(start, goal);
  }

  Point pointByLabel(String label) {
    return portals.entrySet().stream()
      .filter(e -> e.getValue().equals(label))
      .map(e -> e.getKey())
      .findFirst()
      .orElseThrow(NoSuchElementException::new);
  }

  private int shortestRoute(Point start, Point goal) {
    Map<Point, Integer> distances = new HashMap<>();
    Map<Point, Point> parents = new HashMap<>();

    Queue<Point> queue = new PriorityQueue<>(
      Comparator.comparing(
        (Point p) -> distances.getOrDefault(p, Integer.MAX_VALUE)));

    distances.put(start, 0);
    for(Point neighbor : neighbors.get(start)) {
      distances.put(neighbor, 1);
      parents.put(neighbor, start);
      queue.add(neighbor);
    }

    while (!queue.isEmpty()) {
      Point current = queue.poll();
      if (current.equals(goal)) {
        return distances.get(current);
      }
      for (Point neighbor : neighbors.get(current)) {
        int distance = distances.get(current) + 1;
        if (!distances.containsKey(neighbor)) {
          queue.add(neighbor);
        }
        if (distance < distances.getOrDefault(neighbor, Integer.MAX_VALUE)) {
          distances.put(neighbor, distance);
          parents.put(neighbor, current);
        }
      }
    }
    return -1;
  }

  @Override
  protected Object part2() {
    Point aa = pointByLabel("AA");
    Point zz = pointByLabel("ZZ");
    Point3 start = new Point3(aa.x, aa.y, 0);
    Point3 goal = new Point3(zz.x, zz.y, 0);
    return shortestRouteRecursive(start, goal);
  }

  private int shortestRouteRecursive(Point3 start, Point3 goal) {
    Map<Point3, Integer> distances = new HashMap<>();
    Map<Point3, Point3> parents = new HashMap<>();

    Queue<Point3> queue = new PriorityQueue<>(
      Comparator.comparing(
        (Point3 p) -> distances.getOrDefault(p, Integer.MAX_VALUE)));

    distances.put(start, 0);
    for(Point3 neighbor : neighbors(start)) {
      distances.put(neighbor, 1);
      parents.put(neighbor, start);
      queue.add(neighbor);
    }

    while (!queue.isEmpty()) {
      Point3 current = queue.poll();
      if (current.equals(goal)) {
        return distances.get(current);
      }
      for (Point3 neighbor : neighbors(current)) {
        int distance = distances.get(current) + 1;
        if (!distances.containsKey(neighbor)) {
          queue.add(neighbor);
        }
        if (distance < distances.getOrDefault(neighbor, Integer.MAX_VALUE)) {
          distances.put(neighbor, distance);
          parents.put(neighbor, current);
        }
      }
    }
    return -1;
  }

  Set<Point3> neighbors(Point3 p3) {
    Point p2 = new Point(p3.x, p3.y);
    if (isPortal(p2) && !portals.get(p2).equals("AA") && !portals.get(p2).equals("ZZ")) {
      return portalNeighbors(p3);
    } else {
      return neighbors.get(p2).stream()
        .map(p -> new Point3(p.x, p.y, p3.z))
        .collect(Collectors.toSet());
    }
  }

  Set<Point3> portalNeighbors(Point3 p3) {
    Point p2 = new Point(p3.x, p3.y);
    String label = portals.get(p2);
    var neighbors = immediateNeighbors(p2).stream()
    .filter(p -> grid.get(p) == '.')
    .map(p -> new Point3(p.x, p.y, p3.z))
    .collect(Collectors.toSet());
    var pair = portalPairOf(p2);
    if (isOuterPortal(p2)) {
      if (p3.z == 0) return neighbors;
      neighbors.add(new Point3(pair.x, pair.y, p3.z - 1));
    } else {
      neighbors.add(new Point3(pair.x, pair.y, p3.z + 1));
    }
    return neighbors;
  }

  boolean isOuterPortal(Point p) {
    return p.x == xmin + 2 || p.x == xmax - 2 || p.y == ymin + 2 || p.y == ymax - 2;
  }
}
