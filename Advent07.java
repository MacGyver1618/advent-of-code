import java.util.*;
import java.util.regex.*;
import java.util.stream.*;

public class Advent07 extends Advent {

  private static final Pattern PATTERN = Pattern.compile("Step ([A-Z]) must be finished before step ([A-Z]) can begin.");

  private Map<Character, Set<Character>> dependencyGraph = new TreeMap<>();
  private Set<Character> stepsAvailable = new TreeSet<>();
  private List<Character> stepsTaken = new LinkedList<>();

  private Map<Character, Integer> workers = new TreeMap<>();

  public Advent07() {
    super(7);
  }

  @Override
  protected void parseInput() {
    stepsTaken.clear();
    stepsAvailable.clear();
    for (String line : input) {
      Matcher m = PATTERN.matcher(line);
      m.find();
      Character dependency = m.group(1).charAt(0);
      Character dependent = m.group(2).charAt(0);
      stepsAvailable.add(dependency);
      stepsAvailable.add(dependent);
      Set<Character> dependencies = dependencyGraph.getOrDefault(dependent, new TreeSet<Character>());
      dependencies.add(dependency);
      dependencyGraph.put(dependent, dependencies);
    }
  }

  @Override
  protected String part1() {
    int finalSize = stepsAvailable.size();
    while (stepsTaken.size() < finalSize) {
      char nextStep = findAvailable().get(0);
      stepsTaken.add(nextStep);
      stepsAvailable.remove(nextStep);
    }
    return stepsTaken.stream()
                     .map(String::valueOf)
                     .collect(Collectors.joining());
  }

  private List<Character> findAvailable() {
    return stepsAvailable.stream()
                         .filter(this::canTakeStep)
                         .collect(Collectors.toList());
  }

  private boolean canTakeStep(char c) {
    Set<Character> dependencies = dependencyGraph.getOrDefault(c, Collections.emptySet());
    return stepsTaken.containsAll(dependencies);
  }

  @Override
  protected String part2() {
    parseInput();
    int timeTaken = 0;
    while (stepsTaken.size() < 26) {
      addWork();
      decrementWork();
      pruneWork();
      timeTaken++;
    }
    return "" + timeTaken;
  }

  private void addWork() {
    for (char c : findAvailable()) {
      if (workers.size() < 5) {
        workers.put(c, c - 'A' + 61);
        stepsAvailable.remove(c);
      }
    }
  }

  private void decrementWork() {
    workers.replaceAll((k,v) -> v - 1);
  }

  private void pruneWork() {
    Set<Character> completed = workers.entrySet()
                                      .stream()
                                      .filter(e -> e.getValue() == 0)
                                      .map(Map.Entry::getKey)
                                      .collect(Collectors.toSet());
    stepsTaken.addAll(completed);
    workers.keySet().removeAll(completed);
  }
}
