import java.util.*;
import java.util.stream.*;

public class Advent25 extends Advent {

  long[] memory;
  IntCodeMachine machine;

  public Advent25() {
    super(25);
  }

  @Override
  protected void parseInput() {
    memory = Arrays.stream(input.get(0).split(","))
      .mapToLong(Long::valueOf)
      .toArray();
    machine = new IntCodeMachine(memory);
  }

  @Override
  protected Object part1() {
    /*
    Uncomment the following loop to play the text adventure.
    The list of required ingredients at the security checkpoint for
    me was:
    - cake (from science lab)
    - coin (from navigation)
    - monolith (from arcade)
    - mug (from holodeck)
    You can finish the puzzle manually by doing this sequence:
    - west
    - take cake
    - west->south
    - take monolith
    - north->west->south->east->east->east
    - take mug
    - west->west->west->north->east->east->east->south
    - take coin
    - south->west->north->north->north
    */

    while (!machine.finished) {
      machine.run();
      printOutput();
      takeInput();
    }
    return 19013632;
  }

  void printOutput() {
    machine.programOutputs.forEach(l -> sop((char)l.longValue()));
    machine.programOutputs.clear();
  }

  void takeInput() {
    String s = readString();
    s.chars().forEach(c -> machine.input(c));
    machine.input('\n');
  }

  @Override
  protected Object part2() {
    return "All done!";
  }
}
