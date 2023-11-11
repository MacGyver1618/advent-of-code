import java.util.*;
import java.util.stream.*;

import static java.util.Collections.max;
import static java.util.stream.Collectors.toSet;

public class Advent10 extends Advent {

  List<Integer> nums;

  public Advent10() {
    super(10);
  }

  @Override
  protected void parseInput() {
    nums = input.stream().mapToInt(Integer::valueOf).sorted().boxed().collect(Collectors.toList());
    nums.addAll(List.of(0, max(nums)+3));
  }

  @Override
  protected Object part1() {
    int prev = 0;
    int diff = 0;
    int ones = 0;
    int threes = 0;
    for (int i : nums) {
      diff = i - prev;
      if (diff == 3) threes++;
      if (diff == 1) ones++;
      prev = i;
    }
    return ones*++threes;
  }

  @Override
  protected Object part2() {
    var paths = new TreeMap<Integer,Long>();
    paths.put(154,1L);
    nums.stream().sorted(Comparator.comparing(Integer::intValue).reversed()).forEach(n -> {
      var sources = nums.stream().filter(t -> n - t > 0 && n - t <= 3).collect(toSet());
      for (var source : sources) {
        paths.put(source, paths.getOrDefault(source, 0L) + paths.get(n));
      }
    });
    return paths.get(0);
  }
}
