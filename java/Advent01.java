import java.util.*;
import java.util.stream.*;

public class Advent01 extends Advent {

  public Advent01() {
    super(1);
  }

  @Override
  protected void parseInput() {
  }

  @Override
  protected String part1() {
    return "" + input.stream()
      .mapToLong(Long::valueOf)
      .map(i -> i / 3 - 2)
      .sum();
  }

  @Override
  protected String part2() {
    return "" + input.stream()
      .mapToLong(Long::valueOf)
      .map(this::reduceFuel)
      .sum();
  }

  private long reduceFuel(long mass) {
    long result = 0;
    long fuel = requiredFuelFor(mass);
    while (fuel > 0) {
      result += fuel;
      fuel = requiredFuelFor(fuel);
    }
    return result;
  }

  private long requiredFuelFor(long mass) {
    if (mass < 0) return 0;
    long additionalFuel = mass / 3 - 2;
    return additionalFuel > 0 ? additionalFuel : 0;
  }
}
