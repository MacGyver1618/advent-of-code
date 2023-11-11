import java.util.*;

public class Advent11 extends Advent {

  char[][] grid;
  char[][] current;

  int yMin, xMin, yMax, xMax;

  public Advent11() {
    super(11);
  }

  @Override
  protected void parseInput() {
    grid = readCharGrid();

    yMin = 0;
    xMin = 0;
    xMax = grid.length-1;
    yMax = grid[0].length-1;
  }

  @Override
  protected Object part1() {
    char[][] next;
    current = grid;
    while (true) {
      next = evolve();
      if (Arrays.deepEquals(current, next)) {
        return countSeats(next);
      }
      current = next;
    }
  }

  private char[][] evolve() {
    char[][] result = new char[xMax+1][yMax+1];
    for (var p : pointsIn(current)) {
      char seat = current[p.x][p.y];
      int neighbors = neighbors(p.x, p.y);
      if (seat == 'L' && neighbors == 0) {
        result[p.x][p.y] = '#';
      } else if (seat == '#' && neighbors >= 4) {
        result[p.x][p.y] = 'L';
      } else {
        result[p.x][p.y] = seat;
      }
    }
    return result;
  }

  private int neighbors(int x, int y) {
    int result = 0;
    for (int i = x-1; i <= x+1; i++) {
      inner:
      for (int j = y-1; j <=y+1; j++) {
        if (i < xMin || i > xMax || j < yMin || j > yMax || (x == i && y == j)) continue inner;
        if (current[i][j] == '#') result++;
      }
    }
    return result;
  }

  private int countSeats(char[][] grid) {
    return (int) pointsIn(grid).stream()
      .filter(p -> grid[p.x][p.y] == '#')
      .count();
  }

  @Override
  protected Object part2() {
    char[][] next;
    current = grid;
    int count = 0;
    while(true) {
      next = evolve2();
      count++;
      if (Arrays.deepEquals(current, next)) {
        sopl(count);
        return countSeats(next);
      }
      current = next;
    }
  }

  private char[][] evolve2() {
    char[][] result = new char[xMax+1][yMax+1];
    for (int y = 0; y <= yMax; y++) {
      for (int x = 0; x <= xMax; x++) {
        char seat = current[x][y];
        int visibles = visibles(x, y);
        if (seat == 'L' && visibles == 0) {
          result[x][y] = '#';
        } else if (seat == '#' && visibles >= 5) {
          result[x][y] = 'L';
        } else {
          result[x][y] = seat;
        }
      }
    }
    return result;
  }

  private int visibles(int x, int y) {
    var origin = new Point(x,y);
    var directions = List.of(
      new Point(-1,-1),
      new Point(-1, 0),
      new Point(-1, 1),
      new Point( 0,-1),
      new Point( 0, 1),
      new Point( 1,-1),
      new Point( 1, 0),
      new Point( 1, 1));
    int count = 0;
    for (var direction : directions) {
      if (canSee(origin, direction)) count++;
    }
    return count;
  }

  private boolean canSee(Point origin, Point direction) {
    var point = origin.add(direction);
    while (point.x >= xMin && point.x <= xMax && point.y >= yMin && point.y <= yMax) {
      char seat = current[point.x][point.y];
      if (seat == '#') return true;
      if (seat == 'L') return false;
      point = point.add(direction);
    }
    return false;
  }
}
