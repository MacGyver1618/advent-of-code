import java.io.*;
import java.util.*;
import java.util.regex.*;
import java.util.stream.*;

public class Advent11 extends Advent {

  private static final int GRID_SERIAL_NUMBER = 2187;
  private int[][] grid = new int[300][300];

  public Advent11() {
    super(11);
  }

  @Override
  protected void readInput() {

  }

  @Override
  protected void parseInput() {
    for (int x = 0; x < 300; x++) {
      for (int y = 0; y < 300; y++) {
        grid[x][y] = powerLevel(x+1, y+1);
      }
    }
  }

  private int powerLevel(int x, int y) {
    int rackId = x + 10;
    int powerLevel = rackId*y;
    powerLevel += GRID_SERIAL_NUMBER;
    powerLevel *= rackId;
    powerLevel = (powerLevel / 100) % 10;
    powerLevel -= 5;
    return powerLevel;
  }

  @Override
  protected String part1() {
    int maxPower = Integer.MIN_VALUE;
    int maxX = 0, maxY = 0;
    for (int x = 1; x <= 300-2; x++) {
      for (int y = 1; y <= 300-2; y++) {
        int power = totalPower(x, y, 3);
        if (power > maxPower) {
          maxPower = power;
          maxX = x;
          maxY = y;
        }
      }
    }
    return maxX + "," + maxY;
  }

  @Override
  protected String part2() {
    int maxPower = Integer.MIN_VALUE;
    int maxX = 0, maxY = 0, maxSize = 0;
    for (int x = 1; x <= 300; x++) {
      for (int y = 1; y <= 300; y++) {
        for (int size = 1; size <= 300 - Math.max(x,y) + 1; size++) {
          int power = totalPower(x, y, size);
          if (power > maxPower) {
            maxPower = power;
            maxX = x;
            maxY = y;
            maxSize = size;
          }
        }
      }
    }
    return maxX + "," + maxY + "," + maxSize;
  }

  private int totalPower(int x, int y, int size) {
    int result = 0;
    for (int i = x; i < x + size; i++) {
      for (int j = y; j < y + size; j++) {
        result += grid[i-1][j-1];
      }
    }
    return result;
  }
}
