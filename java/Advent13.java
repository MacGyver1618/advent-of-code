import java.util.*;
import java.util.concurrent.*;
import java.util.stream.*;

public class Advent13 extends Advent {

  StringBuffer screenBuffer;
  long score = 0;
  long[] memory;
  IntCodeMachine machine;
  Map<Point, Integer> grid;

  Point position;

  int xmin = Integer.MAX_VALUE;
  int xmax = Integer.MIN_VALUE;
  int ymin = Integer.MAX_VALUE;
  int ymax = Integer.MIN_VALUE;

  public Advent13() {
    super(13);
  }

  @Override
  protected void parseInput() {
    memory = Arrays.stream(input.get(0).split(","))
      .mapToLong(Long::valueOf)
      .toArray();
    machine = new IntCodeMachine(memory);
    grid = new TreeMap<>();
  }

  @Override
  protected Object part1() {
    while (!machine.finished) {
      machine.run();
    }
    populateGrid();
    return grid.values().stream()
      .filter(i -> i == 2)
      .count();
  }

  private void populateGrid() {
    for (int i = 0; i < machine.programOutputs.size(); i += 3) {
      long x = machine.programOutputs.get(i);
      long y = machine.programOutputs.get(i+1);
      long tile = machine.programOutputs.get(i+2);
      if (x == -1 && y == 0) {
        score = tile;
      } else {
        grid.put(new Point((int)x,(int)y), (int)tile);
      }
    }
  }

  @Override
  protected Object part2() {
    try {
      memory[0] = 2;
      grid = new TreeMap<>();
      machine = new IntCodeMachine(memory);
      runGameVisual();
    } catch (Exception e) {
      sopl(e);
    }
    return score;
  }

  private void runGameAutomatic() {
    while (!machine.finished) {
      machine.run();
      populateGrid();
      machine.programOutputs.clear();
      machine.input(findBallPaddleXdiff());
    }
  }

  private void runGameVisual() throws InterruptedException {
    while (!machine.finished) {
      machine.run();
      populateGrid();
      printGame();
      machine.programOutputs.clear();
      machine.input(findBallPaddleXdiff());
      Thread.sleep(20);
    }
  }

  private void runGameInteractive() throws InterruptedException {
    while (!machine.finished) {
      machine.run();
      populateGrid();
      printGame();
      machine.programOutputs.clear();
      machine.input(readDirection());
      Thread.sleep(20);
    }
  }

  private int readDirection() {
    return 0;
  }

  private int findBallPaddleXdiff() {
    int ballX = -1;
    int paddleX = -1;
    for (var entry : grid.entrySet()) {
      if (entry.getValue() == 4) {
        ballX = entry.getKey().x;
      }
      if (entry.getValue() == 3) {
        paddleX = entry.getKey().x;
      }
    }
    return (int) Math.signum(ballX - paddleX);
  }

  private void printGame() {
    screenBuffer = new StringBuffer();
    printEmptyLines(20);
    printMany(' ', 65);
    screenBuffer.append("Score: ").append(score).append("\n");
    findBounds();
    printGrid(50);
    printEmptyLines(10);
    sopl(screenBuffer.toString());
  }

  private void printEmptyLines(int howMany) {
    printMany("\n", howMany);
  }

  private void printMany(Object out, int howMany) {
    IntStream.rangeClosed(1,howMany).forEach(i -> screenBuffer.append(out));
  }

  private void findBounds() {
    xmin = Integer.MAX_VALUE;
    xmax = Integer.MIN_VALUE;
    ymin = Integer.MAX_VALUE;
    ymax = Integer.MIN_VALUE;
    for (Point p : grid.keySet()) {
      if (p.x < xmin) xmin = p.x;
      if (p.x > xmax) xmax = p.x;
      if (p.y < ymin) ymin = p.y;
      if (p.y > ymax) ymax = p.y;
    }
  }

  private void printGrid(int leftPad) {
    for (int y = ymin; y <= ymax; y++) {
      printMany(' ', leftPad);
      for (int x = xmin; x <= xmax; x++) {
        switch (grid.getOrDefault(new Point(x,y), 0)) {
          case 0: screenBuffer.append(' '); break;
          case 1: screenBuffer.append('|'); break;
          case 2: screenBuffer.append('#'); break;
          case 3: screenBuffer.append('-'); break;
          case 4: screenBuffer.append('O'); break;
        }
      }
      screenBuffer.append("\n");
    }
  }
}
