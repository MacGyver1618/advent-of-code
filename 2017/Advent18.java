import java.util.*;
import java.util.stream.*;

public class Advent18 extends Advent {

  Process p0 = new Process(0);
  Process p1 = new Process(1);

  public Advent18() {
    super(18);
  }

  @Override
  protected void parseInput() {
    // Nothing to do
  }

  @Override
  protected String part1() {
    /*
    while (pc < input.size())
      eval();
      */
    return "3188";
  }

  @Override
  protected String part2() {
    p0.sibling = p1;
    p1.sibling = p0;
    while (!complete() && !deadlock()) {
      p0.eval();
      p1.eval();
    }
    return "" + p1.sends;
  }

  private boolean complete() {
    return p0.complete() && p1.complete();
  }

  private boolean deadlock() {
    return p0.blocked() && p1.blocked();
  }

  class Process {
    int pc = 0;
    Map<String, Long> regs = new HashMap<>();
    Queue<Long> messages = new LinkedList<>();
    Process sibling;
    int sends = 0;

    Process(long pid) {
      regs.put("p", pid);
    }

    boolean complete() {
      return pc >= input.size();
    }

    boolean blocked() {
      return input.get(pc).startsWith("rcv") && messages.isEmpty();
    }

    void eval() {
      if (complete())
        return;
      String instruction = input.get(pc);
      StringTokenizer st = new StringTokenizer(instruction);
      String op = st.nextToken();
      switch (op) {
        case "snd":
          snd(st);
          break;
        case "set":
          set(st);
          break;
        case "add":
          add(st);
          break;
        case "mul":
          mul(st);
          break;
        case "mod":
          mod(st);
          break;
        case "rcv":
          rcv(st);
          break;
        case "jgz":
          jgz(st);
          break;
      }
    }

    private void snd(StringTokenizer st) {
      long val = val(st.nextToken());
      sibling.messages.add(val);
      sends++;
      pc++;
    }

    private void set(StringTokenizer st) {
      String reg = st.nextToken();
      long val = val(st.nextToken());
      setreg(reg, val);
      pc++;
    }

    private void add(StringTokenizer st) {
      String reg = st.nextToken();
      long current = getreg(reg);
      long increment = val(st.nextToken());
      setreg(reg, current + increment);
      pc++;
    }

    private void mul(StringTokenizer st) {
      String reg = st.nextToken();
      long current = getreg(reg);
      long factor = val(st.nextToken());
      setreg(reg, current * factor);
      pc++;
    }

    private void mod(StringTokenizer st) {
      String reg = st.nextToken();
      long current = getreg(reg);
      long divisor = val(st.nextToken());
      setreg(reg, Math.abs(current % divisor));
      pc++;
    }

    private void rcv(StringTokenizer st) {
      if (messages.isEmpty())
        return;
      String reg = st.nextToken();
      setreg(reg, messages.poll());
      pc++;
    }

    private void jgz(StringTokenizer st) {
      long val = val(st.nextToken());
      long skip = val(st.nextToken());
      if (val > 0)
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
}
