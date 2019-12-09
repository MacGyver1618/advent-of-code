import java.util.*;
import java.util.stream.*;

public class Advent07 extends Advent {

  long[] nums;

  public Advent07() {
    super(7);
  }

  @Override
  protected void parseInput() {
    nums = Arrays.stream(input.get(0).split(","))
      .mapToLong(Long::valueOf)
      .toArray();
  }

  @Override
  protected Object part1() {
    return findMax(0, 1, 2, 3, 4);
  }

  private long findMax(int... phaseSeed) {
    long maxOutput = 0;
    for (int[] phases : generatePhases(phaseSeed)) {
      long output = findOutput(phases);
      if (output > maxOutput) {
        maxOutput = output;
      }
    }
    return maxOutput;
  }

  private List<int[]> generatePhases(int[] source) {
    List<int[]> result = new ArrayList<>();
    permute(source.length, source, result);
    return result;
  }

  private void permute(int k, int[] a, List<int[]> out) {
    if (k == 1) {
      out.add(Arrays.copyOf(a, a.length));
    } else {
      permute(k - 1, a, out);
      for (int i = 0; i < k - 1; i++) {
        if (k % 2 == 0) {
          swap(a, i, k - 1);
        } else {
          swap(a, 0, k - 1);
        }
        permute(k - 1, a, out);
      }
    }
  }

  private void swap(int[] input, int a, int b) {
      int tmp = input[a];
      input[a] = input[b];
      input[b] = tmp;
  }

  private long findOutput(int[] phases) {
    IntCodeMachine[] machines = initMachines(phases);
    int machinePointer = 0;
    long signal = 0;
    while (!finished(machines)) {
      IntCodeMachine machine = machines[machinePointer];
      machine.input(signal);
      machine.run();
      signal = machine.output();
      machinePointer = (machinePointer + 1) % 5;
    }
    return signal;
  }

  private IntCodeMachine[] initMachines(int[] phases) {
    parseInput();
    IntCodeMachine[] machines = new IntCodeMachine[phases.length];
    for (int i = 0; i < phases.length; i++) {
      machines[i] = new IntCodeMachine(nums);
      machines[i].input(phases[i]);
    }
    return machines;
  }

  private boolean finished(IntCodeMachine[] machines) {
    for (IntCodeMachine machine : machines) {
      if (!machine.finished) {
        return false;
      }
    }
    return true;
  }

  @Override
  protected Object part2() {
    return findMax(5, 6, 7, 8, 9);
  }
}
