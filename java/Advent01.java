import java.util.*;
import java.util.stream.*;

import static java.util.stream.Collectors.toList;

public class Advent01 extends Advent {

  public Advent01() {
    super(1);
  }

  List<Integer> nums;

  @Override
  protected void parseInput() {
    nums = input.stream()
      .map(Integer::valueOf)
      .collect(toList());
  }

  @Override
  protected Object part1() {
    for (int i : nums) {
      for (int j : nums) {
        if (i + j == 2020) {
          if (i == j) {
            continue;
          }
          return i * j;
        }
      }
    }
    return null;
  }

  @Override
  protected Object part2() {
    for (int i : nums) {
      for (int j : nums) {
        for (int k : nums) {
          if (i + j + k == 2020) {
            if (i == j || i == k || j == k) {
              continue;
            }
            return i * j * k;
          }
        }
      }
    }
    return null;
  }
}
