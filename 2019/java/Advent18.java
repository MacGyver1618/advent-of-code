import java.util.*;
import java.util.function.*;
import java.util.stream.*;

public class Advent18 extends Advent {
  List<Character> allKeys = new ArrayList<>();
  int complete = 0;
  Map<Point, Character> grid;
  Map<Character, Point> positions;

  Map<Set<Point>, Path> paths;
  Map<String, Path> segments;

  Point startPosition;
  Point start1;
  Point start2;
  Point start3;
  Point start4;

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
      for (Point pos : Arrays.asList(startPosition, start1, start2, start3, start4)) {
        if (pos == null) continue;
        var pathFromStart = pathFrom(pos, start);
        if (pathFromStart != null) {
          Path fromCenter = new Path(pathFromStart);
          paths.put(Set.of(start, pos), fromCenter);
          segments.put(c + "", fromCenter);
        }
      }
      for (char d : allKeys) {
        Point goal = positionOf(d);
        if (start.equals(goal)) {
          continue;
        }
        if (paths.containsKey(Set.of(start, goal))) {
          continue;
        }
        var path = pathFrom(start, goal);
        if (path == null) {
          continue;
        }
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
        if (p.equals(startPosition)
          || p.equals(start1)
          || p.equals(start2)
          || p.equals(start3)
          || p.equals(start4)) {
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
    populatePart2();
    printGrid();
    populatePaths();
    return shortestTotalRoute();
  }

  private int shortestTotalRoute() {

    Map<State2, Integer> distances = new HashMap<>();
    Map<State2, State2> parents = new HashMap<>();
    State2 start = new State2();
    start.pos1 = start1;
    start.pos2 = start2;
    start.pos3 = start3;
    start.pos4 = start4;

    Queue<State2> queue = new PriorityQueue<>(
      Comparator.comparing(
        (State2 s) -> distances.getOrDefault(s, Integer.MAX_VALUE)));

    distances.put(start, 0);
    for(State2 state : start.nextStates()) {
      distances.put(state, state.distance(start));
      parents.put(state, start);
      queue.add(state);
    }

    while (!queue.isEmpty()) {
      State2 current = queue.poll();
      for (State2 neighbor : current.nextStates()) {
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
  }

  private void populatePart2() {
    start1 = startPosition.add(new Point(-1,-1));
    start2 = startPosition.add(new Point(-1,1));
    start3 = startPosition.add(new Point(1,-1));
    start4 = startPosition.add(new Point(1,1));
    grid.put(startPosition, '#');
    grid.put(startPosition.add(new Point(-1,0)), '#');
    grid.put(startPosition.add(new Point(1,0)), '#');
    grid.put(startPosition.add(new Point(0,-1)), '#');
    grid.put(startPosition.add(new Point(0,1)), '#');
    startPosition = new Point(-1,-1);
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
      return path.bitmap == anded;
    }

    int distance(State other) {
      return paths.get(Set.of(this.position, other.position)).length;
    }
  }

  class State2 {
    int bitmap;
    Point pos1;
    Point pos2;
    Point pos3;
    Point pos4;

    @Override
    public boolean equals(Object o) {
      State2 other = (State2) o;
      return this.bitmap == other.bitmap
        && this.pos1.equals(other.pos1)
        && this.pos2.equals(other.pos2)
        && this.pos3.equals(other.pos3)
        && this.pos4.equals(other.pos4);
    }

    @Override
    public int hashCode() {
      return bitmap*31
        + pos1.hashCode()*23
        + pos2.hashCode()*97
        + pos3.hashCode()*59
        + pos4.hashCode()*37;
    }

    @Override
    public String toString() {
      return pos1 + " " + pos2 + " " + pos3 + " " + pos4 + " " + found();
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

    int distance(State2 other) {
      if (!this.pos1.equals(other.pos1)) {
        return paths.get(Set.of(this.pos1, other.pos1)).length;
      }
      if (!this.pos2.equals(other.pos2)) {
        return paths.get(Set.of(this.pos2, other.pos2)).length;
      }
      if (!this.pos3.equals(other.pos3)) {
        return paths.get(Set.of(this.pos3, other.pos3)).length;
      }
      if (!this.pos4.equals(other.pos4)) {
        return paths.get(Set.of(this.pos4, other.pos4)).length;
      }
      return 0;
    }

    private boolean canReach(char target) {
      Point goal = positionOf(target);
      if (goal.equals(pos1)
        || goal.equals(pos2)
        || goal.equals(pos3)
        || goal.equals(pos4)) {
          return false;
      }
      for (Point position : Arrays.asList(pos1, pos2, pos3, pos4)) {
        var points = Set.of(position, goal);
        Path path = paths.get(points);
        if (path == null) {
          continue;
        }
        int anded = path.bitmap & this.bitmap;
        if (path.bitmap == anded) {
          return true;
        }
      }
      return false;
    }

    Set<State2> nextStates() {
      return remainingVisits().stream()
        .filter(this::canReach)
        .map(this::newState)
        .collect(Collectors.toSet());
    }

    Set<Character> remainingVisits() {
      return allKeys.stream()
        .filter(c -> (bitmap & (1 << (c - 'a'))) == 0)
        .collect(Collectors.toSet());
    }

    State2 newState(char nextTarget) {
      State2 next = new State2();
      next.pos1 = this.pos1;
      next.pos2 = this.pos2;
      next.pos3 = this.pos3;
      next.pos4 = this.pos4;
      Point nextPosition = positionOf(nextTarget);
      if (paths.containsKey(Set.of(pos1, nextPosition))) {
        next.pos1 = nextPosition;
      }
      if (paths.containsKey(Set.of(pos2, nextPosition))) {
        next.pos2 = nextPosition;
      }
      if (paths.containsKey(Set.of(pos3, nextPosition))) {
        next.pos3 = nextPosition;
      }
      if (paths.containsKey(Set.of(pos4, nextPosition))) {
        next.pos4 = nextPosition;
      }
      next.bitmap = this.bitmap + (1 << (nextTarget - 'a'));
      return next;
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
