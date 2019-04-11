import java.util.*;
import java.util.stream.*;

public class Advent06 extends Advent {

  private Set<List<Integer>> combinations;
  private int[] nums;

  public Advent06() {
    super(6);
  }

  @Override
  protected void parseInput() {
    nums = Arrays.stream(input.get(0).split("\\s+")).mapToInt(Integer::parseInt).toArray();
    combinations = new LinkedHashSet<List<Integer>>();
  }

  @Override
  protected String part1() {
    int steps = 0;
    while (!hasCurrent()) {
      redistribute(findFirstMax());
      steps++;
    }
    return "" + steps;
  }

  private boolean hasCurrent() {
    return !combinations.add(Arrays.stream(nums).boxed().collect(Collectors.toList()));
  }

  private int findFirstMax() {
    int max = -1;
    int index = 0;
    for (int i = 0; i < nums.length; i++) {
      if (nums[i] > max) {
        index = i;
        max = nums[i];
      }
    }
    return index;
  }

  private void redistribute(int from) {
    int left = nums[from];
    nums[from] = 0;
    int i = from;
    while (left > 0) {
      nums[++i % nums.length]++;
      left--;
    }
  }

  @Override
  protected String part2() {
    List<Integer> last = Arrays.stream(nums).boxed().collect(Collectors.toList());
    int i = 0;
    for (List<Integer> list : combinations) {
      if (list.equals(last))
        return "" + (combinations.size() - i);
        i++;
    }
    return "Didn't work";
  }

}
