import java.util.*;
import java.util.regex.*;
import java.util.stream.*;

public class Advent04 extends Advent {

  private Pattern timePattern = Pattern.compile("\\[\\d{4}-\\d{2}-\\d{2} (\\d{2}):(\\d{2})\\]");
  private Pattern guardPattern = Pattern.compile("Guard #(\\d+) begins shift");

  private int[] sleeptimes = new int[1440];
  private Map<Integer, Integer> guardSleepTimes = new TreeMap<>();
  private Map<Integer, Object> guardSleepSlots = new TreeMap<>();

  public Advent04() {
    super(4);
  }

  @Override
  protected void parseInput() {
    Collections.sort(input);
    int currentGuard = 0;
    int sleepStart = 0;
    int sleepEnd = 0;
    for (String line : input) {
      Matcher guardMatcher = guardPattern.matcher(line);
      Matcher timeMatcher = timePattern.matcher(line);
      timeMatcher.find();
      int hour = Integer.parseInt(timeMatcher.group(1));
      int minute = Integer.parseInt(timeMatcher.group(2));
      if (guardMatcher.find()) {
        currentGuard = Integer.parseInt(guardMatcher.group(1));
      } else if (line.endsWith("falls asleep")) {
        sleepStart = hour*60 + minute;
      } else if (line.endsWith("wakes up")) {
        sleepEnd = hour*60 + minute;
        populateSleepTimes(currentGuard, sleepStart, sleepEnd);
      }
    }
  }
  
  private void populateSleepTimes(int guard, int start, int end) {
    int total = end - start;
    guardSleepTimes.put(guard, guardSleepTimes.getOrDefault(guard, 0) + total);
    int[] sleepSlots = (int[]) guardSleepSlots.getOrDefault(guard, new int[1440]);
    for (int i = start; i < end; i++) {
      sleeptimes[i]++;
      sleepSlots[i]++;
    }
    guardSleepSlots.put(guard, sleepSlots);
  }

  @Override
  protected String part1() {
    int guard = findSleepiestGuard();
    int sleepMinute = findSleepiestMinute(guard);
    return "" + guard*sleepMinute;
  }

  private int findSleepiestGuard() {
    int maxSleep = 0;
    int sleepiestGuard = 0;
    for (Map.Entry<Integer, Integer> entry : guardSleepTimes.entrySet()) {
      if (entry.getValue() > maxSleep) {
        maxSleep = entry.getValue();
        sleepiestGuard = entry.getKey();
      }
    }
    return sleepiestGuard;
  }

  private int findSleepiestMinute(int guard) {
    int maxSleep = 0;
    int maxMinute = -1;
    int[] sleepSlots = (int[]) guardSleepSlots.get(guard);
    for (int minute = 0; minute < 1440; minute++) {
      if (sleepSlots[minute] > maxSleep) {
        maxSleep = sleepSlots[minute];
        maxMinute = minute;
      }
    }
    return maxMinute;
  }

  @Override
  protected String part2() {
    int guard = -1;
    int maxMinute = -1;
    int maxSleep = -1;
    for (Map.Entry<Integer, Object> entry : guardSleepSlots.entrySet()) {
      int[] sleepSlots = (int[]) entry.getValue();
      for (int minute = 0; minute < 1440; minute++) {
        if (sleepSlots[minute] > maxSleep) {
          maxMinute = minute;
          maxSleep = sleepSlots[minute];
          guard = entry.getKey();
        }
      }
    }
    return "" + guard*maxMinute;
  }
}
