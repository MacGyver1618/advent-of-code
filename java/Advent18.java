import java.util.*;
import java.util.function.*;
import java.util.stream.*;

public class Advent18 extends Advent {
  //List<Character> allKeys = IntStream.rangeClosed('a','z')
  List<Character> allKeys = new ArrayList<>();
  int complete = 0;
  Map<Point, Character> grid;
  Map<Character, Point> positions;

  Map<Set<Point>, Path> paths;
  Map<String, Path> segments;

  Point startPosition;

  static final int NORTH = 1;
  static final int SOUTH = 2;
  static final int WEST = 3;
  static final int EAST = 4;

  static Map<Integer, Point> directions = new HashMap<>() {{
    put(NORTH, new Point(0,-1));
    put(SOUTH, new Point(0,1));
    put(WEST, new Point(-1,0));
    put(EAST, new Point(1,0));
  }};

  int xmin = Integer.MAX_VALUE;
  int xmax = Integer.MIN_VALUE;
  int ymin = Integer.MAX_VALUE;
  int ymax = Integer.MIN_VALUE;

  public Advent18() {
    super(18);
  }

  @Override
  protected void parseInput() {
    populateGrid();
    //printGrid();
    populatePaths();
  }

  private void populateGrid() {
    grid = new TreeMap<>();
    positions = new TreeMap<>();
    for (int y = 0; y < input.size(); y++) {
      if (y < ymin)  ymin = y;
      if (y > ymax)  ymax = y;
      String line = input.get(y);
      for (int x = 0; x < line.length(); x++) {
        if (x < xmin)  xmin = x;
        if (x > xmax)  xmax = x;
        Point p = new Point(x,y);
        char c = line.charAt(x);
        grid.put(p, c);
        if (c != '#' || c != '.' || c != '@') {
          positions.put(c, p);
          if (c >= 'a' && c <= 'z') {
            allKeys.add(c);
          }
        }
        if (c == '@') {
          startPosition = p;
          grid.put(p, '.');
        }
      }
    }
    complete = allKeys.stream()
      .mapToInt(Character::charValue)
      .map(c -> c - 'a')
      .map(i -> 1 << i)
      .sum();
  }

  private void populatePaths() {
    paths = new HashMap<>();
    segments = new TreeMap<>();
    for (char c : allKeys) {
      Point start = positionOf(c);
      Path fromCenter = new Path(pathFrom(startPosition, start));
      paths.put(Set.of(start, startPosition), fromCenter);
      segments.put(c + "", fromCenter);
      for (char d : allKeys) {
        Point goal = positionOf(d);
        if (start.equals(goal)) {
          continue;
        }
        if (paths.containsKey(Set.of(start, goal))) {
          continue;
        }
        var path = pathFrom(start, goal);
        Path forward = new Path(path);
        Collections.reverse(path);
        Path reverse = new Path(path);
        paths.put(Set.of(start, goal), forward);
        segments.put(c + "" + d, forward);
        segments.put(d + "" + c, reverse);
      }
    }
  }

  private Point positionOf(char element) {
    return positions.get(element);
  }

  @Override
  protected Object part1() {
    /*
    State original = new State(startPosition);
    Queue<State> queue = new LinkedList<>();
    Set<State> seen = new HashSet<>();
    Set<State> goalStates = new HashSet<>();
    seen.add(original);
    queue.add(original);
    int length = 0;
    while (!queue.isEmpty()) {
      State current = queue.poll();
      if (current.order.length() > length) {
        length = current.order.length();
        sopl(length);
      }
      if (current.isComplete()) {
        seen.add(current);
        goalStates.add(current);
        continue;
      }
      for (State candidate : current.nextStates()) {
        if (!seen.contains(candidate)) {
          seen.add(candidate);
          queue.add(candidate);
        }
      }
    }
    return goalStates.stream()
      .mapToInt(s -> s.steps)
      .min()
      .orElseThrow(IllegalStateException::new);
      //.map(s -> s.order)
      //.collect(Collectors.toList());
      */
      return shortestRoute();
  }

