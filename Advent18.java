import java.util.*;
import java.util.stream.*;

public class Advent18 extends Advent {

  private int SIZE = 50;
  private char[][] grid = new char[SIZE][SIZE];

  public Advent18() {
    super(18);
  }
  @Override
  protected void parseInput() {
    for (int y = 0; y < input.size(); y++) {
      String line = input.get(y);
      for (int x = 0; x < line.length(); x++) {
        grid[x][y] = line.charAt(x);
      }
    }
  }

  @Override
  protected String part1() {
    for (int i = 0; i < 10; i++) {
      grid = nextGen();
    }
    return "" + resourceValue();
  }

  private int resourceValue() {
    return countChars('#')*countChars('|');
  }

  private void printGrid() {
    StringBuilder sb = new StringBuilder();
    for (int y = 0; y < SIZE; y++) {
      for (int x = 0; x < SIZE; x++) {
        sb.append(grid[x][y]);
      }
      sb.append('\n');
    }
    sopl(sb.toString());
  }

  private char[][] nextGen() {
    char[][] nextGen = new char[SIZE][SIZE];
    for (int y = 0; y < SIZE; y++) {
      for (int x = 0; x < SIZE; x++) {
        char c = grid[x][y];
        nextGen[x][y] = nextChar(c,x,y);
      }
    }
    return nextGen;
  }

  private char nextChar(char c, int x, int y) {
    int xStart = x == 0 ? 0 : x-1;
    int xEnd = x == SIZE-1 ? SIZE-1 : x+1;
    int yStart = y == 0 ? 0 : y-1;
    int yEnd = y == SIZE-1 ? SIZE-1 : y+1;
    int trees = 0;
    int lumber = 0;
    int open = 0;
    for (int i = xStart; i <= xEnd; i++) {
      for (int j = yStart; j <= yEnd; j++) {
        if (i == x && j == y) continue;
        switch (grid[i][j]) {
          case '|': trees++;  break;
          case '#': lumber++; break;
          case '.': open++;   break;
        }
      }
    }
    switch (c) {
      case '.': return trees   >= 3 ? '|' : '.';
      case '|': return lumber  >= 3 ? '#' : '|';
      case '#': return lumber  >= 1 && trees >= 1 ? '#' : '.';
    }
    throw new IllegalStateException();
  }

  private int countChars(char c) {
    int result = 0;
    for (int y = 0; y < SIZE; y++) {
      for (int x = 0; x < SIZE; x++) {
        if (grid[x][y] == c) {
          result++;
        }
      }
    }
    return result;
  }

  @Override
  protected String part2() {
    parseInput();
    int rangeStart = 0;
    int rangeSize = 0;
    List<Integer> resourceValues = new ArrayList<>(1_000_000);
    List<Object> grids = new ArrayList<>(1_000_000);
    main:
    for (int i = 0; i < 1_000_000_000; i++) {
      grid = nextGen();
      for (int j = i-1; j >= 0; j--) {
        char[][] aGrid = (char[][]) grids.get(j);
        if (Arrays.deepEquals(grid, aGrid)) {
          rangeStart = j;
          rangeSize = i-j;
          break main;
        }
      }
      resourceValues.add(resourceValue());
      grids.add(grid);
    }
    return "" + resourceValues.get(((1_000_000_000 - rangeStart) % rangeSize) + rangeStart - 1);
  }
}
