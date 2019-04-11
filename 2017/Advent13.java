import java.util.*;
import java.util.stream.*;

public class Advent13 extends Advent {

  Map<Integer, Integer> gates = new TreeMap<>();

  public Advent13() {
    super(13);
  }

  @Override
  protected void parseInput() {
    input.stream().forEach(this::addGate);
  }

  private void addGate(String line) {
    String[] props = line.split(": ");
    int position = Integer.parseInt(props[0]);
    int depth = Integer.parseInt(props[1]);
    gates.put(position, depth);
  }

  @Override
  protected String part1() {
    return "" + cost(0);
  }

  private int cost(int delay) {
    int cost = 0;
    for (int i = 0; i < 100; i++) {
      cost += i*cost(i, i + delay);
    }
    return cost;
  }

  private int cost(int position, int timeInstant) {
    if (caught(position, timeInstant))
      return depth(position);
    return 0;
  }

  private boolean caught(int position, int timeInstant) {
    if (!hasGate(position))
      return false;
    int depth = depth(position);
    int cycleTime = 2*depth - 2;
    return timeInstant % cycleTime == 0;
  }

  private boolean hasGate(int position) {
    return gates.get(position) != null;
  }

  private int depth(int position) {
    return gates.get(position);
  }

  @Override
  protected String part2() {
    int delay = 0;
    while (caught(delay))
      delay++;
    return "" + delay;
  }

  private boolean caught(int delay) {
    for (int i = 0; i < 100; i++) {
      if (caught(i, i + delay))
        return true;
    }
    return false;
  }
}
