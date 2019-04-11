import java.util.*;
import java.util.stream.*;

public class Advent23 extends Advent {

  int pc = 0;
  Map<String, Long> regs = new HashMap<>();
  int muls = 0;

  public Advent23() {
    super(23);
  }

  @Override
  protected void parseInput() {

  }

  @Override
  protected String part1() {
    while (!complete())
      eval();
    return "" + muls;
  }

  @Override
  protected String part2() {
    int nonPrimes = 0;
    for (int i = 106_700; i <= 123_700; i += 17) {
      if (!isPrime(i))
        nonPrimes++;
    }
    return "" + nonPrimes;
  }

  private boolean isPrime(int n) {
    for (int i = 2; i <= Math.sqrt(n); i++) {
      if (n % i == 0)
        return false;
    }
    return true;
  }

  boolean complete() {
    return pc >= input.size();
  }

  void eval() {
    if (complete())
      return;
    String instruction = input.get(pc);
    StringTokenizer st = new StringTokenizer(instruction);
    String op = st.nextToken();
    switch (op) {
      case "set":
        set(st);
        break;
      case "sub":
        sub(st);
        break;
      case "mul":
        mul(st);
        break;
      case "jnz":
        jnz(st);
        break;
    }
  }

  private void set(StringTokenizer st) {
    String reg = st.nextToken();
    long val = val(st.nextToken());
    setreg(reg, val);
    pc++;
  }

  private void sub(StringTokenizer st) {
    String reg = st.nextToken();
    long current = getreg(reg);
    long increment = val(st.nextToken());
    setreg(reg, current - increment);
    pc++;
  }

  private void mul(StringTokenizer st) {
    String reg = st.nextToken();
    long current = getreg(reg);
    long factor = val(st.nextToken());
    setreg(reg, current * factor);
    muls++;
    pc++;
  }

  private void jnz(StringTokenizer st) {
    long val = val(st.nextToken());
    long skip = val(st.nextToken());
    if (val != 0)
      pc += skip;
    else
      pc++;
  }

  private void setreg(String reg, long val) {
    regs.put(reg, val);
  }

  private long getreg(String reg) {
    Long fromReg = regs.get(reg);
    return fromReg == null ? 0 : fromReg;
  }

  private long val(String num) {
    long val;
    try {
      val = Integer.parseInt(num);
      return val;
    } catch (NumberFormatException e) {
      return getreg(num);
    }
  }
}
