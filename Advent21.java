import java.util.*;
import java.util.stream.*;

public class Advent21 extends Advent {

  long d = 0;
  long f = 0;

  public Advent21() {
    super(21);
  }

  @Override
  protected void readInput() {}

  @Override
  protected void parseInput() {}

  @Override
  protected String part1() {
    loop();
    return "" + f;
  }

  private void loop() {
    /*
    Again, this day required reverse engineering the assembly code.
    This is the inner loop that stores into register F the value to
    be compared against register A. F is initialized to zero, so the
    values of F generated are the same for all values of A. Thus,
    we only need to generate one set of possible outputs and check whether
    the outputs loop.

    If any initial value of register A is in the set of possible
    outputs of F, the loop will terminate. Thus we only need to check
    whether a given value of A is in the list of outputs, and the number
    of computations required to arrive at said value of A is equal to its
    position in the sequence of values of F.
    */
    d = f | 65536;
    f = 7586220;
    while (true) {
      f += d & 255;
      f &= 16777215;
      f *= 65899;
      f &= 16777215;
      if (d < 256) {
        return;
      }
      d /= 256;
    }
  }

  @Override
  protected String part2() {
    List<Long> values = new ArrayList<>(1_000_000);
    values.add(f);
    while (true) {
      loop();
      if (values.contains(f)) {
        break;
      }
      values.add(f);
    }
    return "" + values.get(values.size() - 1);
  }
}
