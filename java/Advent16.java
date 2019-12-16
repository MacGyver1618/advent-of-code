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
      sopl(Arrays.stream(digits).mapToObj(String::valueOf).collect(Collectors.joining()));
      pause();
    }
    return Arrays.stream(digits)
      .limit(8)
      .mapToObj(String::valueOf)
      .collect(Collectors.joining());
  }

  private int[] nextPhase(int start) {
    int[] nextPhase = new int[digits.length];
    for (int position = start; position < digits.length; position++) {
      if (position % 10_000 == 0) sop(".");
      int current = 0;
      for (int component = start; component < digits.length; component++) {
        int multiplier = BASE_PATTERN[((component+1)/(position+1))%4];
        current += digits[component]*multiplier;
      }
      nextPhase[position] = Math.abs(current % 10);
    }
    sopl();
    return nextPhase;
  }

  @Override
  protected Object part2() {
    parseInput();
    generateLongerInput();
    sopl(offset, "/", digits.length);
    for (int i = 0; i < 100; i++) {
      sopl(i);
      digits = nextPhase(offset);
    }
    return Arrays.stream(digits)
      .skip(offset)
      .limit(8)
      .mapToObj(String::valueOf)
      .collect(Collectors.joining());
  }

  private void generateLongerInput() {
    int times = 10_000;
    int[] original = Arrays.copyOf(digits, digits.length);
    digits = new int[times*original.length];
    for (int i = 0; i < times*original.length; i++) {
      digits[i] = original[i % original.length];
    }
  }
}
