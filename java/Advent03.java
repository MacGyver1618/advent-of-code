import java.util.*;
import java.util.stream.*;

public class Advent03 extends Advent {

  public Advent03() {
    super(3);
  }

  @Override
  protected void parseInput() {
  }

  private long slope(int ystep, int xstep) {
    int sum = 0;
    for (int j = 0, i = 0; j < input.size(); j += ystep, i +=xstep)
      if (input.get(j).charAt(i % input.get(j).length()) == '#')
        sum++;
    return sum;
  }

  @Override
  protected Object part1() {
    return slope(1,3);
  }

  @Override
  protected Object part2() {
    long product = 1;
    for (int[] slope : new int[][]{{1,1},{1,3},{1,5},{1,7},{2,1}})
      product *= slope(slope[0],slope[1]);
    return product;
  }
}
