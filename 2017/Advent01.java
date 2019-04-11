import java.util.*;
import java.util.stream.*;

public class Advent01 extends Advent {

  private int[] nums;

  public Advent01() {
    super(1);
  }

  @Override
  protected void parseInput() {
    nums = input.get(0)
                .chars()
                .map(Character::getNumericValue)
                .toArray();
  }

  @Override
  protected String part1() {
    int current, result = 0, length = nums.length;
    for (int i = 0; i < length; i++) {
      current = nums[i];
      if (nums[(i + 1) % length] == current)
        result += current;
    }
    return result + "";
  }

  @Override
  protected String part2() {
    int current, result = 0, len = nums.length;
    for (int i = 0; i < len; i++) {
      current = nums[i];
      if (current == nums[(i + len/2) % len])
        result += current;
    }
    return result + "";
  }
}
