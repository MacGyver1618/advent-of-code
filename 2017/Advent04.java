import java.util.*;
import java.util.stream.*;

public class Advent04 extends Advent {

  public Advent04() {
    super(4);
  }

  @Override
  protected void parseInput() {

  }

  @Override
  protected String part1() {
    return "" +
      input.stream()
           .filter(this::noDuplicates)
           .count();
  }

  private boolean noDuplicates(String line) {
    List<String> words = Arrays.asList(line.split(" "));
    Set<String> set = new HashSet<>(words);
    return words.size() == set.size();
  }

  @Override
  protected String part2() {
    return ""
      + input.stream()
             .filter(this::noAnagrams)
             .count();
  }

  private boolean noAnagrams(String line) {
    List<String> words = Arrays.stream(line.split(" "))
                               .map(this::canonize)
                               .collect(Collectors.toList());
    Set<String> set = new HashSet<>(words);
    return words.size() == set.size();
  }

  private String canonize(String string) {
    char[] array = string.toCharArray();
    Arrays.sort(array);
    return new String(array);
  }
}
