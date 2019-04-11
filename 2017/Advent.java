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

  protected void readInput() {
    String fileName = (dayNumber < 10 ? "0" : "") + dayNumber + ".txt";
    try {
      BufferedReader reader = new BufferedReader(new FileReader(fileName));
      input = reader.lines().collect(Collectors.toList());
    } catch (FileNotFoundException e) {
      sopl("Could not read file ", fileName);
    }
  }

  protected static void sopl(Object... args) {
    Arrays.stream(args).forEach(System.out::print);
    sopl();
  }

  protected static void pause() {
    new Scanner(System.in).nextLine();
  }

  protected static void sopl() {
    System.out.println();
  }

  protected static void sop(Object... args) {
    Arrays.stream(args).forEach(System.out::print);
  }

  protected void run() {
    sopl("Day ", dayNumber, ":");
    readInput();
    parseInput();
    sopl("  Part 1 answer: ", part1());
    sopl("  Part 2 answer: ", part2());
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

  public static void main(String... args) {
    if (args.length == 0)
      args = IntStream.range(1,26).mapToObj(String::valueOf).toArray(String[]::new);
    for (String arg : args) {
      runAdvent(arg);
    }
  }
}
