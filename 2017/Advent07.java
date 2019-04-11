import java.util.*;
import java.util.stream.*;

public class Advent07 extends Advent {

  List<Node> nodes;
  Node root;

  public Advent07() {
    super(7);
  }

  @Override
  protected void parseInput() {
    nodes = input.stream()
                 .map(s -> s.split(" -> ")[0])
                 .map(Node::fromString)
                 .collect(Collectors.toList());
    populateTree();
    root = findRoot();
  }

  private void populateTree() {
    input.stream()
         .forEach(this::populateChildren);
  }

  private void populateChildren(String string) {
    StringTokenizer st = new StringTokenizer(string);
    Node parent = findNode(st.nextToken());
    st.nextToken(); // skip weight
    if (st.hasMoreTokens())
      st.nextToken(); // skip arrow
    while (st.hasMoreTokens()) {
      String childName = st.nextToken();
      if (childName.endsWith(","))
        childName = childName.substring(0, childName.length()-1);
      Node child = findNode(childName);
      parent.addChild(child);
    }
  }

  private Node findRoot() {
    return nodes.stream().filter(n -> n.parent == null).findFirst().orElse(null);
  }

  @Override
  protected String part1() {
    return root.name;
  }

  @Override
  protected String part2() {
    return findNode("arqoys").toString();
    //return unbalanced.toString();
  }

  private Node findNode(String name) {
    return nodes.stream()
                .filter(n -> n.name.equals(name))
                .findFirst()
                .orElse(null);
  }

  static class Node {
    String name;
    int weight;
    Node parent;
    List<Node> children = new LinkedList<>();

    static Node fromString(String string) {
      StringTokenizer st = new StringTokenizer(string);
      String name = st.nextToken();
      String w = st.nextToken();
      int weight = Integer.parseInt(w, 1, w.length()-1, 10);
      return new Node(name, weight);
    }


    Node(String name, int weight) {
      this.name = name;
      this.weight = weight;
    }

    void addChild(Node node) {
      this.children.add(node);
      node.parent = this;
    }

    int totalWeight() {
      int result = this.weight;
      for (Node child : children)
        result += child.totalWeight();
      return result;
    }

    boolean isBalanced() {
      return children.stream().mapToInt(e -> e.totalWeight()).distinct().count() > 1;
    }

    @Override
    public String toString() {
      return name + " (" + weight + ") -> " + children.stream().map(e-> e.name + " " + e.totalWeight()).collect(Collectors.joining(", "));
    }
  }
}
