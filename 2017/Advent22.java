import java.util.*;
import java.util.stream.*;

public class Advent22 extends Advent {

  Map<Point, State> grid;
  Direction direction;
  Point position;

  public Advent22() {
    super(22);
  }

  @Override
  protected void parseInput() {
    grid = new HashMap<>();
    direction = Direction.UP;
    position = new Point(12, 12);
    for (int y = 0; y < input.size(); y++) {
      String line = input.get(y);
      for (int x = 0; x < line.length(); x++) {
        Point key = new Point(x, 24-y);
        State value = line.charAt(x) == '#' ? State.INFECTED : State.CLEAN;
        grid.put(key, value);
      }
    }
  }

  private void turnLeft() {
    switch (direction) {
      case UP:
        direction = Direction.LEFT;
        break;
      case RIGHT:
        direction = Direction.UP;
        break;
      case DOWN:
        direction = Direction.RIGHT;
        break;
      case LEFT:
        direction = Direction.DOWN;
        break;
    }
  }

  private void turnRight() {
    switch (direction) {
      case UP:
        direction = Direction.RIGHT;
        break;
      case RIGHT:
        direction = Direction.DOWN;
        break;
      case DOWN:
        direction = Direction.LEFT;
        break;
      case LEFT:
        direction = Direction.UP;
        break;
    }
  }

  private void turn180() {
    switch (direction) {
      case UP:
        direction = Direction.DOWN;
        break;
      case RIGHT:
        direction = Direction.LEFT;
        break;
      case DOWN:
        direction = Direction.UP;
        break;
      case LEFT:
        direction = Direction.RIGHT;
        break;
    }
  }

  @Override
  protected String part1() {
    int infections = 0;
    for (int i = 0; i < 10_000; i++) {
      if (infected(position)) {
        turnRight();
        clean(position);
      } else {
        turnLeft();
        infect(position);
        infections++;
      }
      position = position.move(direction);
    }
    return "" + infections;
  }

  private void clean(Point point) {
    grid.put(point, State.CLEAN);
  }

  private void infect(Point point) {
    grid.put(point, State.INFECTED);
  }

  private void flag(Point point) {
    grid.put(point, State.FLAGGED);
  }

  private void weaken(Point point) {
    grid.put(point, State.WEAKENED);
  }

  private boolean infected(Point point) {
    State fromGrid = grid.get(point);
    return fromGrid == State.INFECTED;
  }

  private State state(Point point) {
    State fromGrid = grid.get(point);
    if (fromGrid == null)
      return State.CLEAN;
    return fromGrid;
  }

  @Override
  protected String part2() {
    parseInput();
    int infections = 0;
    for (int i = 0; i < 10_000_000; i++) {
      switch (state(position)) {
        case CLEAN:
          turnLeft();
          weaken(position);
          break;
        case WEAKENED:
          infect(position);
          infections++;
          break;
        case INFECTED:
          turnRight();
          flag(position);
          break;
        case FLAGGED:
          turn180();
          clean(position);
          break;
      }
      position = position.move(direction);
    }
    return "" + infections;
  }

  enum Direction {
    UP,
    RIGHT,
    DOWN,
    LEFT;
  }

  enum State {
    CLEAN,
    WEAKENED,
    INFECTED,
    FLAGGED;
  }

  class Point {
    int x, y;

    Point(int x, int y) {
      this.x = x;
      this.y = y;
    }

    Point move(Direction direction) {
      switch (direction) {
        case UP:
          return new Point(x, y+1);
        case DOWN:
          return new Point(x, y-1);
        case LEFT:
          return new Point(x-1, y);
        case RIGHT:
          return new Point(x+1, y);
      }
      throw new IllegalArgumentException();
    }

    @Override
    public int hashCode() {
      return x*1000+y;
    }

    @Override
    public boolean equals(Object o) {
      Point other = (Point)o;
      return this.x == other.x && this.y == other.y;
    }

    @Override
    public String toString() {
      return "(" + x + "," + y + ")";
    }
  }
}
