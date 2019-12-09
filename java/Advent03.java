import java.util.*;
import java.util.stream.*;

public class Advent03 extends Advent {

  int currentLine;
  List<String> instructions = new ArrayList<>();
  Map<Point, Character> grid = new TreeMap<>();
  List<Point> intersections = new ArrayList<>();

  public Advent03() {
    super(3);
  }

  @Override
  protected void parseInput() {}


  @Override
  protected Object part1() {
    Point origin = new Point(0,0);
    currentLine = 0;
    for (String line : input) {
      currentLine++;
      Point position = origin;
      grid.put(position, 'O');
      for (String instruction : line.split(",")) {
        position = doInstruction(position, instruction);
      }
    }

    return intersections.stream()
      .map(p -> p.manhattanDistance(origin))
      .sorted()
      .findFirst()
      .orElseThrow(IllegalStateException::new);
  }

  private Point doInstruction(Point point, String instruction) {
    char direction = instruction.charAt(0);
    int amount = Integer.parseInt(instruction.substring(1));
    for (int i = 0; i < amount; i++) {
      point = increment(point, direction);
      char currentPoint = grid.getOrDefault(point, ' ');
      if (currentLine == 2 && currentPoint == '1') {
        intersections.add(point);
        grid.put(point, 'X');
      } else {
        grid.put(point, currentLine == 1 ? '1' : '2');
      }
    }
    grid.put(point, '+');
    return point;
  }

  private Point increment(Point p, char direction) {
    switch (direction) {
      case 'U': return new Point(p.x, p.y+1);
      case 'D': return new Point(p.x, p.y-1);
      case 'L': return new Point(p.x-1, p.y);
      case 'R': return new Point(p.x+1, p.y);
      default:  throw new UnsupportedOperationException();
    }
  }

  @Override
  protected Object part2() {
    return intersections.stream()
      .mapToInt(this::totalSteps)
      .min()
      .getAsInt();
  }

  private int totalSteps(Point target) {
    int total = 0;
    outer:
    for (String line : input) {
      Point point = new Point(0,0);
      for (String instruction : line.split(",")) {
        char direction = instruction.charAt(0);
        int amount = Integer.parseInt(instruction.substring(1));
        for (int i = 0; i < amount; i++) {
          point = increment(point, direction);
          total++;
          if (point.equals(target)) {
            continue outer;
          }
        }
      }
    }
    return total;
  }
}
