import java.util.*;
import java.util.stream.*;

public class Advent08 extends Advent {

  List<Integer> history = new ArrayList<>();
  boolean halted = false;

  List<Instruction> instructions = new ArrayList<>();

  public Advent08() {
    super(8);
  }

  @Override
  protected void parseInput() {
    for (String line : input) {
      var ss = line.split(" ");
      instructions.add(new Instruction(ss[0], Integer.parseInt(ss[1])));
    }
  }

  @Override
  protected Object part1() {
    return runLoop();
  }

  @Override
  protected Object part2() {
    halted = false;
    int current = 0;
    for (int i = 0; i < input.size(); i++) {
      if (halted) return current;
      var instruction = instructions.get(i);
      switch (instruction.op) {
        case "acc":
          continue;
        case "nop":
          instructions.set(i, new Instruction("jmp", instruction.value));
          current = runLoop();
          instructions.set(i, instruction);
          continue;
        case "jmp":
          instructions.set(i, new Instruction("nop", instruction.value));
          current = runLoop();
          instructions.set(i, instruction);
          continue;
      }
    }
    return null;
  }

  private int runLoop() {
    var state = new State(0,0);
    history = new ArrayList<>();
    while (true) {
      if (state.pc == instructions.size()) {
        halted = true;
        return state.acc;
      }
      if (history.contains(state.pc)) return state.acc;
      history.add(state.pc);
      state = instructions.get(state.pc).execute(state);
    }
  }

  record State(int pc, int acc) {}
  record Instruction(String op, Integer value) {
    State execute(State state) {
      switch(op) {
        case "nop":
          return new State(state.pc+1, state.acc);
        case "acc":
          return new State(state.pc+1, state.acc+value);
        case "jmp":
          return new State(state.pc + value, state.acc);
        default:
          return state;
      }
    }
  }
}
