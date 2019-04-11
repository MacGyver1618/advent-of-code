import java.util.*;
import java.util.stream.*;

public class Advent05 extends Advent {

  private int[] jumps;

  public Advent05() {
    super(5);
  }

  @Override
  protected void parseInput() {
    jumps = input.stream()
                 .mapToInt(Integer::parseInt)
                 .toArray();
  }

  @Override
  protected String part1() {
    int i = 0;
    int current = 0;
    int count = 0;
    while (i < jumps.length) {
      current = jumps[i];
      //sopl("current: ", jumps[i], ", i: ", i);
      jumps[i] = current + 1;
      count++;
      i += current;
      //(new Scanner(System.in)).nextLine();
    }
    return "" + count;
  }

  @Override
  protected String part2() {
    parseInput();
    int i = 0;
    int current = 0;
    int count = 0;
    while (i < jumps.length) {
      current = jumps[i];
      count++;
      jumps[i] = current >= 3 ? current - 1 : current + 1;
      i += current;
    }
    return "" + count;
  }
}
