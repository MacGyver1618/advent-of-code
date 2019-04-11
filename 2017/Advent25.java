import java.util.*;
import java.util.stream.*;

public class Advent25 extends Advent {

  int position = 0;
  Map<Integer, Integer> tape = new TreeMap<>();
  State state = State.A;
  int steps = 12794428;


  public Advent25() {
    super(25);
  }

  @Override
  protected void readInput() {

  }

  @Override
  protected void parseInput() {

  }

  @Override
  protected String part1() {
    for (int i = 0; i < steps; i++)
      eval();
    return "" + checksum();
  }

  @Override
  protected String part2() {
    return "Not complete";
  }

  void eval() {
    int value = read();
    switch (state) {
      case A:
        if (value == 0) {
          write(1);
          move(Direction.RIGHT);
          state = State.B;
        } else {
          write(0);
          move(Direction.LEFT);
          state = State.F;
        }
        break;
      case B:
        if (value == 0) {
          write(0);
          move(Direction.RIGHT);
          state = State.C;
        } else {
          write(0);
          move(Direction.RIGHT);
          state = State.D;
        }
        break;
      case C:
        if (value == 0) {
          write(1);
          move(Direction.LEFT);
          state = State.D;
        } else {
          write(1);
          move(Direction.RIGHT);
          state = State.E;
        }
        break;
      case D:
        if (value == 0) {
          write(0);
          move(Direction.LEFT);
          state = State.E;
        } else {
          write(0);
          move(Direction.LEFT);
          state = State.D;
        }
        break;
      case E:
        if (value == 0) {
          write(0);
          move(Direction.RIGHT);
          state = State.A;
        } else {
          write(1);
          move(Direction.RIGHT);
          state = State.C;
        }
        break;
      case F:
        if (value == 0) {
          write(1);
          move(Direction.LEFT);
          state = State.A;
        } else {
          write(1);
          move(Direction.RIGHT);
          state = State.A;
        }
        break;
    }
  }

  int read() {
    return tape.getOrDefault(position, 0);
  }

  void write(int value) {
    tape.put(position, value);
  }

  void move(Direction direction) {
    switch (direction) {
      case RIGHT:
        position++;
        break;
      case LEFT:
        position--;
        break;
    }
  }

  int checksum() {
    return tape.values().stream().mapToInt(e -> e.intValue()).sum();
  }

  enum State {
    A,
    B,
    C,
    D,
    E,
    F;
  }

  enum Direction {
    LEFT,
    RIGHT;
  }
}
