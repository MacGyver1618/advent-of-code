import java.util.*;
import java.util.stream.*;

public class Advent15 extends Advent {

  private static final long SEED_A = 277;
  private static final long SEED_B = 349;
  private static final long FACTOR_A = 16807;
  private static final long FACTOR_B = 48271;

  public Advent15() {
    super(15);
  }

  @Override
  protected void readInput() {

  }

  @Override
  protected void parseInput() {

  }

  private boolean matches(long a, long b) {
    return (a & 65535) == (b & 65535);
  }

  @Override
  protected String part1() {
    int matches = 0;
    Generator a = new Generator(SEED_A, FACTOR_A);
    Generator b = new Generator(SEED_B, FACTOR_B);
    for (int i = 0; i < 40_000_000; i++)
      if (matches(a.next(), b.next()))
        matches++;
    return "" + matches;
  }

  @Override
  protected String part2() {
    int matches = 0;
    Generator a = new ModGenerator(SEED_A, FACTOR_A, 4);
    Generator b = new ModGenerator(SEED_B, FACTOR_B, 8);
    for (int i = 0; i < 5_000_000; i++)
      if (matches(a.next(), b.next()))
        matches++;
    return "" + matches;
  }

  class Generator {
    long current, factor;

    Generator(long seed, long factor) {
      this.current = seed;
      this.factor = factor;
    }

    long next() {
      long next = current*factor;
      next %= Integer.MAX_VALUE;
      current = next;
      return current;
    }
  }

  class ModGenerator extends Generator {

    long mod;

    ModGenerator(long seed, long factor, long mod) {
      super(seed, factor);
      this.mod = mod;
    }

    @Override
    long next() {
      long result = super.next();
      while (result % mod != 0)
        result = super.next();
      return result;
    }
  }
}
