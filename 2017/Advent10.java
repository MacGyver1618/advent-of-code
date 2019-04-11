import java.util.*;
import java.util.stream.*;

public class Advent10 extends Advent {

  int[] lengths = new int[] {34,88,2,222,254,93,150,0,199,255,39,32,137,136,1,167};
  int[] circList = new int[256];
  int[] denseHash = new int[16];
  String hexHash = "";
  int skip = 0;
  int curPos = 0;


  public Advent10() {
    super(10);
  }

  @Override
  protected void parseInput() {
    for (int i = 0; i < circList.length; i++)
      circList[i] = i;
  }

  @Override
  protected String part1() {
    for (int length : lengths) {
      reverse(curPos, length);
      curPos += length + skip;
      skip++;
    }
    return "" + (circList[0] * circList[1]);
  }

  private void reverse(int startingFrom, int length) {
    int[] temp = new int[length];
    for (int i = 0; i < length; i++) {
      temp[length - i - 1] = circList[(startingFrom + i) % circList.length];
    }
    for (int i = 0; i < length; i++) {
      circList[(startingFrom + i) % circList.length] = temp[i];
    }
  }

  @Override
  protected String part2() {
    parseInput();
    generateNewLengths();
    sparseHash();
    denseHash();
    hexDenseHash();
    return hexHash;
  }

  private void generateNewLengths() {
    String lengthString = input.get(0);
    int[] newLengths = lengthString.chars().toArray();
    int oldLength = newLengths.length;
    newLengths = Arrays.copyOf(newLengths, oldLength+5);
    newLengths[oldLength] = 17;
    newLengths[oldLength+1] = 31;
    newLengths[oldLength+2] = 73;
    newLengths[oldLength+3] = 47;
    newLengths[oldLength+4] = 23;
    lengths = newLengths;
  }

  private void sparseHash() {
    curPos = 0;
    skip = 0;
    for (int i = 0; i < 64; i++) {
      for (int length : lengths) {
        reverse(curPos, length);
        curPos += length + skip;
        skip++;
      }
    }
  }

  private void denseHash() {
    int dense;
    for (int i = 0; i < 256; i += 16) {
      dense = circList[i];
      for (int j = 1; j < 16; j++) {
        dense = dense ^ circList[i+j];
      }
      denseHash[i / 16] = dense;
    }
  }

  private void hexDenseHash() {
    for (int i : denseHash) {
      String cur = Integer.toHexString(i);
      cur = cur.length() == 1 ? "0" + cur : cur;
      hexHash += cur;
    }
  }
}