  private int shortestRoute() {

    Map<State, Integer> distances = new HashMap<>();
    Map<State, State> parents = new HashMap<>();
    State start = new State(startPosition);

    Queue<State> queue = new PriorityQueue<>(
      Comparator.comparing(
        (State s) -> distances.getOrDefault(s, Integer.MAX_VALUE)));

    distances.put(start, 0);
    for(State state : start.nextStates()) {
      distances.put(state, state.distance(start));
      parents.put(state, start);
      queue.add(state);
    }

    while (!queue.isEmpty()) {
      State current = queue.poll();
      //if (current.isComplete()) {
      
      //}

      for (State neighbor : current.nextStates()) {
        int distance = distances.get(current) + neighbor.distance(current);
        if (!distances.containsKey(neighbor)) {
          queue.add(neighbor);
        }
        if (distance < distances.getOrDefault(neighbor, Integer.MAX_VALUE)) {
          distances.put(neighbor, distance);
          parents.put(neighbor, current);
        }
      }
    }

    return distances.entrySet()
      .stream()
      .filter(e -> e.getKey().isComplete())
      .mapToInt(e -> e.getValue())
      .min()
      .orElseThrow(IllegalStateException::new);

    /*

12      while Q is not empty:
13          u ← vertex in Q with min dist[u]
14
15          remove u from Q
16
17          for each neighbor v of u:           // only v that are still in Q
18              alt ← dist[u] + length(u, v)
19              if alt < dist[v]:
20                  dist[v] ← alt
21                  prev[v] ← u
22
23      return dist[], prev[]
*/
  }

  private boolean isTraversible(String s) {
    int l = s.length();
    if (l == 1) {
      return segments.get(s).bitmap == 0;
    } else {
      for (int i = 1; i < l; i++) {
        String keys = s.substring(0, i - 1);
        String segmentKey = s.substring(i-1, i+1);
        Path segment = segments.get(segmentKey);
        int mask = mask(keys);
        if ((segment.bitmap & mask) != segment.bitmap) {
          return false;
        }
      }
    }
    return true;
  }

  int mask(String s) {
    return s.chars()
      .map(c -> c - 'a')
      .map(i -> 1 << i)
      .sum();
  }

  private void printGrid() {
    StringBuffer sb = new StringBuffer();
    for (int y = ymin; y <= ymax; y++) {
      for (int x = xmin; x <= xmax; x++) {
        Point p = new Point(x,y);
        if (p.equals(startPosition)) {
          sb.append("@ ");
          continue;
        }
        char c = grid.get(p);
        sb.append(c == '.' ? ' ' : c);
        sb.append(' ');
      }
      sb.append('\n');
    }
    sopl(sb.toString());
  }

  @Override
  protected Object part2() {
    return null;
  }

  private List<Point> pathFrom(Point start, Point goal, Predicate<Point> stopCondition) {
    Set<Point> closedSet = new TreeSet<>();
    Set<Point> openSet = new TreeSet<>();
    openSet.add(start);

    Map<Point, Point> cameFrom = new TreeMap<>();
    Map<Point, Integer> gScore = new TreeMap<>();
    gScore.put(start, 0);

    Map<Point, Integer> fScore = new TreeMap<>();
    fScore.put(start, start.manhattanDistance(goal));

    while (!openSet.isEmpty()) {
      Point current = openSet.stream()
                             .sorted(Comparator.comparing(p -> fScore.getOrDefault(p, Integer.MAX_VALUE)))
                             .findFirst()
                             .orElseThrow(IllegalStateException::new);
      if (stopCondition.test(current)) {
        return reconstructPath(cameFrom, current);
      }

      openSet.remove(current);
      closedSet.add(current);

      for (Point neighbor : neighbors(current)) {
        if (closedSet.contains(neighbor)) {
          continue;
        }
        int tentative_gScore = gScore.getOrDefault(current, Integer.MAX_VALUE-1) + 1;
        if (!openSet.contains(neighbor)) {
          openSet.add(neighbor);
        } else if (tentative_gScore >= gScore.getOrDefault(neighbor, Integer.MAX_VALUE-1)) {
          continue;
        }

        cameFrom.put(neighbor, current);
        gScore.put(neighbor, tentative_gScore);
        fScore.put(neighbor, gScore.get(neighbor) + neighbor.manhattanDistance(goal));
      }
    }
    return null;
  }

