import java.util.*;
import java.util.stream.*;

public class Advent05 extends Advent {

  int pc = 0;
  int[] nums;
  int[] ops = new int[0];
  int[] modes = new int[0];
  boolean debug = false;
  boolean interactive = false;

  Queue<Integer> programInputs;
  List<Integer> programOutputs;

  public Advent05() {
    super(5);
  }

  @Override
  protected void parseInput() {
    nums = Arrays.stream(input.get(0).split(","))
      .mapToInt(Integer::valueOf)
      .toArray();
    pc = 0;
    programInputs = new ArrayDeque<>();
    programOutputs = new ArrayList<>();
  }

  @Override
  protected Object part1() {
    programInputs.add(1);
    runProgram();
    return programOutputs.get(programOutputs.size() - 1);
  }

  @Override
  protected Object part2() {
    parseInput();
    programInputs.add(5);
    runProgram();
    return programOutputs.get(programOutputs.size() - 1);
  }


  private int runProgram(int a, int b) {
    parseInput();
    nums[1] = a;
    nums[2] = b;
    runProgram();
    return nums[0];
  }

  private void runProgram() {
    while (true) {
      switch (nums[pc] % 100) {
        case 1: add(); break;
        case 2: mult(); break;
        case 3: input(); break;
        case 4: output(); break;
        case 5: jt(); break;
        case 6: jf(); break;
        case 7: lt(); break;
        case 8: eq(); break;
        case 99: return;
      }
    }
  }

  private void add() {
    readArgs(3);
    debugInstruction("add", 3);
    nums[ops[2]] = get(0) + get(1);
  }

  private void mult() {
    readArgs(3);
    debugInstruction("mult", 3);
    nums[ops[2]] = get(0) * get(1);
  }

  private void input() {
    readArgs(1);
    debugInstruction("input", 1);
    if (interactive) {
      sop("Input: ");
      nums[ops[0]] = readInt();
    } else {
      nums[ops[0]] = programInputs.poll();
    }
  }

  private void output() {
    readArgs(1);
    debugInstruction("output", 1);
    if (interactive) {
      sopl(get(0));
    } else {
      programOutputs.add(get(0));
    }
  }

  private void jt() {
    readArgs(2);
    debugInstruction("jt", 2);
    if (get(0) != 0)
      pc = get(1);
  }

  private void jf() {
    readArgs(2);
    debugInstruction("jf", 2);
    if (get(0) == 0)
      pc = get(1);
  }

  private void lt() {
    readArgs(3);
    debugInstruction("lt", 3);
    nums[ops[2]] = (get(0) < get(1)) ? 1 : 0;
  }

  private void eq() {
    readArgs(3);
    debugInstruction("eq", 3);
    nums[ops[2]] = (get(0) == get(1)) ? 1 : 0;
  }

  private int mode(int pos) {
    int div = 100*(int) Math.pow(10, pos);
    return ((int) nums[pc] / div) % 10;
  }

  private void readArgs(int count) {
    ops = new int[count];
    modes = new int[count];
    for (int i = 0; i < count; i++) {
      ops[i] = nums[pc + i + 1];
      modes[i] = mode(i);
    }
    pc += count + 1;
  }

  private int get(int pos) {
    return modes[pos] == 1 ? ops[pos] : nums[ops[pos]];
  }

  private void debug() {
    if (debug) {
      readArgs(3);
      pc -= 4;
      sopl("pc: ", pc);
      sopl("instruction: ", nums[pc]);
      sopl("ops: ", Arrays.toString(ops));
      sopl("modes: ", Arrays.toString(modes));
      pause();
    }
  }

  private void debugInstruction(String name, int numOps) {
    if (debug) {
      String out = "[DEBUG] " + name;
      for (int i = 0; i < numOps; i++) {
        out += " " + get(i);
      }
      sopl(out);
    }
  }
}
