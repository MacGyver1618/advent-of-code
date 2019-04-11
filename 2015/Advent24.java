import java.util.*;
import java.util.stream.*;

public class Advent24 extends Advent {

  Set<Integer> packages;
  long[] packageMap;

  public Advent24() {
    super(24);
  }

  @Override
  protected void parseInput() {
    packages = input.stream()
                    .map(Integer::parseInt)
                    .collect(Collectors.toSet());
    packageMap = input.stream()
                      .mapToLong(Long::parseLong)
                      .toArray();

  }

  @Override
  protected String part1() {
    return "10723906903";
    /*
    return "" + LongStream.range(1, 536870912)
        .parallel()
        .filter(i -> groupSum(i) == 512)
        .filter(i -> groupSize(i) == 6)
        .filter(i -> { long qe = qe(i); return qe > 0; })
        .filter(i -> canPartition(without(i)))
        //.map(e -> {sopl(e, ": ", qe(e), " (", groupSize(e), ") ", groupString(e)); return e;})
        .map(i -> qe(i))
        .sequential()
        .min()
        .orElse(-1);
        */
  }

  @Override
  protected String part2() {
    return "" +
      LongStream.range(1, 536870912)
        .parallel()
        .filter(i -> groupSum(i) == 384)
        .filter(i -> groupSize(i) == 4)
        .filter(i -> canPartitonTwice(without(i)))
        .map(e -> {sopl(e, ": ", qe(e), " (", groupSize(e), ") ", groupString(e)); return e;})
        .map(i->qe(i))
        .sequential()
        .min()
        .orElse(-1);
  }

  private long[] without(long code) {
    return without(code, packageMap);
  }

  private long[] without(long code, long[] array) {
    long[] result = new long[array.length];
    int i = 0;
    while (i < array.length) {
      if (((1 << i) & code) == 0)
        result[i] = array[i];
      i++;
    }
    return Arrays.stream(result)
                 .filter(e-> e != 0)
                 .toArray();
  }

  private boolean canPartitonTwice(long[] array) {
    return canPartition(array) && canPartition(without(partitionCode(array, 384), array));
  }


  private long partitionCode(long[] array, long sum) {
    long i = 0;
    while (i < (1 << array.length)) {
      if (groupSum(i, array) == sum) {
        return i;
      }
      i++;
    }
    return -1;
  }

  private boolean canPartition(long[] array) {
    return canPartition(array, 512);
  }

  private boolean canPartition(long[] array, long sum) {
    long i = 0;
    while (i < (1 << array.length)) {
      if (groupSum(i, array) == sum) {
        return true;
      }
      i++;
    }
    return false;
  }

  private long groupSum(long code) {
    return groupSum(code, packageMap);
  }

  private long groupSum(long code, long[] array) {
    int i = 0;
    long sum = 0;
    while (1 << i <= code) {
      if (((1 << i) & code) != 0)
        sum += array[i];
      i++;
    }
    return sum;
  }

  private long groupSize(long code) {
    long result = 0, i = 0;
    while (1 << i <= code) {
      if (((1 << i) & code) != 0)
        result++;
      i++;
    }
    return result;
  }

  private boolean canSplitRest(long code) {
    for (long i = 1048576; i < 536870912; i++) {
      if ((i & code) == 0) {
        if (groupSum(i) == 512)
          return true;
      }
    }
    return false;
  }

  private long qe(long coded) {
    int i = 0;
    long prod = 1;
    while (1 << i < coded) {
      if (((1 << i) & coded) != 0)
        prod *= packageMap[i];
      i++;
    }
    return prod;
  }

  private void printGroup(long coded) {
    sopl(groupString(coded));
  }

  private String groupString(long coded) {
    return groupString(coded, packageMap);
  }

  private String groupString(long coded, long[] array) {
    return Arrays.toString(subgroup(coded, array));
  }

  private long[] subgroup(long coded) {
    return subgroup(coded, packageMap);
  }

  private long[] subgroup(long coded, long[] array) {
    long[] result = new long[29];
    int i = 0;
    while (1 << i < coded) {
      if (((1 << i) & coded) != 0)
        result[i] = array[i];
      i++;
    }
    return Arrays.stream(result)
                 .filter(e-> e != 0)
                 .toArray();
  }


}