  private List<Point> pathFrom(Point start, Point goal) {
    return pathFrom(start, goal, p -> p.equals(goal));
  }

  private List<Point> neighbors(Point p) {
    return Arrays.asList(NORTH, SOUTH, EAST, WEST).stream()
      .map(d -> directions.get(d).add(p))
      .filter(n -> grid.getOrDefault(n, '#') != '#')
      .collect(Collectors.toList());
  }

  private List<Point> reconstructPath(Map<Point, Point> cameFrom, Point current) {
    List<Point> totalPath = new LinkedList<>();
    totalPath.add(current);
    while (cameFrom.containsKey(current)) {
      current = cameFrom.get(current);
      totalPath.add(current);
    }
    Collections.reverse(totalPath);
    return totalPath;
  }

  class State {
    int bitmap = 0;
    Point position;

    State(Point position) {
      this.position = position;
    }

    State(State state) {
      this.bitmap = state.bitmap;
      this.position = new Point(state.position.x, state.position.y);
    }

    @Override
    public boolean equals(Object o) {
      State other = (State) o;
      return this.bitmap == other.bitmap
        && this.position.equals(other.position);
      //return this.collected.equals(other.collected);
    }

    @Override
    public int hashCode() {
      return ((bitmap + 31)*37 + position.hashCode())*37;
    }

    @Override
    public String toString() {
      return found();
    }

    String found() {
      String result = "";
      for (int i = 0; i < 26; i++) {
        if (((bitmap >> i) & 1) == 1) {
          result += (char)('a'+i);
        }
      }
      return result;
    }

    boolean isComplete() {
      return complete == bitmap;
    }

    Set<State> nextStates() {
      return remainingVisits().stream()
        .filter(this::canReach)
        .map(this::newState)
        .collect(Collectors.toSet());
    }

    Set<Character> reachables() {
      return remainingVisits().stream()
        .filter(this::canReach)
        .collect(Collectors.toSet());
    }

    Set<Character> remainingVisits() {
      return allKeys.stream()
        .filter(c -> (bitmap & (1 << (c - 'a'))) == 0)
        .collect(Collectors.toSet());
    }

    State newState(char nextTarget) {
      State next = new State(this);
      Point nextPosition = positionOf(nextTarget);
      next.position = nextPosition;
      next.bitmap += (1 << (nextTarget - 'a'));
      return next;
    }

    private boolean canReach(char target) {
      Point goal = positionOf(target);
      if (goal.equals(position)) {
        return false;
      }
      var points = Set.of(position, goal);
      Path path = paths.get(points);
      int anded = path.bitmap & this.bitmap;
      return path.bitmap == (path.bitmap & this.bitmap);
      //return collected.containsAll(path.requirements);
    }

    int distance(State other) {
      return paths.get(Set.of(this.position, other.position)).length;
    }
  }

  class Path {
    List<Point> points;
    Set<Character> requirements;
    int bitmap;
    int length;

    Path(List<Point> points) {
      this.points = new ArrayList<>(points);
      this.length = points.size() - 1;
      this.requirements = new TreeSet<>();
      for (Point point : points) {
        char c = grid.getOrDefault(point, '#');
        if (c >= 'A' && c <= 'Z') {
          char d = (char)(c + 32);
          bitmap += (1 << (d - 'a'));
          requirements.add(d);
        }
      }
    }
  }
}
