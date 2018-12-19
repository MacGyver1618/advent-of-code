import java.util.*;
import java.util.stream.*;

public class Advent19 extends Advent {

  int pc = 0;
  int pcReg;
  int[] regs;
  List<String> instructions;

  public Advent19() {
    super(19);
  }

  @Override
  protected void parseInput() {
    pc = 0;
    regs = new int[6];
    instructions = new ArrayList<>();
    for (String line : input) {
      if (line.startsWith("#")) {
        pcReg = Integer.parseInt(line.split(" ")[1]);
      } else {
        instructions.add(line);
      }
    }
  }

  @Override
  protected String part1() {
    runProgram();
    return "" + regs[0];
  }

  private void runProgram() {
    while(pc < instructions.size()) {
      regs[pcReg] = pc;
      eval(instructions.get(pc));
      pc = regs[pcReg];
      pc++;
    }
  }

  private void eval(String instruction) {
    String[] groups = instruction.split(" ");
    String op = groups[0];
    int a = Integer.parseInt(groups[1]);
    int b = Integer.parseInt(groups[2]);
    int c = Integer.parseInt(groups[3]);
    eval(op, a, b, c);
  }

  private void eval(String op, int a, int b, int c) {
    switch(op) {
      case "addr":
        addr(a, b, c); break;
      case "addi":
        addi(a, b, c); break;
      case "mulr":
        mulr(a, b, c); break;
      case "muli":
        muli(a, b, c); break;
      case "banr":
        banr(a, b, c); break;
      case "bani":
        bani(a, b, c); break;
      case "borr":
        borr(a, b, c); break;
      case "bori":
        bori(a, b, c); break;
      case "setr":
        setr(a, b, c); break;
      case "seti":
        seti(a, b, c); break;
      case "gtir":
        gtir(a, b, c); break;
      case "gtri":
        gtri(a, b, c); break;
      case "gtrr":
        gtrr(a, b, c); break;
      case "eqir":
        eqir(a, b, c); break;
      case "eqri":
        eqri(a, b, c); break;
      case "eqrr":
        eqrr(a, b, c); break;
      default:
        throw new UnsupportedOperationException();
    }
  }

  private void addr(int a, int b, int c) {
    regs[c] = regs[a] + regs[b];
  }

  private void addi(int a, int b, int c) {
    regs[c] = regs[a] + b;
  }

  private void mulr(int a, int b, int c) {
    regs[c] = regs[a]*regs[b];
  }

  private void muli(int a, int b, int c) {
    regs[c] = regs[a]*b;
  }

  private void banr(int a, int b, int c) {
    regs[c] = regs[a] & regs[b];
  }

  private void bani(int a, int b, int c) {
    regs[c] = regs[a] & b;
  }

  private void borr(int a, int b, int c) {
    regs[c] = regs[a] | regs[b];
  }

  private void bori(int a, int b, int c) {
    regs[c] = regs[a] | b;
  }

  private void setr(int a, int b, int c) {
    regs[c] = regs[a];
  }

  private void seti(int a, int b, int c) {
    regs[c] = a;
  }

  private void gtir(int a, int b, int c) {
    regs[c] = a > regs[b] ? 1 : 0;
  }

  private void gtri(int a, int b, int c) {
    regs[c] = regs[a] > b ? 1 : 0;
  }

  private void gtrr(int a, int b, int c) {
    regs[c] = regs[a] > regs[b] ? 1 : 0;
  }

  private void eqir(int a, int b, int c) {
    regs[c] = a == regs[b] ? 1 : 0;
  }

  private void eqri(int a, int b, int c) {
    regs[c] = regs[a] == b ? 1 : 0;
  }

  private void eqrr(int a, int b, int c) {
    regs[c] = regs[a] == regs[b] ? 1 : 0;
  }

  @Override
  protected String part2() {
    /*
    This day was about reverse engineering. It sets the final register
    to a large number, and asks us to sum its factors. For my input, the
    large number was 10551329.
    */
    int result = 0;
    int n = 10551329;
    for (int i = 1; i <= n; i++) {
      if (n % i == 0) {
        result += i;
      }
    }
    return "" + result;
  }
}
