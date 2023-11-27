import java.io.*;
import java.util.*;
import java.util.function.*;
import java.util.stream.*;

public class Advent06 extends Advent {

  private static final int ORIGINAL_MAX = 400;
  private static final int BUFFER = 0;
  private static final int GRID_MAX = ORIGINAL_MAX + BUFFER;
  private static final int GRID_MIN = 0 - BUFFER;
  private List<Point> points = new LinkedList<>();
  private Map<Point, Integer> pointsGrid = new TreeMap<>();
  private Map<Point, Integer> distanceGrid = new TreeMap<>();
  private int[][] grid = new int[GRID_MAX - GRID_MIN][GRID_MAX - GRID_MIN];
  private Set<Integer> edges = new TreeSet<>();

  public Advent06() {
    super(6);
  }

  @Override
  protected void parseInput() {
    for (int i = 1; i <= input.size(); i++) {
      Point p = parsePoint(input.get(i-1));
      pointsGrid.put(p, i);
      points.add(p);
    }
    populateDistances();
    printGrid();
    populateEdges();
  }

  private Point parsePoint(String line) {
    String[] coords = line.split(", ");
    int x = Integer.parseInt(coords[0]);
    int y = Integer.parseInt(coords[1]);
    return new Point(x, y);
  }

  @Override
  protected String part1() {
    int max = countMax();
    return "" + max;
  }

  private void populateDistances() {
    for (int x = GRID_MIN; x < GRID_MAX; x++) {
      for (int y = GRID_MIN; y < GRID_MAX; y++) {
        Point current = new Point(x, y);
        int closest = findClosest(current);
        distanceGrid.put(current, closest);
        grid[x - GRID_MIN][y - GRID_MIN] = closest;
      }
    }
  }

  private int findClosest(Point p) {
    Map<Integer, Integer> distances = new TreeMap<>();
    for (Map.Entry<Point, Integer> entry : pointsGrid.entrySet()) {
      int distance = manhattanDistance(p, entry.getKey());
      distances.put(entry.getValue(), distance);
    }
    List<Map.Entry<Integer, Integer>> sortedDistances =
      distances.entrySet()
               .stream()
               .sorted(Map.Entry.comparingByValue())
               .collect(Collectors.toList());
    int first = sortedDistances.get(0).getValue();
    int second = sortedDistances.get(1).getValue();
    if (first == second) return 0;
    return sortedDistances.get(0).getKey();
  }

  private void populateEdges() {
    for (int i = 0; i < GRID_MAX - GRID_MIN; i++) {
      edges.add(grid[0][i]);
      edges.add(grid[i][0]);
      edges.add(grid[GRID_MAX - GRID_MIN - 1][i]);
      edges.add(grid[i][GRID_MAX - GRID_MIN - 1]);
    }
  }

  private int manhattanDistance(Point a, Point b) {
    return Math.abs(a.x - b.x) + Math.abs(a.y - b.y);
  }

  private int countMax() {
    return pointsGrid.entrySet()
                     .stream()
                     .mapToInt(Map.Entry::getValue)
                     .filter(i -> !edges.contains(i))
                     .map(this::countWithClosest)
                     .max()
                     .getAsInt();
  }

  private int countWithClosest(int id) {
    return (int) distanceGrid.entrySet()
                             .stream()
                             .mapToInt(Map.Entry::getValue)
                             .filter(i -> i == id)
                             .count();
  }

  @Override
  protected String part2() {
    int result = 0;
    for (int x = GRID_MIN; x < GRID_MAX; x++) {
      for (int y = GRID_MIN; y < GRID_MAX; y++) {
        Point p = new Point(x, y);
        int totalDistance = totalDistance(p);
        if (totalDistance < 10000) {
          result++;
        }
      }
    }
    return "" + result;
  }

  private int totalDistance(Point p1) {
    return (int) points.stream()
                       .mapToInt(p2 -> manhattanDistance(p1, p2))
                       .sum();
  }

  private void printGrid() {
    try {
      PrintWriter pw = new PrintWriter("06_grid.txt");
      for (int x = GRID_MIN; x < GRID_MAX; x++) {
        for (int y = GRID_MIN; y < GRID_MAX; y++) {
          int closest = grid[x - GRID_MIN][y - GRID_MIN];
          pw.print(charFor(closest));
        }
        pw.println();
      }
    } catch (Exception e) {}
  }

  private char charFor(int n) {
    if (n == 0) return ' ';
    if (n <= 26) return (char)('a' + n - 1);
    return (char)('A' + n - 27);
  }
}
