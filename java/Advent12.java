import java.io.*;
import java.util.*;
import java.util.stream.*;

public class Advent12 extends Advent {

  NavigableMap<Integer, Character> state = new TreeMap<>();
  Map<String, Character> transitions = new TreeMap<>();

  public Advent12() {
    super(12);
  }

  @Override
  protected void parseInput() {
    parseState(input.get(0).split(" ")[2]);
    input.subList(2, input.size())
         .stream()
         .forEach(this::parseRule);
  }

  private void parseState(String s) {
    for (int i = 0; i < s.length(); i++) {
      state.put(i, s.charAt(i));
    }
  }

  private void parseRule(String s) {
    String state = s.split(" => ")[0];
    char newState = s.split(" => ")[1].charAt(0);
    transitions.put(state, newState);
  }

  @Override
  protected String part1() {
    for (int gen = 0; gen < 20; gen++) {
      state = nextGeneration();
    }
    return "" + sumNumbers();
  }

  private NavigableMap<Integer, Character> nextGeneration() {
    NavigableMap<Integer, Character> result = new TreeMap<>();
    int first = lowerBound();
    int last = upperBound();
    for (int i = first; i <= last; i++) {
      result.put(i, nextState(i));
    }
    return result;
  }

  private int lowerBound() {
    return state.entrySet().stream()
                .filter(e -> e.getValue() == '#')
                .map(e -> e.getKey())
                .findFirst()
                .orElseThrow(IllegalStateException::new) - 2;
  }

  private int upperBound() {
    return state.entrySet().stream()
                .sorted(Comparator.comparing(Map.Entry<Integer, Character>::getKey).reversed())
                .filter(e -> e.getValue() == '#')
                .map(e -> e.getKey())
                .findFirst()
                .orElseThrow(IllegalStateException::new) + 2;
  }

  private char nextState(int pos) {
    String neighborhood = "";
    for (int i = pos - 2; i <= pos + 2; i++) {
      neighborhood += state.getOrDefault(i, '.');
    }
    return transitions.getOrDefault(neighborhood, '.');
  }


  private int sumNumbers(Map<Integer, Character> buckets) {
    return (int) buckets.entrySet()
                        .stream()
                        .filter(e -> e.getValue() == '#')
                        .mapToInt(e -> e.getKey())
                        .sum();
  }

  private int sumNumbers() {
    return sumNumbers(state);
  }

  @Override
  protected String part2() {
    /* This starts off where the previous one left off.

    This solution requires knowledge that this day is actually
    a one-dimensional variant of Conway's game of life. These games
    (also known as cellular automata) have been studied for some decades,
    and many (most? all?) initial states converge on some repeating pattern.

    I just stepped through the input manually to see whether this happens,
    and if I could determine a easy mathematical formula to predict the sum
    at a given generation. It turned out to be linear, and I tested this
    in jshell to verify against successive generations.

    My input stabilized at generation 103, where the bucket sum was 6901,
    and each successive generation had a bucket sum of 67 more.

    Uncomment this block to check for yourself, your input
    *will* differ from my literals.
    */
    NavigableMap<Integer, Character> previousState = new TreeMap<>();
    for (long gen = 20; gen < 50_000_000_000L; gen++) {
      previousState = state;
      state = nextGeneration();
      if (statePattern(state).equals(statePattern(previousState))) {
        long genDiff = sumNumbers(state) - sumNumbers(previousState);
        long baseScore = sumNumbers(previousState);
        return "" + sumAtGen(50_000_000_000L, genDiff, gen, baseScore);
      }
    }
    return "Pattern not repeating";
  }

  private String statePattern(Map<Integer, Character> stateMap) {
    String s = stateMap.entrySet().stream().map(e -> e.getValue() + "").collect(Collectors.joining());
    return s.substring(s.indexOf("#"), s.lastIndexOf("#") + 1);
  }

  private long sumAtGen(long gen, long genDiff, long firstGen, long baseScore) {
    return (gen - firstGen)*genDiff + baseScore;
  }
}
