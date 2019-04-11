import java.util.*;
import java.util.stream.*;

public class Advent16 extends Advent {

  List<String> instructions = new ArrayList<>();
  char[] programs;
  List<String> history = new LinkedList<>();

  public Advent16() {
    super(16);
  }

  @Override
  protected void parseInput() {
    StringTokenizer st = new StringTokenizer(input.get(0), ",");
    while (st.hasMoreTokens())
      instructions.add(st.nextToken());
    generateTemplate();
  }

  private void generateTemplate() {
    programs = new char[16];
    for (int i = 0; i < 16; i++)
      programs[i] = (char)('a' + (char)i);
  }

  @Override
  protected String part1() {
    for (String instruction : instructions) {
      eval(instruction);
    }
    return new String(programs);
  }

  private void eval(String instruction) {
    char op = instruction.charAt(0);
    String args = instruction.substring(1);
    switch (op) {
      case 's':
        spin(args);
        break;
      case 'x':
        exchange(args);
        break;
      case 'p':
        pair(args);
        break;
    }
  }

  private void spin(String args) {
    int howMany = Integer.parseInt(args);
    spin(howMany);
  }

  private void spin(int n) {
    char[] newPrograms = new char[16];
    int len = programs.length;
    for (int i = 0; i < len; i++) {
      newPrograms[i] = programs[(i + len - n) % len];
    }
    programs = newPrograms;
  }

  private void exchange(String args) {
    String[] whichOnes = args.split("/");
    int from = Integer.parseInt(whichOnes[0]);
    int to = Integer.parseInt(whichOnes[1]);
    swap(from, to);
  }

  private void pair(String args) {
    char from = args.charAt(0);
    char to = args.charAt(2);
    swap(positionOf(from), positionOf(to));
  }

  private int positionOf(char c) {
    for (int i = 0; i < programs.length; i++) {
      if (programs[i] == c)
        return i;
    }
    return -1;
  }

  private void swap(int a, int b) {
    char temp = programs[a];
    programs[a] = programs[b];
    programs[b] = temp;
  }

  @Override
  protected String part2() {
    generateTemplate();
    for (int i = 0; i < 1_000_000_000; i++) {
      String current = new String(programs);
      if (!history.contains(current)) {
        history.add(current);
        dance();
      } else {
        return findLoop(current, i);
      }
    }
    return "shouldn't get this far";
  }

  private void dance() {
    for (String instruction : instructions) {
      eval(instruction);
    }
  }

  private String findLoop(String perm, int i) {
    int loopSize = i - history.indexOf(perm);
    int head = history.size() - loopSize;
    return history.get(1_000_000_000 % loopSize);
  }
}
