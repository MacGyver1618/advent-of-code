import java.util.*;
import java.util.stream.*;

public class Advent14 extends Advent {

  String key = "nbysizxe";
  int[] template = new int[256];
  String[] rows = new String[128];
  int[][] grid = new int[128][128];
  boolean[][] visited = new boolean[128][128];

  public Advent14() {
    super(14);
  }

  @Override
  protected void readInput() {
    // No input file today
  }

  @Override
  protected void parseInput() {
    for (int i = 0; i < 256; i++)
      template[i] = i;
  }

  private int[] blankArray() {
    return Arrays.copyOf(template, template.length);
  }

  @Override
  protected String part1() {
    for (int i = 0; i < 128; i++)
      rows[i] = bitsOf(knotHashOf(row(i)));
    return "" + countOnes();
  }

  private int countOnes() {
    int ones = 0;
    for (String row : rows)
      for (char c : row.toCharArray())
        if (c == '1')
          ones++;
    return ones;
  }

  private String row(int number) {
    return key + "-" + number;
  }

  @Override
  protected String part2() {
    formGrid();
    //printGrid();
    return "" + countRegions();
  }

  private void printGrid() {
    for (int i = 0; i < 128; i++) {
      for (int j = 0; j < 128; j++)
        sop(grid[i][j]);
      sopl();
    }
  }

  private void formGrid() {
    for (int i = 0; i < rows.length; i++) {
      String row = rows[i];
      for (int j = 0; j < row.length(); j++)
        grid[i][j] = Integer.parseInt(row.substring(j,j+1));
    }
  }

  private int countRegions() {
    int regions = 0;
    for (int i = 0; i < 128; i++)
      for (int j = 0; j < 128; j++)
        if (!visited[i][j] && grid[i][j] == 1) {
          regions++;
          traverseRegion(i, j);
        }
    return regions;
  }

  private void traverseRegion(int i, int j) {
    if (i < 0 || j < 0 || i > 127 || j > 127)
      return;
    if (visited[i][j])
      return;
    visited[i][j] = true;
    if (grid[i][j] == 0)
      return;
    traverseRegion(i  , j-1);
    traverseRegion(i  , j+1);
    traverseRegion(i-1, j  );
    traverseRegion(i+1, j  );
  }

  private String bitsOf(String hexString) {
    String result = "";
    for (int i = 0; i < hexString.length(); i++) {
      String curHex = hexString.substring(i, i+1);
      result += fourBit(curHex);
    }
    return result;
  }

  private String fourBit(String hex) {
    int num = Integer.parseInt(hex, 16);
    String bits = Integer.toBinaryString(num);
    return String.format("%4s", bits).replace(' ', '0');
  }

  private String knotHashOf(String string) {
    int[] lengths = generateNewLengths(string);
    int[] sparse = sparseHash(blankArray(), lengths);
    int[] dense = denseHash(sparse);
    return hexDenseHash(dense);
  }

  private int[] generateNewLengths(String lengthString) {
    int[] newLengths = lengthString.chars().toArray();
    int oldLength = newLengths.length;
    newLengths = Arrays.copyOf(newLengths, oldLength+5);
    newLengths[oldLength] = 17;
    newLengths[oldLength+1] = 31;
    newLengths[oldLength+2] = 73;
    newLengths[oldLength+3] = 47;
    newLengths[oldLength+4] = 23;
    return newLengths;
  }

  private int[] sparseHash(int[] circList, int[] lengths) {
    int curPos = 0;
    int skip = 0;
    for (int i = 0; i < 64; i++) {
      for (int length : lengths) {
        reverse(circList, curPos, length);
        curPos += length + skip;
        skip++;
      }
    }
    return circList;
  }

  private void reverse(int[] circList, int startingFrom, int length) {
    int[] temp = new int[length];
    for (int i = 0; i < length; i++) {
      temp[length - i - 1] = circList[(startingFrom + i) % circList.length];
    }
    for (int i = 0; i < length; i++) {
      circList[(startingFrom + i) % circList.length] = temp[i];
    }
  }

  private int[] denseHash(int[] circList) {
    int[] denseHash = new int[16];
    for (int i = 0; i < 256; i += 16) {
      int dense = circList[i];
      for (int j = 1; j < 16; j++) {
        dense = dense ^ circList[i+j];
      }
      denseHash[i / 16] = dense;
    }
    return denseHash;
  }

  private String hexDenseHash(int[] denseHash) {
    String hexHash = "";
    for (int i : denseHash) {
      String cur = Integer.toHexString(i);
      cur = cur.length() == 1 ? "0" + cur : cur;
      hexHash += cur;
    }
    return hexHash;
  }
}
