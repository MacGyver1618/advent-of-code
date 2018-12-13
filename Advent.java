import java.io.*;
import java.lang.reflect.*;
import java.util.*;
import java.util.stream.*;

public abstract class Advent {

  private int dayNumber;
  protected List<String> input;

  public Advent(int day) {
    this.dayNumber = day;
  }

  protected static void sop(Object... args) {
    Arrays.stream(args).forEach(System.out::print);
  }

  protected static void sopl() {
    System.out.println();
  }

  protected static void sopl(Object... args) {
    sop(args);
    sopl();
  }

  protected static void pause() {
    readString();
  }

  protected static String readString() {
    return new Scanner(System.in).nextLine();
  }

  protected static int readInt() {
    return Integer.parseInt(readString());
  }

  protected static Map<Character, Integer> charFreqs(String s) {
    return frequencies(characterList(s));
  }

  protected static List<Character> characterList(String s) {
    return s.chars()
            .mapToObj(c -> Character.valueOf((char) c))
            .collect(Collectors.toList());
  }

  protected static <T> Map<T, Integer> frequencies(Collection<T> coll) {
    Map<T, Integer> result = new TreeMap<>();
    for (T t : coll) {
      Integer count = result.get(t);
      result.put(t, count == null ? 1 : ++count);
    }
    return result;
  }

  protected void run() {
    sopl("Day ", dayNumber, ":");
    readInput();
    long startTime = System.nanoTime();
    parseInput();
    long timeTaken = System.nanoTime() - startTime;
    sopl("  Input parsing took ", formatTime(timeTaken));
    startTime = System.nanoTime();
    String part1 = part1();
    timeTaken = System.nanoTime() - startTime;
    sopl("  Part 1 answer: ", part1, " (", formatTime(timeTaken), ")");
    startTime = System.nanoTime();
    String part2 = part2();
    timeTaken = System.nanoTime() - startTime;
    sopl("  Part 2 answer: ", part2, " (", formatTime(timeTaken), ")");
    sopl();
  }

  protected void readInput() {
    readInput((dayNumber < 10 ? "0" : "") + dayNumber + ".txt");
  }

  protected void readExample() {
    readInput((dayNumber < 10 ? "0" : "") + dayNumber + "_example.txt");
  }

  protected void readInput(String fileName) {
    try {
      BufferedReader reader = new BufferedReader(new FileReader(fileName));
      input = reader.lines().collect(Collectors.toList());
    } catch (FileNotFoundException e) {
      sopl("Could not read file ", fileName);
    }
  }

  protected void parseInput() {
    sopl("  Input parsing for day ", dayNumber, " not implemented");
  }

  protected String part1() {
    return "Not complete";
  }

  protected String part2() {
    return "Not complete";
  }

  private String formatTime(long time) {
    if (time < 1_000) return time + " ns";
    if (time < 1_000_000) return (time / 1_000) + " µs";
    if (time < 1_000_000_000) return (time / 1_000_000) + " ms";
    return (time / 1_000_000_000)  + " s";
  }

  public static void main(String... args) {
    if (args.length == 0)
      args = IntStream.rangeClosed(1,25).mapToObj(String::valueOf).toArray(String[]::new);
    sopl("*******************");
    sopl("ADVENT OF CODE 2018");
    sopl("*******************");
    sopl();
    for (String arg : args) {
      runAdvent(arg);
    }
  }

  private static void runAdvent(String number) {
    String name = "Advent";
    if (number.length() == 1)
      name += "0";
    name += number;
    try {
      Class<?> clazz = Class.forName(name);
      Advent advent = (Advent) clazz.getDeclaredConstructor().newInstance();
      advent.run();
    } catch (ClassNotFoundException e) {
      sopl("Class ", name, " not found");
    } catch (InstantiationException e) {
      sopl("Could not instantiate class ", name);
    } catch (IllegalAccessException e) {
      sopl("Could not access constructor of ", name);
    } catch (NoSuchMethodException e) {
      sopl("Could not find constructor for ", name);
    } catch (InvocationTargetException e) {
      sopl("Could not invoke constructor of ", name);
    }
  }

  class Point implements Comparable<Point> {
    int x, y;

    Point(int x, int y) {
      this.x = x;
      this.y = y;
    }

    @Override
    public boolean equals(Object other) {
      Point that = (Point) other;
      return this.x == that.x && this.y == that.y;
    }

    @Override
    public int hashCode() {
      return 1000*x + y;
    }

    @Override
    public String toString() {
      return "(" + x + "," + y + ")";
    }

    public int compareTo(Point other) {
      int xDiff = this.x - other.x;
      int yDiff = this.y - other.y;
      int coordDiff = xDiff + yDiff;
      return coordDiff != 0 ? coordDiff : xDiff != 0 ? xDiff : yDiff;
    }
  }
}
