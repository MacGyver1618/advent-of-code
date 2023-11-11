import java.util.*;
import java.util.regex.*;
import java.util.stream.*;

public class Advent14 extends Advent {

  List<Rule> rules;
  Map<String, Long> resourceRequirements;
  Map<String, Long> resourceYields;
  Set<String> resourceNames;

  public Advent14() {
    super(14);
  }

  @Override
  protected void parseInput() {
    rules = new ArrayList<>();
    resourceRequirements = new TreeMap<>();
    resourceYields = new TreeMap<>();
    resourceNames = new TreeSet<>();
    for (String line : input) {
      String[] sides = line.split(" => ");
      String[] reagents = sides[0].split(", ");
      String product = sides[1];
      rules.add(new Rule(reagents, product));
    }
    for (Rule rule : rules) {
      resourceNames.addAll(rule.reagents.keySet());
      resourceNames.add(rule.product);
      for (Rule upstream : rules) {
        if (upstream.reagents.containsKey(rule.product)) {
          rule.inputs.add(upstream);
        }
      }
    }
  }

  @Override
  protected Object part1() {
    resourceRequirements.put("FUEL", 1L);
    evaluate(ruleToProduce("FUEL"));
    while (!rules.stream().allMatch(r -> r.evaluated)) {
      for (Rule rule : rules) {
        if (!rule.evaluated) {
          evaluate(rule);
        }
      }
    }
    return resourceRequirements.get("ORE");
  }

  private void evaluate(Rule rule) {
    if (rule.inputs.stream().allMatch(r -> r.evaluated)) {
      long required = resourceRequirements.get(rule.product);
      for (var entry : rule.requirement(required).entrySet()) {
        long currentReq = resourceRequirements.getOrDefault(entry.getKey(), 0L);
        resourceRequirements.put(entry.getKey(), currentReq + entry.getValue());
      }
      rule.evaluated = true;
    }
  }

  private boolean onlyOreRequired() {
    return resourceRequirements.entrySet().stream()
      .filter((var e) -> e.getValue() > 0)
      .allMatch((var e) -> e.getKey().equals("ORE"));
  }

  private void updateRequirement(String name, long amount) {
    long available = resourceYields.getOrDefault(name, 0L);
    long currentReq = resourceRequirements.getOrDefault(name, 0L);
    sopl("We need ", amount, " of ", name, " and have ", available, " available");
    sopl("Previous requirement is ", currentReq, " of ", name);
    if (available < amount) {
      long additionalReq = amount - available;
      sopl("We need an extra ", additionalReq, " of ", name);
      resourceRequirements.put(name, additionalReq + currentReq);
    } else {
      resourceYields.put(name, available - amount);
    }
  }

  private Rule ruleToProduce(String name) {
    if (name.equals("ORE")) {
      return new Rule(new String[] { "1 ORE" }, "1 ORE");
    }
    for (Rule rule : rules) {
      if (rule.product.equals(name)) {
        return rule;
      }
    }
    throw new NoSuchElementException(name + " not found in resources");
  }

  static long ceil(long a, long b) {
    return a % b == 0 ? a/b : a/b + 1;
  }

  @Override
  protected Object part2() {
    long limit = 1_000_000_000_000L;
    long min = 8_000_000L;
    long max = 9_000_000L;
    long mid;
    while (true) {
      mid = (min+max)/2;
      long oreThis = oreForFuel(mid);
      long oreNext = oreForFuel(mid+1);
      if (oreThis == limit || (oreThis < limit && oreNext > limit)) {
          return mid;
      }
      if (oreThis < limit) {
        min = mid;
      } else if (oreThis > limit) {
        max = mid;
      }
    }
  }

  private long oreForFuel(long fuel) {
    parseInput();
    resourceRequirements.put("FUEL", fuel);
    evaluate(ruleToProduce("FUEL"));
    while (!rules.stream().allMatch(r -> r.evaluated)) {
      for (Rule rule : rules) {
        if (!rule.evaluated) {
          evaluate(rule);
        }
      }
    }
    return resourceRequirements.get("ORE");
  }

  static class Rule {

    Map<String, Long> reagents;
    String product;
    Long amount;
    boolean evaluated = false;
    Set<Rule> inputs = new HashSet<>();

    Rule(String[] reagentArray, String productString) {
      reagents = new TreeMap<>();
      for (String reagent : reagentArray) {
        String[] parts = reagent.split(" ");
        Long howMuch = Long.parseLong(parts[0]);
        String name = parts[1];
        reagents.put(name, howMuch);
      }
      String[] productParts = productString.split(" ");
      amount = Long.parseLong(productParts[0]);
      product = productParts[1];
    }

    long invocationsNeeded(long amount) {
      return amount > this.amount ? ceil(amount, this.amount) : 1;
    }

    Map<String,Long> requirement(long amount) {
      var result = new TreeMap<>(reagents);
      result.replaceAll((k,v) -> v*invocationsNeeded(amount));
      return result;
    }

    boolean sufficientResources(Map<String, Long> resources) {
      return reagents.entrySet().stream()
        .allMatch((var e) -> resources.getOrDefault(e.getKey(), 0L) >= e.getValue());
    }

    Map<String, Long> react(Map<String, Long> resources) {
      var result = new TreeMap<>(resources);
      for (var reagent : reagents.entrySet()) {
        long currentAmount = resources.get(reagent);
        result.put(reagent.getKey(), currentAmount - reagent.getValue());
      }
      return result;
    }

    @Override
    public String toString() {
      return reagents + " => " + amount + " " + product;
    }
  }
}
