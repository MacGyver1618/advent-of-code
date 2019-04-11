import java.util.*;
import java.util.stream.*;

public class Advent25 extends Advent {

  private int targetRow = 2981;
  private int targetCol = 3075;

  public Advent25() {
    super(25);
  }

  @Override
  protected void readInput() {}

  @Override
  protected void parseInput() {}

  @Override
  protected String part1() {
    int row = 1;
    int col = 1;
    int maxRow = 1;
    long val = 20151125;
    while (row != targetRow || col != targetCol) {
      if (row == 1) {
        row = maxRow + 1;
        col = 1;
        maxRow++;
      } else {
        row--;
        col++;
      }
      val = (val * 252533) % 33554393;
      if (row + col == targetRow + targetCol)
        sopl("(", row,",",col,"): ", val);
      //(new Scanner(System.in)).nextLine();
    }
    return "" + val;
  }
}
