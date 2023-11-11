import java.util.*;
import java.util.stream.*;

import static java.util.stream.Collectors.toList;

public class Advent05 extends Advent {

  List<Long> nums;

  public Advent05() {
    super(5);
  }

  @Override
  protected void parseInput() {
    nums = input.stream()
      .mapToLong(this::toSeatNumber)
      .sorted()
      .boxed()
      .collect(toList());
  }

  private long toSeatNumber(String s) {
    return Integer.parseInt(s.replace('F', '0')
      .replace('B','1')
      .replace('L','0')
      .replace('R', '1'),2);
  }

  @Override
  protected Object part1() {
    return nums.get(nums.size()-1);
  }

  @Override
  protected Object part2() {
    var allSeats = LongStream.rangeClosed(nums.get(0), nums.get(nums.size()-1)).boxed().collect(toList());
    allSeats.removeAll(nums);
    return allSeats.get(0);
  }
}
