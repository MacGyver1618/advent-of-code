import java.util.*;
import java.util.stream.*;

public class Advent24 extends Advent {

  List<Component> components = new LinkedList<>();
  Node rootNode = new RootNode();

  public Advent24() {
    super(24);
  }

  @Override
  protected void parseInput() {
    for (String line : input) {
      String[] ports = line.split("/");
      int in = Integer.parseInt(ports[0]);
      int out = Integer.parseInt(ports[1]);
      components.add(new Component(in, out));
    }
    rootNode.unusedComponents = new LinkedList<>(components);
    rootNode.populate();
  }

  @Override
  protected String part1() {
    return "" + rootNode.strength();
  }

  @Override
  protected String part2() {
    return "" + rootNode.maxDepth();
  }

  class Node {
    List<Node> children = new LinkedList<>();
    Component component;
    List<Component> unusedComponents;
    int depth;
    int strength;

    void populate() {
      if (depth == 40)
        sopl(depth, ": ", strength);
      for (Component unused : unusedComponents) {
        if (unused.canConnect(component))
          addChild(unused);
        else if (unused.reverse().canConnect(component))
          addChildReversed(unused);
      }
      for (Node child : children) {
        child.depth = this.depth + 1;
        child.strength = this.strength + child.component.strength();
        child.populate();
      }
    }

    int strength() {
      if (children == null || children.isEmpty())
        return component.strength();
      return component.strength() +
        children.stream()
                .mapToInt(e -> e.strength())
                .max()
                .orElseThrow(IllegalStateException::new);
    }

    int maxDepth() {
      if (children.isEmpty()) {
        return depth;
      }
      return children.stream()
                     .mapToInt(e -> e.maxDepth())
                     .max()
                     .orElseThrow(IllegalStateException::new);
    }

    void addChild(Component component) {
      Node child = new Node();
      child.component = component;
      List<Component> newUnused = new LinkedList<>(unusedComponents);
      newUnused.remove(component);
      child.unusedComponents = newUnused;
      children.add(child);
    }

    void addChildReversed(Component component) {
      Node child = new Node();
      child.component = component.reverse();
      List<Component> newUnused = new LinkedList<>(unusedComponents);
      newUnused.remove(component);
      child.unusedComponents = newUnused;
      children.add(child);
    }
  }

  class RootNode extends Node {
    @Override
    void populate() {
      children = new LinkedList<>();
      for (Component unused : unusedComponents) {
        if (unused.canConnect(0))
          addChild(unused);
        else if (unused.reverse().canConnect(0))
          addChildReversed(unused);
      }
      for (Node child : children) {
        child.depth = 1;
        child.strength = child.component.strength();
        child.populate();
      }
    }

    @Override
    int strength() {
      return children.stream()
                .mapToInt(e -> e.strength())
                .max()
                .orElseThrow(IllegalStateException::new);
    }
  }

  class Component {
    int input, output;

    Component(int in, int out) {
      this.input = in;
      this.output = out;
    }

    Component reverse() {
      return new Component(output, input);
    }

    boolean canConnect(Component other) {
      return this.input == other.output;
    }

    boolean canConnect(int i) {
      return this.input == i;
    }

    int strength() {
      return input + output;
    }

    @Override
    public boolean equals(Object o) {
      Component other = (Component) o;
      return this.input == other.input && this.output == other.output;
    }
  }
}
