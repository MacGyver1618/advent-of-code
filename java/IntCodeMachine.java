import java.util.*;
import java.util.concurrent.*;

public class IntCodeMachine {

  int pc = 0;
  long[] memory;
  long[] ops = new long[0];
  int[] modes = new int[0];
  long rb = 0;

  boolean debug = false;
  boolean debugRaw = false;
  boolean interactive = false;
  boolean step = false;

  boolean halted = false;
  boolean finished = false;

  Queue<Long> programInputs = new LinkedBlockingQueue<>();
  List<Long> programOutputs = new ArrayList<>();

  public IntCodeMachine(long[] memory) {
    this.memory = Arrays.copyOf(memory, 1_000_000);
    this.pc = 0;
  }

  public void run() {
    halted = false;
    while (!halted && !finished) {
      switch ((int)(memory[pc] % 100)) {
        case 1: add(); break;
        case 2: mult(); break;
        case 3: in(); break;
        case 4: out(); break;
        case 5: jt(); break;
        case 6: jf(); break;
        case 7: lt(); break;
        case 8: eq(); break;
        case 9: rb(); break;
        case 99: finish();
      }
      if (step) pause();
    }
  }

  public void input(long val) {
    programInputs.add(val);
  }

  public long output() {
    return programOutputs.get(programOutputs.size() - 1);
  }

  private void add() {
    debugRaw(3);
    readModes(3);
    long op1 = read(modes[0], readNext());
    long op2 = read(modes[1], readNext());
    long target = readNext();
    //debugInstruction("add", 3);
    write(modes[2], target, op1 + op2);
    pc++;
  }

  private void mult() {
    debugRaw(3);
    readModes(3);
    long op1 = read(modes[0], readNext());
    long op2 = read(modes[1], readNext());
    long target = readNext();
    //debugInstruction("mult", 3);
    write(modes[2], target, op1 * op2);
    pc++;
  }

  private void in() {
    if (programInputs.isEmpty()) {
      halted = true;
      return;
    }
    debugRaw(1);
    readArgs(1);
    debugInstruction("input", 1);
    if (interactive) {
      print("Input: ");
      write(0, readInt());
    } else {
      write(0, programInputs.poll());
    }
  }

  private void out() {
    debugRaw(1);
    readArgs(1);
    debugInstruction("output", 1);
    if (interactive) {
      print(get(0));
    } else {
      programOutputs.add(get(0));
    }
  }

  private void jt() {
    debugRaw(2);
    readArgs(2);
    debugInstruction("jt", 2);
    if (get(0) != 0)
      pc = (int) get(1);
  }

  private void jf() {
    debugRaw(2);
    readArgs(2);
    debugInstruction("jf", 2);
    if (get(0) == 0)
      pc = (int) get(1);
  }

  private void lt() {
    debugRaw(3);
    readArgs(3);
    debugInstruction("lt", 3);
    write(2, (get(0) < get(1)) ? 1 : 0);
  }

  private void eq() {
    debugRaw(3);
    readArgs(3);
    debugInstruction("eq", 3);
    write(2, (get(0) == get(1)) ? 1 : 0);
  }

  private void rb() {
    debugRaw(1);
    readArgs(1);
    debugInstruction("rb", 1);
    rb += get(0);
  }

  private void finish() {
    finished = true;
  }

  private int mode(int pos) {
    int div = 100*(int) Math.pow(10, pos);
    return ((int) memory[pc] / div) % 10;
  }

  private void readArgs(int count) {
    ops = new long[count];
    modes = new int[count];
    for (int i = 0; i < count; i++) {
      ops[i] = memory[pc + i + 1];
      modes[i] = mode(i);
    }
    pc += count + 1;
  }

  private long get(int pos) {
    switch ((int)modes[pos]) {
      case 0: return memory[(int)ops[pos]];
      case 1: return ops[pos];
      case 2: return memory[(int)(ops[pos] + rb)];
      default: throw new UnsupportedOperationException();
    }
  }

  private long readNext() {
    return memory[++pc];
  }

  private void readModes(int count) {
    modes = new int[count];
    for (int i = 0; i < count; i++) {
      modes[i] = mode(i);
    }
  }

  private long read(int mode, long raw) {
    switch (mode) {
      case 0: return memory[(int)raw];
      case 1: return raw;
      case 2: return memory[(int)(raw + rb)];
      default: throw new UnsupportedOperationException("Unknown read mode " + mode);
    }
  }

  private void write(int mode, long addr, long value) {
    if (mode == 2) {
      addr += rb;
    }
    memory[(int)addr] = value;
  }

  private void write(int pos, long value) {
    long targetAddress = 0;
    switch((int)modes[pos]) {
      case 0: targetAddress = ops[pos]; break;
      case 2: targetAddress = ops[pos] + rb; break;
      default: throw new UnsupportedOperationException("can't write in absolute mode");
    }
    memory[(int)targetAddress] = value;
  }

  private void debugRaw(int count) {
    if (debugRaw) {
      readArgs(count);
      pc -= count + 1;
      print("[DEBUG] pc: ", pc);
      print("[DEBUG] rb: ", rb);
      print("[DEBUG] instruction: ", memory[pc]);
      print("[DEBUG] ops: ", Arrays.toString(ops));
      print("[DEBUG] modes: ", Arrays.toString(modes));
    }
  }

  private void debugInstruction(String name, int numOps) {
    if (debug) {
      String out = "[DEBUG] " + name;
      for (int i = 0; i < numOps; i++) {
        if (i < numOps - 1 || memory[pc - 2] % 100 == 9) {
          out += " " + get(i);
        } else {
          out += " " + (ops[i] + (modes[i] == 2 ? rb : 0));
        }
      }
      print(out);
    }
  }

  private void print(Object... args) {
    for (Object arg : args) {
      System.out.print(arg);
    }
    System.out.println();
  }

  private void pause() {
    readString();
  }

  private int readInt() {
    return Integer.parseInt(readString());
  }

  protected static String readString() {
    return new Scanner(System.in).nextLine();
  }
}
