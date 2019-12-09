import java.util.*;
import java.util.regex.*;
import java.util.stream.*;

public class Advent06 extends Advent {

  private Pattern p = Pattern.compile("([A-Z0-9]+)\\)([A-Z0-9]+)");

  private Map<String, String> orbits;

  public Advent06() {
    super(6);
  }

  @Override
  protected void parseInput() {
    orbits = new HashMap<>();
    for (String line : input) {
      Matcher m = p.matcher(line);
      m.find();
      String center = m.group(1);
      String orbiter = m.group(2);
      orbits.put(orbiter, center);
    }
  }

  @Override
  protected Object part1() {
    return orbits.keySet().stream()
      .mapToInt(this::countOrbits)
      .sum();
  }

  private int countOrbits(String orbiter) {
    if (orbiter.equals("COM")) return 0;
    int orbitCount = 0;
    String orbited = orbits.get(orbiter);
    while (orbited != null) {
      orbitCount++;
      orbited = orbits.get(orbited);
    }
    return orbitCount;
  }

  @Override
  protected Object part2() {
    var fromYou = orbitPathFrom("YOU");
    var fromSanta = orbitPathFrom("SAN");
    return findDiff(fromYou, fromSanta);
  }

  private List<String> orbitPathFrom(String orbiter) {
    List<String> result = new ArrayList<>();
    String orbited = orbits.get(orbiter);
    while (orbited != null) {
      result.add(orbited);
      orbited = orbits.get(orbited);
    }
    return result;
  }

  private int findDiff(List<String> a, List<String> b) {
    for (int i = 1; ; i++) {
      String fromA = a.get(a.size() - i);
      String fromB = b.get(b.size() - i);
      if (!fromA.equals(fromB)) {
        return a.size() + b.size() - 2*i + 2;
      }
    }
  }
}
