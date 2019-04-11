import java.util.*;
import java.util.regex.*;
import java.util.stream.*;

public class Advent08 extends Advent {

  private Map<String, Integer> regs = new HashMap<>();
  private Pattern p = Pattern.compile("([a-z]+) (inc|dec) (-?\\d+) if ([a-z]+) (>|<|!=|==|<=|>=) (-?\\d+)");
  private int max = 0;

  public Advent08() {
    super(8);
  }

  @Override
  protected void parseInput() {

  }

  @Override
  protected String part1() {
    input.stream().forEach(this::interpret);
    return "" + regs.values()
                    .stream()
                    .mapToInt(e -> e.intValue())
                    .max()
                    .orElseThrow(NullPointerException::new);
  }

  private void interpret(String line) {
    Matcher m = p.matcher(line);
    m.find();
    String target = m.group(1);
    String op = m.group(2);
    int increment = Integer.parseInt(m.group(3));
    String source = m.group(4);
    String pred = m.group(5);
    int border = Integer.parseInt(m.group(6));

    if (eval(source, pred, border))
      increment(target, op, increment);
  }

  private boolean eval(String source, String pred, int border) {
    int val = getReg(source);
    switch (pred) {
      case ">":
        return val > border;
      case "<":
        return val < border;
      case ">=":
        return val >= border;
      case "<=":
        return val <= border;
      case "==":
        return val == border;
      case "!=":
        return val != border;
      default:
        throw new IllegalArgumentException("don't understand predicate " + pred);
    }
  }

  private void increment(String target, String op, int increment) {
    int val = getReg(target);
    switch (op) {
      case "inc":
        regs.put(target, val + increment);
        break;
      case "dec":
        regs.put(target, val - increment);
        break;
      default:
        throw new IllegalArgumentException("don't understand operation " + op);
    }
  }

  private int getReg(String name) {
    if (!regs.containsKey(name))
      regs.put(name, 0);
    int val = regs.get(name);
    if (val > max) {
      max = val;
    }
    return val;
  }

  @Override
  protected String part2() {
    return "" + max;
  }
}
