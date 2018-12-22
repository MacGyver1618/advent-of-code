import java.util.*;
import java.util.stream.*;

public class Advent22 extends Advent {

  private int depth = 3879;
  private Point target = new Point(8, 713);
  private Point extent = target;
  //private int depth = 510;
  //private Point target = new Point(10, 10);
  //private Point extent = new Point(16, 16);
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
                       .filter(e -> !e.getKey().equals(origin))
                       .filter(e -> !e.getKey().equals(target))
                       .mapToInt(e -> e.getValue().riskLevel)
                       .sum();
  }

  private void printGrid(int xMax, int yMax) {
    StringBuilder sb = new StringBuilder();
    for (int y = 0; y <= yMax; y++) {
      for (int x = 0; x <= xMax; x++) {
        Point p = new Point(x, y);
        Region r = regions.get(p);
        sopl(p);
        char c;
        if (p.equals(origin)) {
          c = 'M';
        } else if (p.equals(target)) {
          c = 'T';
        } else {
          c = r.riskLevel == 0 ? '.' : r.riskLevel == 1 ? '=' : '|';
        }
        sb.append(c);
      }
      sb.append('\n');
    }
    System.out.print(sb.toString());
  }

  private int geologicIndex(Point p) {
    if (p.equals(origin)) return 0;
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

  private Type regionType(Point p) {
    return regionType(erosionLevel(p) % 3);
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
    Position start = new Position(origin, Tool.TORCH);
    Position end = new Position(target, Tool.TORCH);
    return "" + pathFrom(start, end).size();
  }

  private Set<Point> adjacent(Point p) {
    Set<Point> result = new TreeSet<>();
    if (p.x > 0) result.add(new Point(p.x-1, p.y));
    if (p.y > 0) result.add(new Point(p.x, p.y-1));
    result.add(new Point(p.x+1, p.y));
    result.add(new Point(p.x, p.y+1));
    return result;
  }

  private List<Position> pathFrom(Position start, Position goal) {
    Set<Position> closedSet = new HashSet<>();
    Set<Position> openSet = new HashSet<>();
    openSet.add(start);

    Map<Position, Position> cameFrom = new HashMap<>();
    Map<Position, Integer> gScore = new HashMap<>();
    gScore.put(start, 0);

    Map<Position, Integer> fScore = new HashMap<>();
    fScore.put(start, start.point.manhattanDistance(goal.point));

    while (!openSet.isEmpty()) {
      Position current = openSet.stream()
                                .sorted(Comparator.comparing(p -> fScore.getOrDefault(p, Integer.MAX_VALUE)))
                                .findFirst()
                                .orElseThrow(IllegalStateException::new);

      if (current.point.equals(goal.point)) {
        return reconstructPath(cameFrom, current);
      }

      openSet.remove(current);
      closedSet.add(current);

      for (Position neighbor : neighbors(current)) {
        if (closedSet.contains(neighbor)) {
          continue;
        }
        int tentative_gScore = gScore.getOrDefault(current, Integer.MAX_VALUE-1) + distanceBetween(current, neighbor);
        if (!openSet.contains(neighbor)) {
          openSet.add(neighbor);
        } else if (tentative_gScore >= gScore.getOrDefault(neighbor, Integer.MAX_VALUE-1)) {
          continue;
        }

        cameFrom.put(neighbor, current);
        gScore.put(neighbor, tentative_gScore);
        fScore.put(neighbor, gScore.get(neighbor) + neighbor.point.manhattanDistance(goal.point));
      }
    }
    return null;
  }

  private int distanceBetween(Position a, Position b) {
    return a.point.equals(b.point) ? 7 : 1;
  }

  private Set<Position> neighbors(Position pos) {
    Set<Position> result = new HashSet<>();
    result.add(allowedGearChange(pos));
    result.addAll(adjacent(pos.point).stream()
                                     .filter(p -> canAdvance(pos, p))
                                     .map(p -> new Position(p, pos.tool))
                                     .collect(Collectors.toSet()));
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
    return new Position(pos.point, newTool);
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

  class Position {
    Point point;
    Tool tool;
    Type type;

    Position(Point point, Tool tool) {
      this.point = point;
      this.tool = tool;
      this.type = getType(point);
    }

    public int hashCode() {
      return point.hashCode();
    }

    public boolean equals(Object o) {
      Position other = (Position) o;
      return other.point.equals(this.point) && other.tool == this.tool;
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
