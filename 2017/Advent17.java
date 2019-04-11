import java.util.*;
import java.util.stream.*;

public class Advent17 extends Advent {

  private int skips = 382;
  private int position = 0;
  private List<Integer> buffer = new LinkedList<>();

  private Node circular;

  public Advent17() {
    super(17);
  }

  @Override
  protected void readInput() {

  }

  @Override
  protected void parseInput() {
    buffer.add(0);
  }

  @Override
  protected String part1() {
    for (int i = 1; i <= 2017; i++) {
      position += skips;
      position %= buffer.size();
      buffer.add(++position, i);
    }
    return "" + buffer.get(position + 1);
  }

  @Override
  protected String part2() {
    int answer = 1;
    int size = 1;
    for (int i = 1; i <= 50_000_000; i++) {
      position += skips;
      position %= size;
      position++;
      size++;
      if (position == 1) answer = i;
      //buffer.add(++position, i);
      //if (i % 50_000 == 0) sop(".");
    }
    //sopl();
    return "" + answer;
    /*
    circular = circular(0);
    for (int i = 1; i <= 50_000_000; i++) {
      circular = skip(circular, skips);
      circular.addNext(i);
      circular = circular.next;
      if (i % 50_000 == 0) sop(".");
    }
    sopl();
    while (circular.value != 0)
      circular = circular.next;
    return "" + circular.next.value;*/
  }

  private Node skip(Node node, int howMany) {
    for (int i = 0; i < howMany; i++)
      node = node.next;
    return node;
  }

  private Node circular(int value) {
    Node result = new Node(value);
    result.next = result;
    return result;
  }

  class Node {
    int value;
    Node next;

    Node(int value) {
      this.value = value;
    }

    void addNext(int value) {
      Node node = new Node(value);
      node.next = this.next;
      this.next = node;
    }
  }
}
