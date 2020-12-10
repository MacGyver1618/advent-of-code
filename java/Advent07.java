import java.util.*;
import java.util.regex.Pattern;

public class Advent07 extends Advent {

  record Edge(String from, String to, int weight) {}

  Set<Edge> edges = new HashSet<>();

  public Advent07() {
    super(7);
  }

  @Override
  protected void parseInput() {
    for (String line : input) {
      var ss = line.split(" bags contain ");
      var node = ss[0];
      var rest = ss[1];
      if (!rest.startsWith("no")) {
        var children = rest.split(", ");
        var p = Pattern.compile("(\\d+) ([a-z]+ [a-z]+) bags?\\.?");
        for (var child : children) {
          var m = p.matcher(child);
          m.find();
          edges.add(new Edge(node, m.group(2), Integer.parseInt(m.group(1))));
        }
      }
    }
  }

  @Override
  protected Object part1() {
    var found = new HashSet<String>();
    Queue<String> queue = new ArrayDeque<>();
    queue.add("shiny gold");
    while (!queue.isEmpty()) {
      var current = queue.poll();
      for (var edge : edges) {
        if (edge.to.equals(current) && !found.contains(edge.from)) {
          found.add(edge.from);
          queue.add(edge.from);
        }
      }
    }
    return found.size();
  }

  @Override
  protected Object part2() {
    return weightOf("shiny gold")-1;
  }

  private long weightOf(String node) {
    var weight = 1L;
    for (var edge : edges) {
      if (edge.from.equals(node)) {
        weight += edge.weight * weightOf(edge.to);
      }
    }
    return weight;
  }
}
