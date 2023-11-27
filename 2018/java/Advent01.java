import java.util.*;
import java.util.stream.*;

public class Advent01 extends Advent {

  Set<Integer> freqs = new TreeSet<>();

  public Advent01() {
    super(1);
  }

  @Override
  protected void parseInput() {}

  @Override
  protected String part1() {
    return "" + input.stream()
                     .mapToInt(Integer::parseInt)
                     .sum();
  }

  @Override
  protected String part2() {
    int freq = 0;
    int l = input.size();
    int icrement = 0;
    freqs.add(freq);
    for (int i = 0; ; i++) {
      freq += Integer.parseInt(input.get(i % l));
      if (freqs.contains(freq))
        break;
      freqs.add(freq);
    }
    return freq + "";
  }
}
