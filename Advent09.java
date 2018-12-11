import java.util.*;
import java.util.stream.*;

public class Advent09 extends Advent {

  private static int NUM_PLAYERS = 416;
  private int LAST_MARBLE = 71617;

  public Advent09() {
    super(9);
  }

  @Override
  protected void readInput() {}

  @Override
  protected void parseInput() {}

  @Override
  protected String part1() {
    return "" + playGame(LAST_MARBLE, NUM_PLAYERS);
  }

  private long playGame(int lastMarble, int players) {
    int nextMarble = 0;
    long[] scores = new long[players];
    int currentPlayer = 0;
    CircularNode currentMarble = new CircularNode(0);
    while (nextMarble < lastMarble) {
      nextMarble++;
      if (nextMarble % 23 != 0) {
        currentMarble = currentMarble.moveClockwise(1);
        currentMarble = currentMarble.addAfter(nextMarble);
      } else {
        scores[currentPlayer] += nextMarble;
        currentMarble = currentMarble.moveCounterClockwise(7);
        scores[currentPlayer] += currentMarble.marble;
        currentMarble = currentMarble.remove();
      }
      currentPlayer = (currentPlayer + 1) % players;
    }
    return highestScore(scores);
  }

  private long highestScore(long[] scores) {
    return LongStream.of(scores)
                     .max()
                     .orElse(0);
  }

  @Override
  protected String part2() {
    return "" + playGame(LAST_MARBLE*100, NUM_PLAYERS);
  }

  class CircularNode {
    CircularNode next;
    CircularNode previous;
    int marble;

    CircularNode(int marble) {
      this.marble = marble;
      this.next = this;
      this.previous = this;
    }

    CircularNode moveClockwise(int amount) {
      return amount == 0 ? this : next.moveClockwise(amount - 1);
    }

    CircularNode moveCounterClockwise(int amount) {
      return amount == 0 ? this : previous.moveCounterClockwise(amount - 1);
    }

    CircularNode addAfter(int marble) {
      CircularNode after = new CircularNode(marble);
      after.next = this.next;
      after.previous = this;
      this.next.previous = after;
      this.next = after;
      return after;
    }

    CircularNode remove() {
      next.previous = previous;
      previous.next = next;
      return next;
    }

    @Override
    public String toString() {
      return this.previous.marble + "<-" + this.marble + "->" + this.next.marble;
    }
  }
}
