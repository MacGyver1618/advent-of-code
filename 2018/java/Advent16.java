import java.util.*;
import java.util.regex.*;
import java.util.stream.*;

public class Advent16 extends Advent {

  List<String> instructionTest;
  List<String> testProgram;
  Pattern regPattern = Pattern.compile("\\[(\\d), (\\d), (\\d), (\\d)\\]");
  List<String> opcodes = List.of("addr", "addi", "mulr", "muli", "banr", "bani", "borr", "bori", "setr", "seti", "gtir", "gtri", "gtrr", "eqir", "eqri", "eqrr");

  Map<Integer, List<String>> opCodeMatches = new TreeMap<>();

  public Advent16() {
    super(16);
  }

  @Override
  protected void parseInput() {
    debug = true;
    instructionTest = readFile("16_instruction_test.txt");
    testProgram = readFile("16_test_program.txt");
  }

  @Override
  protected String part1() {
    int[] before = new int[0];
    int[] instruction = new int[0];
    int[] after = new int[0];
    String line;
    int result = 0;
    for (int i = 0; i < instructionTest.size(); i++) {
      line = input.get(i);
      if (line.startsWith("Before")) {
        before = parseRegs(line);
      } else if (line.length() > 0 && line.charAt(0) <= '9') {
        instruction = parseInstruction(line);
      } else if (line.startsWith("After")) {
        after = parseRegs(line);
      } else {
        result += opCodeMatches(before, instruction, after) >= 3 ? 1 : 0;
      }
    }
    return "" + result;
  }

  private int[] parseRegs(String line) {
    Matcher m = regPattern.matcher(line);
    m.find();
    int[] result = new int[4];
    result[0] = Integer.parseInt(m.group(1));
    result[1] = Integer.parseInt(m.group(2));
    result[2] = Integer.parseInt(m.group(3));
    result[3] = Integer.parseInt(m.group(4));
    return result;
  }

  private int[] parseInstruction(String line) {
    String[] s = line.split(" ");
    int[] result = new int[4];
    result[0] = Integer.parseInt(s[0]);
    result[1] = Integer.parseInt(s[1]);
    result[2] = Integer.parseInt(s[2]);
    result[3] = Integer.parseInt(s[3]);
    return result;
  }

  private int opCodeMatches(int[] before, int[] instruction, int[] after) {
    int result = 0;
    List<String> matches = new ArrayList<>();
    for (String op : opcodes) {
      int[] testResult = testOpCode(op, instruction, before);
      if (Arrays.equals(after, testResult)) {
        result++;
        matches.add(op);
      }
    }
    intersectMatches(instruction[0], matches);
    return result;
  }

  private void intersectMatches(int opcode, List<String> matches) {
    var current = opCodeMatches.get(opcode);
    if (current != null) {
      matches.retainAll(current);
    }
    opCodeMatches.put(opcode, matches);
  }

  private int[] testOpCode(String op, int[] instruction, int[] regsBefore) {
    int[] regsAfter = new int[4];
    int a = instruction[1];
    int b = instruction[2];
    int c = instruction[3];
    switch(op) {
      case "addr":
        return addr(a, b, c, regsBefore);
      case "addi":
        return addi(a, b, c, regsBefore);
      case "mulr":
        return mulr(a, b, c, regsBefore);
      case "muli":
        return muli(a, b, c, regsBefore);
      case "banr":
        return banr(a, b, c, regsBefore);
      case "bani":
        return bani(a, b, c, regsBefore);
      case "borr":
        return borr(a, b, c, regsBefore);
      case "bori":
        return bori(a, b, c, regsBefore);
      case "setr":
        return setr(a, b, c, regsBefore);
      case "seti":
        return seti(a, b, c, regsBefore);
      case "gtir":
        return gtir(a, b, c, regsBefore);
      case "gtri":
        return gtri(a, b, c, regsBefore);
      case "gtrr":
        return gtrr(a, b, c, regsBefore);
      case "eqir":
        return eqir(a, b, c, regsBefore);
      case "eqri":
        return eqri(a, b, c, regsBefore);
      case "eqrr":
        return eqrr(a, b, c, regsBefore);
      default:
        throw new UnsupportedOperationException();
    }
  }

  private int[] addr(int a, int b, int c, int[] regsBefore) {
    int[] result = Arrays.copyOf(regsBefore, 4);
    result[c] = regsBefore[a] + regsBefore[b];
    return result;
  }

