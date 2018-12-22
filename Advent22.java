import java.util.*;
import java.util.stream.*;

public class Advent22 extends Advent {

  private int depth = 3879;
  private Point target = new Point(8, 713);
  private int buffer = 50;
  private Point extent = target.add(new Point(buffer, buffer));
  Point origin = new Point(0,0);
  Map<Point, Region> regions = new TreeMap<>();

  public Advent22() {
    super(22);
  }

  @Override
  protected void readInput() {}

  @Override
  protected void parseInput() {
    for (int y = 0; y <= extent.y; y++) {
      for (int x = 0; x <= extent.x; x++) {
        Point p = new Point(x,y);
        addRegion(p);
      }
    }
  }

  private void addRegion(Point p) {
    Region r = new Region();
    r.geologicIndex = geologicIndex(p);
    r.erosionLevel = erosionLevel(p);
    r.riskLevel = r.erosionLevel % 3;
    r.type = regionType(r.riskLevel);
    regions.put(p, r);
  }

  @Override
  protected String part1() {
    return "" + regions.entrySet()
                       .stream()
                       .filter(e -> e.getKey().x <= target.x)
                       .filter(e -> e.getKey().y <= target.y)
                       .mapToInt(e -> e.getValue().riskLevel)
                       .sum();
  }

  private int geologicIndex(Point p) {
    if (p.equals(origin)) return 0;
    if (p.equals(target)) return 0;
    if (p.y == 0) return p.x*16807;
    if (p.x == 0) return p.y*48271;
    return erosionLevel(new Point(p.x-1, p.y))*erosionLevel(new Point(p.x, p.y-1));
  }

  private int erosionLevel(Point p) {
    int geoIndex;
    if (regions.containsKey(p)) {
      geoIndex = regions.get(p).geologicIndex;
    } else {
      geoIndex = geologicIndex(p);
    }
    return (geoIndex + depth) % 20183;
  }

  private Type regionType(int i) {
    switch (i) {
      case 0: return Type.ROCKY;
      case 1: return Type.WET;
      case 2: return Type.NARROW;
    }
    throw new IllegalArgumentException();
  }

  private int riskLevel(Point p) {
    return erosionLevel(p) % 3;
  }

  @Override
  protected String part2() {
    Position start = new Position(origin, Tool.TORCH, getType(origin));
    Position end = new Position(target, Tool.TORCH, getType(target));
    List<Position> path = pathFrom(start, end);
    return "" + countDistance(path);
  }

  private int countDistance(List<Position> positions) {
    Queue<Position> queue = new LinkedList<>(positions);
    Position current = queue.poll();
    Position previous = null;
    int distance = 0;
    while (!queue.isEmpty()) {
      previous = current;
      current = queue.poll();
      distance += distanceBetween(previous, current);
    }
    return distance;
  }

  private List<Position> pathFrom(Position start, Position goal) {
    Map<Position, Position> cameFrom = new TreeMap<>();
    Map<Position, Integer> distances = new TreeMap<>();
    Queue<Position> unvisited = new PriorityQueue<>(Comparator.comparing(p -> distances.getOrDefault(p, Integer.MAX_VALUE)));
    Set<Position> visited = new TreeSet<>();

    unvisited.add(start);
    distances.put(start, 0);

    while (!unvisited.isEmpty()) {
      Position current =  unvisited.poll();
      if (current.equals(goal)) {
        return reconstructPath(cameFrom, current);
      }
      unvisited.remove(current);
      visited.add(current);

      for (Position neighbor : neighbors(current)) {
        if (!visited.contains(neighbor)) {
          unvisited.add(neighbor);
        }
        int currentDistance = distances.getOrDefault(neighbor, Integer.MAX_VALUE);
        int alternateDistance = distances.get(current) + distanceBetween(current, neighbor);
        if (alternateDistance < currentDistance) {
          distances.put(neighbor, alternateDistance);
          cameFrom.put(neighbor, current);
        }
      }
    }
    throw new IllegalStateException("No path found!");
  }

  private int distanceBetween(Position a, Position b) {
    return a.point.equals(b.point) ? 7 : 1;
  }

  private Set<Position> neighbors(Position pos) {
    Set<Position> result = new HashSet<>();
    result.add(allowedGearChange(pos));
    result.addAll(adjacent(pos.point).stream()
                                     .filter(p -> canAdvance(pos, p))
                                     .map(p -> new Position(p, pos.tool, getType(p)))
                                     .collect(Collectors.toSet()));
    return result;
  }

  private Position allowedGearChange(Position pos) {
    Tool oldTool = pos.tool;
    Tool newTool = null;
    switch (pos.type) {
      case ROCKY:
        newTool = oldTool == Tool.TORCH ? Tool.CLIMBING_GEAR : Tool.TORCH;
        break;
      case WET:
        newTool = oldTool == Tool.CLIMBING_GEAR ? Tool.NEITHER : Tool.CLIMBING_GEAR;
        break;
      case NARROW:
        newTool = oldTool == Tool.NEITHER ? Tool.TORCH : Tool.NEITHER;
        break;
    }
    return new Position(pos.point, newTool, getType(pos.point));
  }

  private Set<Point> adjacent(Point p) {
    Set<Point> result = new TreeSet<>();
    if (p.x > 0) result.add(new Point(p.x-1, p.y));
    if (p.y > 0) result.add(new Point(p.x, p.y-1));
    if (p.x < extent.x) result.add(new Point(p.x+1, p.y));
    if (p.y < extent.y) result.add(new Point(p.x, p.y+1));
    return result;
  }


  private boolean canAdvance(Position from, Point to) {
    switch (getType(to)) {
      case ROCKY: return from.tool != Tool.NEITHER;
      case WET: return from.tool != Tool.TORCH;
      case NARROW: return from.tool != Tool.CLIMBING_GEAR;
    }
    throw new IllegalStateException();
  }

  private List<Position> reconstructPath(Map<Position, Position> cameFrom, Position current) {
    List<Position> totalPath = new LinkedList<>();
    totalPath.add(current);
    while (cameFrom.containsKey(current)) {
      current = cameFrom.get(current);
      totalPath.add(current);
    }
    Collections.reverse(totalPath);
    return totalPath;
  }

  private Type getType(Point p) {
    if (!regions.containsKey(p)) {
      addRegion(p);
    }
    return regions.get(p).type;
  }

  static class Position implements Comparable<Position> {

    static Comparator<Position> comparator = Comparator.comparing((Position p) -> p.point)
                                                       .thenComparing((Position p) -> p.tool);
    Point point;
    Tool tool;
    Type type;

    Position(Point point, Tool tool, Type type) {
      this.point = point;
      this.tool = tool;
      this.type = type;
    }

    public int hashCode() {
      return point.hashCode() + tool.ordinal();
    }

    public boolean equals(Object o) {
      Position other = (Position) o;
      return other.point.equals(this.point) && other.tool == this.tool;
    }

    public String toString() {
      return "At " + point + " with " + tool.name();
    }

    public int compareTo(Position other) {
      return comparator.compare(this, other);
    }
  }

  class Region {
    int geologicIndex;
    int erosionLevel;
    Type type;
    int riskLevel;
  }

  enum Type {
    ROCKY,
    WET,
    NARROW;
  }

  enum Tool {
    CLIMBING_GEAR,
    TORCH,
    NEITHER;
  }
}
