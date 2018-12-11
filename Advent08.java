import java.util.*;
import java.util.stream.*;

public class Advent08 extends Advent {

  private int[] numbers;
  private Node tree;

  public Advent08() {
    super(8);
  }

  @Override
  protected void parseInput() {
    numbers = Arrays.stream(input.get(0).split(" "))
                    .mapToInt(Integer::parseInt)
                    .toArray();
    tree = parseNode(0);
  }

  private Node parseNode(int index) {
    int childCount = numbers[index];
    int metadataCount = numbers[index + 1];
    int childIndex = index + 2;
    Node node = new Node();
    node.firstIndex = index;
    int i = 0;
    Node child;
    while (i < childCount) {
      child = parseNode(childIndex);
      node.children.add(child);
      childIndex = child.lastIndex + 1;
      i++;
    }
    node.lastIndex = childIndex + metadataCount - 1;
    for (i = 0; i < metadataCount; i++) {
      node.metadata.add(numbers[childIndex + i]);
    }
    return node;
  }
  
  @Override
  protected String part1() {
    return "" + metadataSum(tree);
  }

  private int metadataSum(Node node) {
    int result = 0;
    for (int metadata : node.metadata) {
      result += metadata;
    }
    for (Node child : node.children) {
      result += metadataSum(child);
    }
    return result;
  }

  @Override
  protected String part2() {
    return "" + childSum(tree);
  }

  private int childSum(Node node) {
    int result = 0;
    if (node.children.size() == 0) {
      for (int metadata : node.metadata) {
        result += metadata;
      }
    } else {
      for (int metadata : node.metadata) {
        if (metadata == 0 || metadata > node.children.size()) {
          continue;
        } else {
          result += childSum(node.children.get(metadata - 1));
        }
      }
    }
    return result;
  }

  class Node {
    int firstIndex;
    int lastIndex;
    List<Node> children = new LinkedList<>();
    List<Integer> metadata = new LinkedList<>();
  }
}
