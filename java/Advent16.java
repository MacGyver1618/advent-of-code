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
    int l = digits.length;
    int[] nextPhase = new int[l];
    for (int i = 0; i < l; i++) {
      int sum = 0;
      int k = i + 1;
      int substep = 2*k;
      int groupstep = 4*k;
      for (int n = i; n < l; n += groupstep) {
        for (int offset = 0; offset < k && n + offset < l; offset++) {
          int index = n + offset;
          sum += digits[index];
          if (index + substep < l)
            sum -= digits[index + substep];
        }
      }
      if (sum < 0) sum *= -1;
      nextPhase[i] = sum % 10;
    }
    return nextPhase;
  }

  @Override
  protected Object part2() {
    generateLongerInput();
    for (int i = 0; i < 100; i++) {
      int[] nextPhase = new int[digits.length];
      int partialSum = 0;
      for (int k = digits.length - 1; k >= offset; k--) {
        partialSum += digits[k];
        nextPhase[k] = partialSum % 10;
      }
      digits = nextPhase;
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
