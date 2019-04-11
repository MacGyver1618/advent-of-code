import java.util.*;
import java.util.stream.*;
import java.io.*;

public class Advent03 extends Advent {

  private int input = 368078;
  private Map<Point, Integer> grid = new HashMap<>();

  public Advent03() {
    super(3);
  }

  @Override
  protected void readInput() {

  }

  @Override
  protected void parseInput() {

  }

  @Override
  protected String part1() {
    int x = 0, y = 0;
    int sideLength = 0;
    int current = 1;
    int remaining = input - current;
    while (current < input) {
      x++;
      current++;
      sideLength += 2;
      // go up
      if ((input - current) > sideLength) {
        y += (sideLength-1);
        current += (sideLength-1);
      } else if ((input - current) > 0) {
        y += (input - current);
        current += (input - current);
      }
      // go left
      if ((input - current) > sideLength) {
        x -= sideLength;
        current += sideLength;
      } else if ((input - current) > 0) {
        x -= (input - current);
        current -= (input - current);
      }
      // go down
      if ((input - current) > sideLength) {
        y -= sideLength;
        current += sideLength;
      } else if ((input - current) > 0) {
        y -= (input - current);
        current += (input - current);
      }
      // go right
      if ((input - current) > sideLength) {
        x += sideLength;
        current += sideLength;
      } else if ((input - current) > 0) {
        x += (input - current);
        current += (input - current);
      }
    }
    return "" + (Math.abs(x) + Math.abs(y));
  }

  @Override
  protected String part2() {

    Scanner scanner = new Scanner(System.in);
    int x = 0, y = 0;
    Point currentPoint = new Point(x,y);
    int currentValue = 1;
    grid.put(currentPoint, currentValue);
    while (currentValue < input) {
      currentPoint = advancePoint(currentPoint);
      currentValue = evaluatePoint(currentPoint);
      grid.put(currentPoint, currentValue);
    }
    return "" + currentValue;
  }

  private Point advancePoint(Point point) {
    if (hasLeft(point) && !hasUp(point))
      return upFrom(point);
    if (hasDown(point))
      return leftFrom(point);
    if (hasRight(point))
      return downFrom(point);
    return rightFrom(point);
  }

  private Point leftFrom(Point point) {
    return new Point(point.x-1, point.y);
  }

  private Point rightFrom(Point point) {
    return new Point(point.x+1, point.y);
  }

  private Point upFrom(Point point) {
    return new Point(point.x, point.y+1);
  }

  private Point downFrom(Point point) {
    return new Point(point.x, point.y-1);
  }

  private int evaluatePoint(Point point) {
    int x = point.x, y = point.y;
    return valueOf(x+1,y+1) +
           valueOf(x+1,y)   +
           valueOf(x+1,y-1) +
           valueOf(x,y+1)   +
           valueOf(x,y-1)   +
           valueOf(x-1,y+1) +
           valueOf(x-1,y)   +
           valueOf(x-1,y-1);
  }

  private int valueOf(int x, int y) {
    Point point = new Point(x,y);
    Integer value = grid.get(point);
    return (value == null) ? 0 : value;
  }

  private boolean hasLeft(Point point) {
    return leftOf(point) != null;
  }

  private boolean hasRight(Point point) {
    return rightOf(point) != null;
  }

  private boolean hasUp(Point point) {
    return upOf(point) != null;
  }

  private boolean hasDown(Point point) {
    return downOf(point) != null;
  }

  private Integer leftOf(Point point) {
    return grid.get(new Point(point.x-1, point.y));
  }

  private Integer rightOf(Point point) {
    return grid.get(new Point(point.x+1, point.y));
  }

  private Integer upOf(Point point) {
    return grid.get(new Point(point.x, point.y+1));
  }

  private Integer downOf(Point point) {
    return grid.get(new Point(point.x, point.y-1));
  }

  class Point {
    public int x, y;
    Point(int x, int y) {
      this.x = x;
      this.y = y;
    }

    @Override
    public int hashCode() {
      return 1000000*x + y;
    }

    @Override
    public boolean equals(Object o) {
      Point other = (Point) o;
      return other.x == this.x && other.y == this.y;
    }

    @Override
    public String toString() {
      return "(" + x + "," + y + ")";
    }
  }
}
