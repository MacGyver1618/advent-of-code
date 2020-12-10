import java.io.*;
import java.lang.reflect.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;
import java.util.stream.*;

public abstract class Advent {

  private static final String INPUT_PATH = "../input/";
  private int dayNumber;
  protected List<String> input;
  protected String fullInput;

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

  protected static int toInt(String s) {
    return Integer.parseInt(s);
  }

  protected static long toLong(String s) {
    return Long.parseLong(s);
  }

  protected static double toDouble(String s) {
    return Double.parseDouble(s);
  }

  protected static void halt(int ms) {
    try {
      Thread.sleep(ms);
    } catch (Exception e) {}
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
    Object part1 = part1();
    timeTaken = System.nanoTime() - startTime;
    if (part1 == null) {
      sopl("  Part 1 not implemented");
    } else {
      sopl("  Part 1 answer: ", part1, " (", formatTime(timeTaken), ")");
    }
    startTime = System.nanoTime();
    Object part2 = part2();
    timeTaken = System.nanoTime() - startTime;
    if (part2 == null) {
      sopl("  Part 2 not implemented");
    } else {
      sopl("  Part 2 answer: ", part2, " (", formatTime(timeTaken), ")");
    }
    sopl();
  }

  protected void readInput() {
    readInput((dayNumber < 10 ? "0" : "") + dayNumber + ".txt");
  }

  protected void readExample() {
    readInput((dayNumber < 10 ? "0" : "") + dayNumber + "_example.txt");
  }

  protected void readInput(String fileName) {
    try (BufferedReader reader = new BufferedReader(new FileReader(INPUT_PATH + fileName))) {
      input = reader.lines().collect(Collectors.toList());
      fullInput = Files.readString(Path.of(INPUT_PATH + fileName));
    } catch (IOException e) {
      sopl("Could not read file ", fileName);
    }
  }

  protected abstract void parseInput();

  protected abstract Object part1();

  protected abstract Object part2();

  private static String formatTime(long nanos) {
    if (nanos < 1_000) return nanos + " ns";
    if (nanos < 1_000_000) return (nanos / 1_000) + " µs";
    if (nanos < 1_000_000_000) return (nanos / 1_000_000) + " ms";
    return (nanos / 1_000_000_000)  + " s";
  }

  public static void main(String... args) {
    if (args.length == 0)
      args = IntStream.rangeClosed(1,25).mapToObj(String::valueOf).toArray(String[]::new);
    sopl("*******************");
    sopl("ADVENT OF CODE 2020");
    sopl("*******************");
    sopl();
    long startTime = System.nanoTime();
    for (String arg : args) {
      runAdvent(arg);
    }
    long totalTime = System.nanoTime() - startTime;
    sopl("Total time taken: ", formatTime(totalTime));
    sopl();
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

  static class Point implements Comparable<Point> {
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

    int manhattanDistance(Point other) {
      return Math.abs(this.x-other.x) + Math.abs(this.y-other.y);
    }

    Point add(Point other) {
      return new Point(this.x + other.x, this.y + other.y);
    }

    Point subtract(Point other) {
      return new Point(this.x - other.x, this.y - other.y);
    }

    public int compareTo(Point other) {
      int xDiff = this.x - other.x;
      int yDiff = this.y - other.y;
      int coordDiff = xDiff + yDiff;
      return coordDiff != 0 ? coordDiff : xDiff != 0 ? xDiff : yDiff;
    }
  }

  static class Point3 implements Comparable<Point3> {
    int x, y, z;

    Point3(int x, int y, int z) {
      this.x = x;
      this.y = y;
      this.z = z;
    }

    @Override
    public boolean equals(Object other) {
      Point3 that = (Point3) other;
      return this.x == that.x && this.y == that.y && this.z == that.z;
    }

    @Override
    public int hashCode() {
      return 1_000_000*x + 1_000*y + z;
    }

    @Override
    public String toString() {
      return "(" + x + "," + y + "," + z + ")";
    }

    int manhattanDistance(Point3 other) {
      return Math.abs(this.x-other.x) + Math.abs(this.y-other.y) + Math.abs(this.z-other.z);
    }

    public int compareTo(Point3 other) {
      int xDiff = this.x - other.x;
      int yDiff = this.y - other.y;
      int zDiff = this.z - other.z;
      int coordDiff = xDiff + yDiff + zDiff;
      return coordDiff != 0 ? coordDiff : xDiff != 0 ? xDiff : yDiff != 0 ? yDiff : zDiff;
    }
  }
}
