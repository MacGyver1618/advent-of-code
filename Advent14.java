import java.util.*;
import java.util.stream.*;

public class Advent14 extends Advent {

  private int NUM_RECIPES = 286051;
  private List<Integer> compareTo = List.of(2,8,6,0,5,1);
  private List<Integer> scoreBoard = new ArrayList<>(50_000_000);

  public Advent14() {
    super(14);
  }

  @Override
  protected void readInput() {}

  @Override
  protected void parseInput() {}

  @Override
  protected String part1() {
    scoreBoard.add(3);
    scoreBoard.add(7);
    int elf1 = 0;
    int elf2 = 1;
    int round = 0;
    int sum = 0;
    int score1 = 0;
    int score2 = 0;
    while (scoreBoard.size() < NUM_RECIPES + 10) {
      score1 = scoreBoard.get(elf1);
      score2 = scoreBoard.get(elf2);
      sum = score1 + score2;
      addScores(sum);
      elf1 = (elf1 + score1 + 1) % scoreBoard.size();
      elf2 = (elf2 + score2 + 1) % scoreBoard.size();
    }
    return "" + lastTen();
  }

  private void addScores(int sum) {
    int tens = sum / 10;
    int singles = sum % 10;
    if (tens != 0) {
      scoreBoard.add(tens);
    }
    scoreBoard.add(singles);
  }

  private String lastTen() {
    String result = "";
    for (int i = scoreBoard.size() - 10; i < scoreBoard.size(); i++) {
      result += scoreBoard.get(i);
    }
    return result;
  }

  @Override
  protected String part2() {
    scoreBoard.clear();
    scoreBoard.add(3);
    scoreBoard.add(7);
    int elf1 = 0;
    int elf2 = 1;
    int round = 0;
    int sum = 0;
    int score1 = 0;
    int score2 = 0;
    while (!scoreContainsTail()) {
      score1 = scoreBoard.get(elf1);
      score2 = scoreBoard.get(elf2);
      sum = score1 + score2;
      addScores(sum);
      elf1 = (elf1 + score1 + 1) % scoreBoard.size();
      elf2 = (elf2 + score2 + 1) % scoreBoard.size();
    }
    return "" + leftOfTail();
  }

  private boolean scoreContainsTail() {
    return scoreEndsWithTail() || scoreEndsWithTailPad(1);
  }

  private boolean scoreEndsWithTail() {
    return scoreEndsWithTailPad(0);
  }

  private boolean scoreEndsWithTailPad(int pad) {
    if (scoreBoard.size() < compareTo.size() + pad) return false;
    int tailStart = scoreBoard.size() - compareTo.size() - pad;
    for (int i = 0; i < compareTo.size(); i++) {
      if (scoreBoard.get(i + tailStart) != compareTo.get(i)) {
        return false;
      }
    }
    return true;
  }

  private int leftOfTail() {
    return scoreEndsWithTail() ? (scoreBoard.size() - compareTo.size()) : (scoreBoard.size() - compareTo.size() - 1);
  }
}
