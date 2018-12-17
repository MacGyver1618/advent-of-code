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
    while (true) {
      score1 = scoreBoard.get(elf1);
      score2 = scoreBoard.get(elf2);
      sum = score1 + score2;
      int tens = sum / 10;
      int singles = sum % 10;
      if (tens != 0) {
        scoreBoard.add(tens);
        if (scoreBoard.size() == NUM_RECIPES + 10) break;
      }
      scoreBoard.add(singles);
      if (scoreBoard.size() == NUM_RECIPES + 10) break;
      elf1 = (elf1 + score1 + 1) % scoreBoard.size();
      elf2 = (elf2 + score2 + 1) % scoreBoard.size();
    }
    return lastTen();
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
    while (true) {
      score1 = scoreBoard.get(elf1);
      score2 = scoreBoard.get(elf2);
      sum = score1 + score2;
      int tens = sum / 10;
      int singles = sum % 10;
      if (tens != 0) {
        scoreBoard.add(tens);
        if (scoreEndsWithTail()) break;
      }
      scoreBoard.add(singles);
      if (scoreEndsWithTail()) break;
      elf1 = (elf1 + score1 + 1) % scoreBoard.size();
      elf2 = (elf2 + score2 + 1) % scoreBoard.size();
    }
    return "" + (scoreBoard.size() - compareTo.size());
  }

  private boolean scoreEndsWithTail() {
    if (scoreBoard.size() < compareTo.size()) return false;
    int tailStart = scoreBoard.size() - compareTo.size();
    for (int i = 0; i < compareTo.size(); i++) {
      if (scoreBoard.get(i + tailStart) != compareTo.get(i)) {
        return false;
      }
    }
    return true;
  }
}
