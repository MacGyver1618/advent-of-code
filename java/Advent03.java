import java.util.*;
import java.util.regex.*;
import java.util.stream.*;

public class Advent03 extends Advent {

  private List<List<Integer>> instructions = new LinkedList<>();
  private Map<Point, Integer> claims = new HashMap<>();
  private Pattern p = Pattern.compile("#(\\d+) @ (\\d+),(\\d+): (\\d+)x(\\d+)");
  private Map<Integer, Area> areas = new TreeMap<>();

  public Advent03() {
    super(3);
  }

  @Override
  protected void parseInput() {
    input.forEach(this::parseLine);
  }

  private void parseLine(String line) {
    Matcher m = p.matcher(line);
    if (m.find()) {
      int num = Integer.parseInt(m.group(1));
      int topX = Integer.parseInt(m.group(2));
      int topY = Integer.parseInt(m.group(3));
      int width = Integer.parseInt(m.group(4));
      int height = Integer.parseInt(m.group(5));
      areas.put(num, new Area(topX, topY, width, height));
    }
  }

  @Override
  protected String part1() {
    areas.values().forEach(this::populateFabric);
    return "" + countX();
  }

  private void populateFabric(Area area) {
    area.points().forEach(point -> claims.put(point, claims.getOrDefault(point, 0) + 1));
  }

  private long countX() {
    return claims.values()
                 .stream()
                 .mapToInt(Integer::intValue)
                 .filter(i -> i > 1)
                 .count();
  }

  @Override
  protected String part2() {
    return "" + areas.entrySet()
                     .stream()
                     .filter(e -> !hasOverlaps(e))
                     .map(Map.Entry::getKey)
                     .findFirst()
                     .orElseThrow(IllegalStateException::new);
  }

  private boolean hasOverlaps(Map.Entry<Integer, Area> entry) {
    return areas.entrySet()
                .stream()
                .filter(e -> e.getKey() != entry.getKey())
                .anyMatch(e -> e.getValue().overlaps(entry.getValue()));
  }

  static class Area {

    private int minX;
    private int minY;
    private int maxX;
    private int maxY;

    Area(int x, int y, int w, int h) {
      minX = x;
      maxX = x + w - 1;
      minY = y;
      maxY = y + h - 1;
    }

    Stream<Point> points() {
      return IntStream.rangeClosed(minX, maxX)
                      .boxed()
                      .flatMap(x -> pointsX(x));
    }

    private Stream<Point> pointsX(int x) {
      return IntStream.rangeClosed(minY, maxY)
                      .mapToObj(y -> new Point(x,y));
    }

    boolean overlaps(Area other) {
      return this.minX <= other.maxX
          && this.maxX >= other.minX
          && this.minY <= other.maxY
          && this.maxY >= other.minY;
    }
  }
}
