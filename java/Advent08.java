import java.util.*;
import java.util.stream.*;

public class Advent08 extends Advent {

  int WIDTH = 25;
  int HEIGHT = 6;
  int LAYERS;
  int[][][] pixels;

  public Advent08() {
    super(8);
  }

  @Override
  protected void parseInput() {
    String in = input.get(0);
    LAYERS = in.length() / (WIDTH * HEIGHT);
    pixels = new int[WIDTH][HEIGHT][LAYERS];
    for (int z = 0; z < LAYERS; z++) {
      for (int y = 0; y < HEIGHT; y++) {
        for (int x = 0; x < WIDTH; x++) {
          int pos = z*HEIGHT*WIDTH + y*WIDTH + x;
          pixels[x][y][z] = Integer.parseInt(in.substring(pos, pos+1));
        }
      }
    }
  }

  @Override
  protected Object part1() {
    int fewestZeroes = Integer.MAX_VALUE;
    int fewestZeroesAt = -1;
    for (int z = 0; z < LAYERS; z++) {
      int zeroCount = countZeroesAt(z);
      if (zeroCount < fewestZeroes) {
        fewestZeroes = zeroCount;
        fewestZeroesAt = z;
      }
    }
    return countOnesAt(fewestZeroesAt)*countTwosAt(fewestZeroesAt);
  }

  private int countZeroesAt(int layer) {
    return countDigits(layer, 0);
  }

  private int countOnesAt(int layer) {
    return countDigits(layer, 1);
  }

  private int countTwosAt(int layer) {
    return countDigits(layer, 2);
  }

  private int countDigits(int layer, int digit) {
    int count = 0;
    for (int y = 0; y < HEIGHT; y++) {
      for (int x = 0; x < WIDTH; x++) {
        if (pixels[x][y][layer] == digit) {
          count++;
        }
      }
    }
    return count;
  }

  @Override
  protected Object part2() {
    for (int y = 0; y < HEIGHT; y++) {
      for (int x = 0; x < WIDTH; x++) {
        sop(pixelAt(x,y), ' ');
      }
      sopl();
    }
    return "See above";
  }

  private char pixelAt(int x, int y) {
    for (int z = 0; z < LAYERS; z++) {
      int pixel = pixels[x][y][z];
      if (pixel != 2) {
        return pixel == 0 ? ' ' : '*';
      }
    }
    throw new IllegalStateException();
  }
}
