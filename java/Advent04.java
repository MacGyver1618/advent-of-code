import java.util.*;
import java.util.stream.*;

public class Advent04 extends Advent {

  int min = 387638;
  int max = 919123;

  public Advent04() {
    super(4);
  }

  @Override
  protected void readInput() {}

  @Override
  protected void parseInput() {}

  @Override
  protected Object part1() {
    return IntStream.rangeClosed(min, max)
      .filter(this::isMonotonic)
      .filter(this::hasDouble)
      .count();
  }

  private boolean isMonotonic(int n) {
      int cur;
      int prev = n % 10;
      n /= 10;
      for (; n > 0; n /= 10, prev = cur) {
        if (prev < (cur = n % 10)) {
          return false;
        }
      }
      return true;
  }

  private boolean hasDouble(int n) {
    int cur;
    int prev = n % 10;
    n /= 10;
    for (; n > 0; n /= 10, prev = cur) {
      if (prev == (cur = n % 10)) {
        return true;
      }
    }
    return false;
  }

  @Override
  protected Object part2() {
    return IntStream.rangeClosed(min, max)
      .filter(this::isMonotonic)
      .filter(this::hasDouble)
      .filter(i -> rle(i).contains("2"))
      .count();
  }

  private String rle(int n) {
    String rle = "";
    int adjacent = 1;
    int cur;
    int prev = n % 10;
    n /= 10;
    for (; n > 0; prev = cur, n /= 10) {
      if (prev == (cur = n % 10)) {
        adjacent++;
      } else {
        rle += adjacent;
        adjacent = 1;
      }
    }
    return rle + adjacent;
  }
}
