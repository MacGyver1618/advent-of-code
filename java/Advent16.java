import java.util.*;
import java.util.stream.*;

public class Advent16 extends Advent {

  int offset;
  int[] BASE_PATTERN = new int[] {0,1,0,-1};
  int[][] patterns;
  int[] digits;

  public Advent16() {
    super(16);
  }

  @Override
  protected void parseInput() {
    digits = input.get(0).chars().map(c -> (char) c - '0').toArray();
    offset = Integer.parseInt(Arrays.stream(digits)
      .limit(7)
      .mapToObj(String::valueOf)
      .collect(Collectors.joining()));
  }

  @Override
  protected Object part1() {
    for (int i = 0; i < 100; i++) {
      digits = nextPhase(0);
    }
    return Arrays.stream(digits)
      .limit(8)
      .mapToObj(String::valueOf)
      .collect(Collectors.joining());
  }

  private int[] nextPhase(int start) {
    int[] nextPhase = new int[digits.length];
    for (int i = 0; i < digits.length; i++) {
      int sum = 0;
      for (int n = i; n < digits.length; n += 4*(i+1)) {
        for (int offset = 0; offset < i; offset++) {
          partialSum += digits[n + offset];
        }
        for (int offset = 2*(i+1); offset < i; offset++) {
          partialSum -= digits[n + offset];
        }
      }
      nextPhase[i] = partialSum % 10;
    }
    return nextPhase;
  }

  @Override
  protected Object part2() {
    generateLongerInput();
    for (int i = 0; i < 100; i++) {
      digits = nextPhase(offset);
    }
    return Arrays.stream(digits)
      .skip(offset)
      .limit(8)
      .mapToObj(String::valueOf)
      .collect(Collectors.joining());
  }

  private void generateLongerInput() {
    parseInput();
    int times = 10_000;
    int[] original = Arrays.copyOf(digits, digits.length);
    digits = new int[times*original.length];
    for (int i = 0; i < times*original.length; i++) {
      digits[i] = original[i % original.length];
    }
  }
}
