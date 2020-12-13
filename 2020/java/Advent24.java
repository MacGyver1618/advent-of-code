import java.util.*;
import java.util.stream.*;

public class Advent24 extends Advent {

  boolean visual = true;
  int frameInterval = 50;
  //char[][] grid;
  Map<Point, Character> grid;
  Map<Point3, Character> grid3d;
  //Set<char[][]> history;
  Set<Map<Point, Character>> history;

  public Advent24() {
    super(24);
  }

  @Override
  protected void parseInput() {
    //grid = new char[input.get(0).length()][input.size()];
    grid = new TreeMap<>();
    grid3d = new TreeMap<>();
    for (int y = 0; y < input.size(); y++) {
      String line = input.get(y);
      for (int x = 0; x < line.length(); x++) {
        grid.put(new Point(x,y), line.charAt(x));
        grid3d.put(new Point3(x,y,0), line.charAt(x));
        //grid[x][y] = line.charAt(x);
      }
    }
    history = new HashSet<>();
    history.add(grid);
  }

  @Override
  protected Object part1() {
    while (true) {
      grid = nextGeneration();
      if (!history.add(grid)) {
        return bioDiversity();
      }
    }
  }

  //char[][] nextGeneration() {
  Map<Point, Character> nextGeneration() {
    //char[][] nextGen = Arrays.copyOf(grid, grid.length);
    Map<Point, Character> nextGen = new TreeMap<>();
    for (int y = 0; y < 5; y++) {
      for (int x = 0; x < 5; x++) {
        Point p = new Point(x,y);
        int liveNeighbors = liveNeighbors(x,y);
        if (grid.get(p) == '#') {
          nextGen.put(p, liveNeighbors == 1 ? '#' : '.');
        } else {
          nextGen.put(p, liveNeighbors == 1 || liveNeighbors == 2 ? '#' : '.');
        }
        /*
        if (grid[x][y] == '#') {
          nextGen[x][y] = liveNeighbors == 1 ? '#' : '.';
        } else {
          nextGen[x][y] = liveNeighbors == 1 || liveNeighbors == 2 ? '#' : '.';
        }
        */
      }
    }
    return nextGen;
  }

  int liveNeighbors(int x, int y) {
    int sum = 0;
    if (x != 0) sum += grid.get(new Point(x-1,y)) == '#' ? 1 : 0;
    if (x != 4) sum += grid.get(new Point(x+1,y)) == '#' ? 1 : 0;
    if (y != 0) sum += grid.get(new Point(x,y-1)) == '#' ? 1 : 0;
    if (y != 4) sum += grid.get(new Point(x,y+1)) == '#' ? 1 : 0;
    return sum;
  }

  long bioDiversity() {
    long sum = 0;
    int current = 1;
    for (int y = 0; y < 5; y++) {
      for (int x = 0; x < 5; x++) {
        //if (grid[x][y] == '#') {
        if (grid.get(new Point(x,y)) == '#') {
          sum += current;
        }
        current *= 2;
      }
    }
    return sum;
  }

  private void printGrid() {
    for (int y = 0; y <= 4; y++) {
      for (int x = 0; x <= 4; x++) {
        //sop(grid[x][y]);
        sop(grid.get(new Point(x,y)));
      }
      sopl();
    }
  }

  private void printGrid3D() {
    for (int z = -5; z <= 5; z++) {
      for (int y = 0; y <= 4; y++) {
        for (int x = 0; x <= 4; x++) {
          sop(grid3d.getOrDefault(new Point3(x,y,z), '?'));
        }
        sopl();
      }
      sopl();
    }
  }

  @Override
  protected Object part2() {
    for (int i = 0; i < 200; i++) {
      grid3d = nextGeneration3D();
      if (visual) {
        sopl("After ", i+1, " minutes");
        printGrid3D();
        sopl();
        pause();
      }
    }
    return grid3d.values().stream()
      .filter(c -> c == '#')
      .count();
  }


