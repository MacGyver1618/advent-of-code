import com.google.common.collect.Sets;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

public class Advent06 extends Advent {
  List<List<Set<String>>> groups = new ArrayList<>();

  public Advent06() {
    super(6);
  }

  @Override
  protected void parseInput() {
    for (String group : fullInput.split("\n\n")) {
      groups.add(Arrays.stream(group.split("\n"))
        .map(s -> s.split(""))
        .map(Set::of)
        .collect(Collectors.toList()));
    }
  }

  @Override
  protected Object part1() {
    return groups.stream()
      .mapToInt(this::union)
      .sum();
  }

  @Override
  protected Object part2() {
    return groups.stream()
      .mapToInt(this::intersection)
      .sum();
  }

  private int union(List<Set<String>> sets) {
    return sets.stream()
      .reduce(Sets::union)
      .get()
      .size();
  }

  private int intersection(List<Set<String>> sets) {
    return sets.stream()
      .reduce(Sets::intersection)
      .get()
      .size();
  }
}
