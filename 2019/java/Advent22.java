import java.math.*;
import java.util.*;
import java.util.stream.*;

public class Advent22 extends Advent {

  //int DECK_SIZE = 10;
  int DECK_SIZE = 10_007;

  List<Integer> cards;

  public Advent22() {
    super(22);
  }

  @Override
  protected void parseInput() {
    cards = IntStream.range(0,DECK_SIZE).boxed().collect(Collectors.toList());
  }

  @Override
  protected Object part1() {
    readInstructions();
    return cards.indexOf(2019);
  }

  long mod(long n) {
    return mod(n, DECK_SIZE);
  }

  long mod(long n, long k) {
    long result = n % k;
    return result < 0 ? result + k : result;
  }

  void readInstructions() {
    for (String line : input) {
      String[] ss = line.split(" ");
      if (ss[1].equals("into")) {
        dealIntoNewStack();
        continue;
      }
      if (ss[1].equals("with")) {
        dealWithIncrement(Integer.parseInt(ss[3]));
        continue;
      }
      if (ss[0].equals("cut")) {
        cut(Integer.parseInt(ss[1]));
        continue;
      }
    }
  }

  void dealIntoNewStack() {
    Collections.reverse(cards);
  }

  void dealWithIncrement(int n) {
    List<Integer> newCards = IntStream.range(0,DECK_SIZE).boxed().collect(Collectors.toList());
    for (int i = 0; i < DECK_SIZE; i++) {
      newCards.set((i*n)%DECK_SIZE, cards.get(i));
    }
    cards = newCards;
  }

  void cut(int n) {
    List<Integer> newCards = new ArrayList<>(DECK_SIZE);
    if (n < 0) {
      newCards.addAll(cards.subList(DECK_SIZE + n, DECK_SIZE));
      newCards.addAll(cards.subList(0, DECK_SIZE + n));
    } else {
      newCards.addAll(cards.subList(n, DECK_SIZE));
      newCards.addAll(cards.subList(0, n));
    }
    cards = newCards;
  }

  @Override
  protected Object part2() {
    BigInteger size = BigInteger.valueOf(119_315_717_514_047L);
    BigInteger shuffles = BigInteger.valueOf(101_741_582_076_661L);
    BigInteger skip = BigInteger.ONE;
    BigInteger start = BigInteger.ZERO;
    var reverse = new ArrayList<>(input);
    Collections.reverse(reverse);
    for (String line : reverse) {
      String[] ss = line.split(" ");
      if (ss[1].equals("into")) {
        skip = skip.negate().mod(size);
        start = start.negate().add(size).subtract(BigInteger.ONE).mod(size);
        continue;
      }
      if (ss[1].equals("with")) {
        BigInteger inc = new BigInteger(ss[3]);
        skip = skip.multiply(inc.modInverse(size)).mod(size);
        start = start.multiply(inc.modInverse(size)).mod(size);
        continue;
      }
      if (ss[0].equals("cut")) {
        BigInteger amt = new BigInteger(ss[1]);
        start = start.add(amt).mod(size);
        continue;
      }
    }
    start = start.multiply(skip.modPow(shuffles, size).subtract(BigInteger.ONE).multiply(skip.subtract(BigInteger.ONE).modInverse(size)));
    skip = skip.modPow(shuffles, size);
    return BigInteger.valueOf(2020).multiply(skip).add(start).mod(size);
  }

  void printArr(BigInteger skip, BigInteger start) {
    var res = IntStream.range(0, 10)
      .mapToObj(BigInteger::valueOf)
      .map(skip::multiply)
      .map(start::add)
      .map(n -> n.mod(BigInteger.valueOf(DECK_SIZE)))
      .map(BigInteger::intValue)
      .collect(Collectors.toList());
    for (int i = 0; i < res.size(); i++) {
      cards.set(res.get(i), i);
    }
    sopl(cards);
  }
}
