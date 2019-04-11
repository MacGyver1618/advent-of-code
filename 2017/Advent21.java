import java.util.*;
import java.util.stream.*;

public class Advent21 extends Advent {

  private String seed = ".#./..#/###";
  private Map<String, String> rules = new HashMap<>();

  public Advent21() {
    super(21);
  }

  @Override
  protected void parseInput() {
    for (String line : input) {
      String[] rule = line.split(" => ");
      rules.put(rule[0], rule[1]);
    }
  }

  @Override
  protected String part1() {
    char[][] current = gridify(seed);
    for (int i = 0; i < 5; i++) {
      char[][] next = template(current);
      int j = 0;
      for (char[][] square : split(current)) {
        add(next, j, enhance(square));
        j++;
      }
      current = next;
    }
    return "" + countOn(current);
  }

  private void add(char[][] target, int position, char[][] subgrid) {
    int L = subgrid.length;
    int N = target.length / L;
    int row = position / N;
    int col = position % N;
    for (int i = row*L; i < row*L + L; i++)
      for (int j = col*L; j < col*L + L; j++)
        target[i][j] = subgrid[i-row*L][j-col*L];
  }

  private int countOn(char[][] grid) {
    int result = 0;
    for (int i = 0; i < grid.length; i++)
      for (int j = 0; j < grid.length; j++)
        if (grid[i][j] == '#')
          result++;
    return result;
  }

  private char[][] enhance(char[][] grid) {
    for (char[][] transformation : transformations(grid))
      if (rules.keySet().contains(linearize(transformation)))
        return gridify(rules.get(linearize(transformation)));
    throw new IllegalStateException();
  }

  private String linearize(char[][] grid) {
    String result = "";
    for (int i = 0; i < grid.length; i++) {
      for (int j = 0; j < grid.length; j++)
        result += grid[i][j];
      result += "/";
    }
    return result.substring(0, result.length() - 1);
  }

  private List<char[][]> transformations(char[][] grid) {
    List<char[][]> result = new LinkedList<>();
    result.add(grid);
    result.add(flipVertical(grid));
    result.add(flipHorizontal(grid));
    result.add(flipVertical(flipHorizontal(grid)));
    result.add(transpose(grid));
    result.add(transpose(flipVertical(grid)));
    result.add(transpose(flipHorizontal(grid)));
    result.add(transpose(flipVertical(flipHorizontal(grid))));
    return result;
  }

  private void printGrid(char[][] grid) {
    Arrays.stream(grid).forEach(e -> sopl(Arrays.toString(e)));
  }

  private char[][] gridify(String string) {
    StringTokenizer st = new StringTokenizer(string, "/");
    int n = st.countTokens();
    char[][] result = new char[n][n];
    for (int i = 0; i < n; i++) {
      result[i] = st.nextToken().toCharArray();
    }
    return result;
  }

  private char[][] transpose(char[][] grid) {
    char[][] result = new char[grid.length][grid.length];
    for (int i = 0; i < grid.length; i++)
      for (int j = 0; j < grid.length; j++)
        result[i][j] = grid[j][i];
    return result;
  }

  private char[][] flipVertical(char[][] grid) {
    char[][] result = Arrays.copyOf(grid, grid.length);
    for (int i = 0; i < result.length / 2; i++)
      result = swap(result, i, result.length - 1 - i);
    return result;
  }

  private char[][] flipHorizontal(char[][] grid) {
    char[][] result = Arrays.copyOf(grid, grid.length);
    for (int i = 0; i < result.length; i++)
      for (int j = 0; j < result.length / 2; j++)
        result[i] = swap(result[i], j, result.length - 1 -j);
    return result;
  }

  private char[][] swap(char[][] grid, int from, int to) {
    char[][] result = Arrays.copyOf(grid, grid.length);
    char[] temp = result[to];
    result[to] = result[from];
    result[from] = temp;
    return result;
  }

  private char[] swap(char[] grid, int from, int to) {
    char[] result = Arrays.copyOf(grid, grid.length);
    char temp = result[to];
    result[to] = result[from];
    result[from] = temp;
    return result;
  }

  private char[][] template(char[][] previous) {
    int n = previous.length;
    if (n % 2 == 0) {
      return new char[3*n/2][3*n/2];
    }
    return new char[4*n/3][4*n/3];
  }

  private List<char[][]> split(char[][] grid) {
    if (grid.length % 2 == 0)
      return split(grid, 2);
    return split(grid, 3);
  }

  private List<char[][]> split(char[][] grid, int n) {
    List<char[][]> result = new LinkedList<>();
    for (int i = 0; i < grid.length; i += n)
      for (int j = 0; j < grid.length; j += n)
        result.add(subgrid(grid, i, i+n, j, j+n));
    return result;
  }

  private char[][] subgrid(char[][] grid, int xmin, int xmax, int ymin, int ymax) {
    char[][] result = new char[xmax-xmin][ymax-ymin];
    for (int i = xmin; i < xmax; i++)
      for (int j = ymin; j < ymax; j++)
        result[i-xmin][j-ymin] = grid[i][j];
    return result;
  }

  @Override
  protected String part2() {
    char[][] current = gridify(seed);
    for (int i = 0; i < 18; i++) {
      char[][] next = template(current);
      int j = 0;
      for (char[][] square : split(current)) {
        add(next, j, enhance(square));
        j++;
      }
      current = next;
    }
    return "" + countOn(current);
  }
}
