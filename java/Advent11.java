import java.util.*;
import java.util.stream.*;

public class Advent11 extends Advent {

  private static final Point UP    = new Point( 0, 1);
  private static final Point DOWN  = new Point( 0,-1);
  private static final Point LEFT  = new Point(-1, 0);
  private static final Point RIGHT = new Point( 1, 0);

  private Map<Point, Character> paint;
  private Point position;
  private Point direction;

  private long[] memory;
  private IntCodeMachine machine;

  private int xmin = Integer.MAX_VALUE;
  private int xmax = Integer.MIN_VALUE;
  private int ymin = Integer.MAX_VALUE;
  private int ymax = Integer.MIN_VALUE;

  public Advent11() {
    super(11);
  }

  @Override
  protected void parseInput() {
    memory = Arrays.stream(input.get(0).split(","))
      .mapToLong(Long::valueOf)
      .toArray();
    position = new Point(0,0);
    direction = UP;
    paint = new TreeMap<>();
    machine = new IntCodeMachine(memory);
  }

  @Override
  protected Object part1() {
    runPaintJob();
    return paint.size();
  }

  private void runPaintJob() {
    while (!machine.finished) {
      input();
      machine.run();
      paint();
      turn();
      advance();
    }
  }

  private void input() {
    char currentPaint = paint.getOrDefault(position, '.');
    machine.input(currentPaint == '#' ? 1 : 0);
  }

  private void paint() {
    int l = machine.programOutputs.size();
    long fromMachine = machine.programOutputs.get(l - 2);
    char newPaint = fromMachine == 1 ? '#' : '.';
    paint.put(position, newPaint);
  }

  private void turn() {
    int l = machine.programOutputs.size();
    long fromMachine = machine.programOutputs.get(l - 1);
    if (fromMachine == 1) {
      direction = new Point(   direction.y, -1*direction.x);
    } else {
      direction = new Point(-1*direction.y,    direction.x);
    }
  }

  private void advance() {
    position = position.add(direction);
  }

  @Override
  protected Object part2() {
    parseInput();
    paint.put(position, '#');
    runPaintJob();
    findBounds();
    printGrid();
    return "See above";
  }

  private void findBounds() {
    for (Point p : paint.keySet())
      if (paint.get(p) == '#') {
        if (p.x < xmin) xmin = p.x;
        if (p.x > xmax) xmax = p.x;
        if (p.y < ymin) ymin = p.y;
        if (p.y > ymax) ymax = p.y;
      }
  }

  private void printGrid() {
    for (int y = ymax; y >= ymin; y--) {
      for (int x = xmin; x <= xmax; x++) {
        Point pos = new Point(x,y);
        char currentPaint = paint.getOrDefault(pos, ' ');
        currentPaint = currentPaint == '#' ? '#' : ' ';
        sop(currentPaint , ' ');
      }
      sopl();
    }
  }
}