  private int[] addi(int a, int b, int c, int[] regsBefore) {
    int[] result = Arrays.copyOf(regsBefore, 4);
      result[c] = regsBefore[a] + b;
    return result;
  }

  private int[] mulr(int a, int b, int c, int[] regsBefore) {
    int[] result = Arrays.copyOf(regsBefore, 4);
    result[c] = regsBefore[a]*regsBefore[b];
    return result;
  }

  private int[] muli(int a, int b, int c, int[] regsBefore) {
    int[] result = Arrays.copyOf(regsBefore, 4);
    result[c] = regsBefore[a]*b;
    return result;
  }

  private int[] banr(int a, int b, int c, int[] regsBefore) {
    int[] result = Arrays.copyOf(regsBefore, 4);
    result[c] = regsBefore[a] & regsBefore[b];
    return result;
  }

  private int[] bani(int a, int b, int c, int[] regsBefore) {
    int[] result = Arrays.copyOf(regsBefore, 4);
    result[c] = regsBefore[a] & b;
    return result;
  }

  private int[] borr(int a, int b, int c, int[] regsBefore) {
    int[] result = Arrays.copyOf(regsBefore, 4);
    result[c] = regsBefore[a] | regsBefore[b];
    return result;
  }

  private int[] bori(int a, int b, int c, int[] regsBefore) {
    int[] result = Arrays.copyOf(regsBefore, 4);
    result[c] = regsBefore[a] | b;
    return result;
  }

  private int[] setr(int a, int b, int c, int[] regsBefore) {
    int[] result = Arrays.copyOf(regsBefore, 4);
    result[c] = regsBefore[a];
    return result;
  }

  private int[] seti(int a, int b, int c, int[] regsBefore) {
    int[] result = Arrays.copyOf(regsBefore, 4);
    result[c] = a;
    return result;
  }

  private int[] gtir(int a, int b, int c, int[] regsBefore) {
    int[] result = Arrays.copyOf(regsBefore, 4);
    result[c] = a > regsBefore[b] ? 1 : 0;
    return result;
  }

  private int[] gtri(int a, int b, int c, int[] regsBefore) {
    int[] result = Arrays.copyOf(regsBefore, 4);
    result[c] = regsBefore[a] > b ? 1 : 0;
    return result;
  }

  private int[] gtrr(int a, int b, int c, int[] regsBefore) {
    int[] result = Arrays.copyOf(regsBefore, 4);
    result[c] = regsBefore[a] > regsBefore[b] ? 1 : 0;
    return result;
  }

  private int[] eqir(int a, int b, int c, int[] regsBefore) {
    int[] result = Arrays.copyOf(regsBefore, 4);
    result[c] = a == regsBefore[b] ? 1 : 0;
    return result;
  }

  private int[] eqri(int a, int b, int c, int[] regsBefore) {
    int[] result = Arrays.copyOf(regsBefore, 4);
    result[c] = regsBefore[a] == b ? 1 : 0;
    return result;
  }

  private int[] eqrr(int a, int b, int c, int[] regsBefore) {
    int[] result = Arrays.copyOf(regsBefore, 4);
    result[c] = regsBefore[a] == regsBefore[b] ? 1 : 0;
    return result;
  }

  @Override
  protected String part2() {
    while (moreThanOnePossible()) {
      pruneSingles();
    }
    int[] regs = new int[] { 0, 0, 0, 0};
    for (String line : testProgram) {
      int[] instruction = parseInstruction(line);
      int opcode = instruction[0];
      String op = opCodeMatches.get(opcode).get(0);
      regs = testOpCode(op, instruction, regs);
    }
    return "" + regs[0];
  }

  private boolean moreThanOnePossible() {
    return opCodeMatches.values()
                        .stream()
                        .anyMatch(l -> l.size() > 1);
  }

  private void pruneSingles() {
    var singles = opCodeMatches.entrySet()
                               .stream()
                               .filter(e -> e.getValue().size() == 1)
                               .map(e -> e.getValue().get(0))
                               .collect(Collectors.toList());
    opCodeMatches.replaceAll((k,v) -> {
      var next = new ArrayList<String>(v);
      if (next.size() > 1) {
        next.removeAll(singles);
      }
      return next;
    });
  }
}
