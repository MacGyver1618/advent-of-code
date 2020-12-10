import java.util.*;
import java.util.stream.*;

import static java.util.Collections.max;
import static java.util.Collections.min;

public class Advent09 extends Advent {

  List<Long> nums = new ArrayList<>();

  public Advent09() {
    super(9);
  }

  @Override
  protected void parseInput() {
    nums = input.stream()
      .map(Long::valueOf)
      .collect(Collectors.toList());
  }

  @Override
  protected Object part1() {
    return IntStream.range(25, nums.size())
      .filter(this::valid)
      .mapToLong(nums::get)
      .findFirst()
      .getAsLong();
  }

  private boolean valid(int i) {
    var sublist = nums.subList(i-25,i);
    return sublist.stream()
      .flatMap(n -> sublist.stream().map(l -> l.longValue() + n))
      .noneMatch(nums.get(i)::equals);
  }

  @Override
  protected Object part2() {
    var target = (long) part1();
    int s = nums.size();
    for (int l = 2; l < s; l++) {
      for (int i = 0; i < s-l; i++) {
        var sublist = nums.subList(i, i+l);
        if (sublist.stream().mapToLong(Long::longValue).sum() == target) {
          return min(sublist)+max(sublist);
        }
      }
    }
    return null;
  }
}