  Map<Point3, Character> nextGeneration3D() {
    Map<Point3, Character> nextGen = new TreeMap<>();
    int zmin = zmin();
    int zmax = zmax();
    for (int z = zmin; z <= zmax; z++) {
      for (int y = 0; y < 5; y++) {
        for (int x = 0; x < 5; x++) {
          Point3 p = new Point3(x,y,z);
          if (x == 2 && y == 2) continue;
          int liveNeighbors = liveNeighbors3D(p);
          char c;
          if (grid3d.getOrDefault(p, '.') == '#') {
            c = liveNeighbors == 1 ? '#' : '.';
          } else {
            c = liveNeighbors == 1 || liveNeighbors == 2 ? '#' : '.';
          }
          nextGen.put(p, c);
        }
      }
    }
    return nextGen;
  }

  int zmin() {
    return grid3d.keySet().stream()
      .mapToInt(k -> k.z)
      .min()
      .orElseThrow(IllegalStateException::new) - 1;
  }

  int zmax() {
    return grid3d.keySet().stream()
      .mapToInt(k -> k.z)
      .max()
      .orElseThrow(IllegalStateException::new) + 1;
  }

  int liveNeighbors3D(Point3 p) {
    int sum = 0;
    sum += upperNeighbors(p);
    sum += lowerNeighbors(p);
    sum += leftNeighbors(p);
    sum += rightNeighbors(p);
    return sum;
  }

  int upperNeighbors(Point3 p) {
    int sum = 0;
    if (p.y == 0) {
      sum += grid3d.getOrDefault(new Point3(2,1,p.z-1), '.') == '#' ? 1 : 0;
    } else if (p.x == 2 && p.y == 3) {
      for (int i = 0; i <= 4; i++) {
        sum += grid3d.getOrDefault(new Point3(i,4,p.z+1), '.') == '#' ? 1 : 0;
      }
    } else {
      sum += grid3d.getOrDefault(new Point3(p.x,p.y-1,p.z), '.') == '#' ? 1 : 0;
    }
    return sum;
  }

  int lowerNeighbors(Point3 p) {
    int sum = 0;
    if (p.y == 4) {
      sum += grid3d.getOrDefault(new Point3(2,3,p.z-1), '.') == '#' ? 1 : 0;
    } else if (p.x == 2 && p.y == 1) {
      for (int i = 0; i <= 4; i++) {
        sum += grid3d.getOrDefault(new Point3(i,0,p.z+1), '.') == '#' ? 1 : 0;
      }
    } else {
      sum += grid3d.getOrDefault(new Point3(p.x,p.y+1,p.z), '.') == '#' ? 1 : 0;
    }
    return sum;
  }

  int leftNeighbors(Point3 p) {
    int sum = 0;
    if (p.x == 0) {
      sum += grid3d.getOrDefault(new Point3(1,2,p.z-1), '.') == '#' ? 1 : 0;
    } else if (p.x == 3 && p.y == 2) {
      for (int i = 0; i <= 4; i++) {
        sum += grid3d.getOrDefault(new Point3(4,i,p.z+1), '.') == '#' ? 1 : 0;
      }
    } else {
      sum += grid3d.getOrDefault(new Point3(p.x-1,p.y,p.z), '.') == '#' ? 1 : 0;
    }
    return sum;
  }

  int rightNeighbors(Point3 p) {
    int sum = 0;
    if (p.x == 4) {
      sum += grid3d.getOrDefault(new Point3(3,2,p.z-1), '.') == '#' ? 1 : 0;
    } else if (p.x == 1 && p.y == 2) {
      for (int i = 0; i <= 4; i++) {
        sum += grid3d.getOrDefault(new Point3(0,i,p.z+1), '.') == '#' ? 1 : 0;
      }
    } else {
      sum += grid3d.getOrDefault(new Point3(p.x+1,p.y,p.z), '.') == '#' ? 1 : 0;
    }
    return sum;
  }
}
