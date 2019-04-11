import java.util.*;
import java.util.stream.*;

public class Advent19 extends Advent {

  char[][] grid = new char[201][201];
  int x, y;
  Direction direction = Direction.UP;
  String collected = "";
  int steps = 1;

  public Advent19() {
    super(19);
  }

  @Override
  protected void parseInput() {
    for (int i = 0; i < input.size(); i++) {
      String row = input.get(i);
      for (int j = 0; j < row.length(); j++) {
        grid[j][i] = row.charAt(j);
      }
    }
  }

  private void printGrid() {
    for (int i = 0; i < 201; i++) {
      for (int j = 0; j < 201; j++) {
        sop(grid[j][i]);
      }
      sopl();
    }
  }

  @Override
  protected String part1() {
    findStart();
    traverse();
    return collected;
  }

  private void findStart() {
    y = 0;
    for (x = 0; x < 201; x++) {
      if (grid[x][y] == '|')
        return;
    }
  }

  private void traverse() {
    while (canContinue()) {
      step();
      collect();
      direction = evaluateDirection();
    }
  }

  private boolean canContinue() {
    if (x < 0 || y < 0 || y > 201 || x > 201)
      return false;
    switch (direction) {
      case UP:
        return grid[x][y+1] != ' ';
      case DOWN:
        return grid[x][y-1] != ' ';
      case LEFT:
        return grid[x-1][y] != ' ';
      case RIGHT:
        return grid[x+1][y] != ' ';
    }
    return false;
  }

  private void step() {
    steps++;
    switch (direction) {
      case UP:
        y++;
        break;
      case DOWN:
        y--;
        break;
      case LEFT:
        x--;
        break;
      case RIGHT:
        x++;
        break;
    }
  }

  private void collect() {
    char current = grid[x][y];
    if (current >= 'A' && current <= 'Z')
      collected += current;
  }

  private Direction evaluateDirection() {
    if (grid[x][y] != '+')
      return direction;
    if (direction == Direction.UP || direction == Direction.DOWN) {
      if (grid[x+1][y] == '-')
        return Direction.RIGHT;
      return Direction.LEFT;
    }
    if (direction == Direction.LEFT || direction == Direction.RIGHT) {
      if (grid[x][y+1] == '|')
        return Direction.UP;
      return Direction.DOWN;
    }
    throw new IllegalStateException();
  }

  @Override
  protected String part2() {
    return "" + steps;
  }

  enum Direction {
    UP,
    LEFT,
    DOWN,
    RIGHT;
  }
}
