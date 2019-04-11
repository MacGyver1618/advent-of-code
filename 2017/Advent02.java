import java.util.*;
import java.util.stream.*;

public class Advent02 extends Advent {

  public Advent02() {
    super(2);
  }

  @Override
  protected void parseInput() {}

  @Override
  protected String part1() {
    return "" + input.stream()
                     .mapToInt(this::diffLine)
                     .sum();
  }

  private int max(String line) {
    return intStream(line).max().orElse(0);
  }

  private IntStream intStream(String line) {
    return Stream.of(line.split("\\s+"))
                 .mapToInt(Integer::parseInt);
  }

  private int min(String line) {
    return intStream(line).min().orElse(0);
  }

  private int diffLine(String line) {
    return max(line) - min(line);
  }

  @Override
  protected String part2() {
    return "" + input.stream()
                     .mapToInt(this::quotient)
                     .sum();
  }

  private int quotient(String line) {
    return findQuotient(intStream(line).boxed().collect(Collectors.toList()));
  }

  private int findQuotient(List<Integer> numbers) {
    for (int number : numbers)
      for (int otherNumber : numbers)
        if (number != otherNumber && number % otherNumber == 0)
          return number / otherNumber;
    return 0;
  }
}
