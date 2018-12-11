import java.io.*;
import java.util.*;
import java.util.regex.*;
import java.util.stream.*;

public class Advent10 extends Advent {

  private static Pattern PATTERN = Pattern.compile("position=<\\s*(-?\\d+),\\s*(-?\\d+)> velocity=<\\s*(-?\\d+),\\s*(-?\\d+)>");
  private List<MovingPoint> points = new LinkedList<>();
  private int secondsTaken = 0;

  public Advent10() {
    super(10);
  }

  @Override
  protected void parseInput() {
    for (String line : input) {
      Matcher m = PATTERN.matcher(line);
      m.find();
      int posX = Integer.parseInt(m.group(1));
      int posY = Integer.parseInt(m.group(2));
      int velX = Integer.parseInt(m.group(3));
      int velY = Integer.parseInt(m.group(4));
      MovingPoint point = new MovingPoint();
      point.position = new Point(posX, posY);
      point.velocity = new Point(velX, velY);
      points.add(point);
    }
  }

  @Override
  protected String part1() {
    int i = 0;
    long area = area();
    long previousArea = -1;
    boolean converged = false;
    while (true) {
      i++;
      updatePositions();
      previousArea = area;
      area = area();
      if (area > previousArea) {
        rewindPositions();
        i--;
        break;
      }
    }
    secondsTaken = i;
    printPoints();
    return "See above";
  }

  private void updatePositions() {
    for (MovingPoint point : points) {
      point.position.x += point.velocity.x;
      point.position.y += point.velocity.y;
    }
  }

  private void rewindPositions() {
    for (MovingPoint point : points) {
      point.position.x -= point.velocity.x;
      point.position.y -= point.velocity.y;
    }
  }

  private long area() {
    return (maxX() - minX() + 1) * (maxY() - minY() + 1);
  }

  private long maxX() {
    return points.stream()
                 .mapToInt(mp -> mp.position.x)
                 .max()
                 .orElse(-1);
  }

  private long minX() {
    return points.stream()
                 .mapToInt(mp -> mp.position.x)
                 .min()
                 .orElse(-1);
  }

  private long maxY() {
    return points.stream()
                 .mapToInt(mp -> mp.position.y)
                 .max()
                 .orElse(-1);
  }

  private long minY() {
    return points.stream()
                 .mapToInt(mp -> mp.position.y)
                 .min()
                 .orElse(-1);
  }

  private void printPoints() {
    try {
      PrintWriter pw = new PrintWriter("10_out.txt");
      int maxX = (int)maxX();
      int minX = (int)minX();
      int maxY = (int)maxY();
      int minY = (int)minY();
      char[][] grid = new char[maxX-minX+1][maxY-minY+1];
      for (int x = 0; x <= maxX-minX; x++) {
        for (int y = 0; y <= maxY-minY; y++) {
          grid[x][y] = '.';
        }
      }
      for (MovingPoint point : points) {
        int x = point.position.x;
        int y = point.position.y;
        grid[x-minX][y-minY] = '#';
      }
      for (int y = 0; y <= maxY-minY; y++) {
        for (int x = 0; x <= maxX-minX; x++) {
          sop(grid[x][y]);
          pw.print(grid[x][y]);
        }
        sopl();
        pw.println();
      }
      pw.flush();
    } catch (Exception e) {
      sopl(e);
    }
  }

  @Override
  protected String part2() {
    return "" + secondsTaken;
  }

  class MovingPoint {
    Point position;
    Point velocity;

    @Override
    public String toString() {
      return position.toString() + "<" + velocity.toString() + ">";
    }
  }
}
