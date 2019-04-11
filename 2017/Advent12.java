import java.util.*;
import java.util.stream.*;

public class Advent12 extends Advent {

  Map<Integer, Node> nodes = new HashMap<>();
  List<Node> unexplored = new LinkedList<>();
  int groups;

  public Advent12() {
    super(12);
  }

  @Override
  protected void parseInput() {
    input.stream().forEach(this::parseNode);
  }

  private void parseNode(String string) {
    String[] parts = string.split(" <-> ");
    int nodeNum = Integer.parseInt(parts[0]);
    Node root = getNode(nodeNum);
    String connections = parts[1];
    Arrays.stream(connections.split(", "))
          .map(Integer::valueOf)
          .map(this::getNode)
          .forEach(root::addNeighbor);
  }

  @Override
  protected String part1() {
    return "" + nodes.keySet()
                     .stream()
                     .filter(e ->  canConnect(0, e))
                     .count();
  }

  private boolean canConnect(int from, int to) {
    Route route = new Route(getNode(from), getNode(to));
    return route.pathLength() >= 0;
  }

  private boolean canConnect(Node from, Node to) {
    Route route = new Route(from, to);
    return route.pathLength() >= 0;
  }

  @Override
  protected String part2() {
    unexplored.addAll(nodes.values());
    Node current;
    while (!unexplored.isEmpty()) {
      current = unexplored.get(0);
      for (Node node : nodes.values()) {
        if (canConnect(current, node))
          unexplored.remove(node);
      }
      groups++;
    }
    return "" + groups;
  }

  private Node getNode(int number) {
    if (!nodes.keySet().contains(number))
      nodes.put(number, new Node(number));
    return nodes.get(number);
  }

  public static class Route {

    Node from, to;

    Set<Node> closedSet = new HashSet<>();
    Set<Node> openSet = new HashSet<>();
    Map<Node, Node> cameFrom = new HashMap<>();
    Map<Node, Integer> gScore = new HashMap<>();
    Map<Node, Integer> fScore = new HashMap<>();

    Route(Node from, Node to) {
      this.from = from;
      this.to = to;

      openSet.add(from);
      gScore.put(from, 0);
      fScore.put(from, 1);
    }

    int pathLength() {
      Node current;
      while (!openSet.isEmpty()) {
        current = minF();
        if (current.equals(to))
          return gScore.get(current);

        openSet.remove(current);
        closedSet.add(current);

        for (Node neighbor : current.neighbors) {
          if (closedSet.contains(neighbor))
            continue;

          if (!openSet.contains(neighbor))
            openSet.add(neighbor);

          int tentativeGScore = gScore.get(current) + 1;
          if (tentativeGScore >= gScoreFor(neighbor))
            continue;

          cameFrom.put(neighbor, current);
          gScore.put(neighbor, tentativeGScore);
          fScore.put(neighbor, gScoreFor(neighbor) + 1);
        }
      }
      return -1;
    }

    Node minF() {
      int min = 9999999;
      Node candidate = null;
      for (Node node : openSet) {
        if (fScore.containsKey(node))
          if (fScore.get(node) < min) {
            min = fScore.get(node);
            candidate = node;
          }
      }
      if (candidate == null)
        throw new NullPointerException("Did not find fScore");
      return candidate;
    }

    int gScoreFor(Node neighbor) {
      if (gScore.containsKey(neighbor))
        return gScore.get(neighbor);
      return 9999999;
    }

  }

  public static class Node {

    int number;
    List<Node> neighbors = new ArrayList<>();

    Node(int number) {
      this.number = number;
    }

    void addNeighbor(Node neighbor) {
      neighbors.add(neighbor);
    }

    void addNeighbors(List<Node> neighbors) {
      this.neighbors.addAll(neighbors);
    }

    @Override
    public int hashCode() {
      return number;
    }

    @Override
    public boolean equals(Object o) {
      Node other = (Node) o;
      return this.number == other.number;
    }
  }
}
