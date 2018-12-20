import java.util.*;
import java.util.stream.*;

public class Advent20 extends Advent {

  private String regex;

  Map<Point, Integer> pathsToRooms = new TreeMap<>();

  public Advent20() {
    super(20);
  }

  @Override
  protected void readInput() {
    //readExample();
    super.readInput();
  }

  @Override
  protected void parseInput() {
    regex = input.get(0);
  }

  @Override
  protected String part1() {
    int i = 1;
    char c = regex.charAt(i);
    String s = "";
    Stack<String> stack = new Stack<>();
    Point cursor = new Point(0,0);
    Stack<Point> cursors = new Stack<>();
    int pathLength = 0;
    Stack<Integer> pathLengths = new Stack<>();
    while (c != '$') {
      switch (c) {
        case '(':
          stack.push(s);
          stack.push("(");
          cursors.push(cursor);
          pathLengths.push(pathLength);
          s = "";
          break;
        case '|':
          if (stack.peek().equals("(")) {
            stack.push(s);
            s = "";
          } else {
            String old = stack.pop();
            stack.push(old.length() > s.length() ? old : s);
          }
          cursor = cursors.peek();
          pathLength = pathLengths.peek();
          break;
        case ')':
          String old = stack.pop();
          stack.pop(); // Opening paren
          String base = stack.pop();
          base += old.length() > s.length() ? old : s;
          pathLength = pathLengths.pop();
          cursor = cursors.pop();
          s = base;
          break;
        default:
          switch (c) {
            case 'N':
              cursor = cursor.add(new Point(0,-1));
              break;
            case 'S':
              cursor = cursor.add(new Point(0,1));
              break;
            case 'W':
              cursor = cursor.add(new Point(-1,0));
              break;
            case 'E':
              cursor = cursor.add(new Point(1,0));
              break;
          }
          pathLength++;
          int oldShortest = pathsToRooms.getOrDefault(cursor, Integer.MAX_VALUE);
          if (pathLength < oldShortest) {
            pathsToRooms.put(cursor, pathLength);
          }
          s += c;
      }
      c = regex.charAt(++i);
    }
    return "" + longestShortestPath();
  }

  private int longestShortestPath() {
    return pathsToRooms.values()
                       .stream()
                       .mapToInt(Integer::intValue)
                       .max()
                       .orElseThrow(IllegalStateException::new);
  }

  @Override
  protected String part2() {
    return "" + roomsOver1000();
  }



  private long roomsOver1000() {
    return pathsToRooms.values()
                       .stream()
                       .mapToInt(Integer::intValue)
                       .filter(i -> i >= 1000)
                       .count();
  }
}
