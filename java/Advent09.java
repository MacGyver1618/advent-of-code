import java.util.*;
import java.util.stream.*;

public class Advent09 extends Advent {

  long[] nums;

  public Advent09() {
    super(9);
  }

  @Override
  protected void parseInput() {
    nums = Arrays.stream(input.get(0).split(","))
      .mapToLong(Long::valueOf)
      .toArray();
  }

  @Override
  protected Object part1() {
    IntCodeMachine machine = new IntCodeMachine(nums);
    machine.input(1L);
    while (!machine.finished) {
      machine.run();
    }
    return machine.output();
  }

  @Override
  protected Object part2() {
    IntCodeMachine machine = new IntCodeMachine(nums);
    machine.input(2L);
    while (!machine.finished) {
      machine.run();
    }
    return machine.output();
  }
}
