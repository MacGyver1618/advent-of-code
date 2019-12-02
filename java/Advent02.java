import java.util.*;
import java.util.stream.*;

public class Advent02 extends Advent {

  int pc = 0;
  int[] nums;

  public Advent02() {
    super(2);
  }

  @Override
  protected void parseInput() {
    nums = Arrays.stream(input.get(0).split(","))
      .mapToInt(Integer::valueOf)
      .toArray();
    pc = 0;
  }

  @Override
  protected Object part1() {
    return runProgram(12, 2);
  }

  @Override
  protected Object part2() {
    for (int noun = 0; noun < 100; noun++) {
      for (int verb = 0; verb < 100; verb++) {
        if (runProgram(noun, verb) == 19690720) {
          return 100*noun + verb;
        }
      }
    }
    return null;
  }

  private int runProgram(int a, int b) {
    parseInput();
    nums[1] = a;
    nums[2] = b;
    runProgram();
    return nums[0];
  }

  private void runProgram() {
    int op1, op2, target;
    while (true) {
      switch (nums[pc]) {
        case 1:
          op1 = nums[nums[pc + 1]];
          op2 = nums[nums[pc + 2]];
          target = nums[pc + 3];
          nums[target] = op1 + op2;
          break;
        case 2:
          op1 = nums[nums[pc + 1]];
          op2 = nums[nums[pc + 2]];
          target = nums[pc + 3];
          nums[target] = op1 * op2;
          break;
        case 99:
          return;
      }
      pc += 4;
    }
  }
}
