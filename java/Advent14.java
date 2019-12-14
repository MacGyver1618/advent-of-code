import java.util.*;
import java.util.regex.*;
import java.util.stream.*;

public class Advent14 extends Advent {

  List<Rule> rules;
  Map<String, Integer> resources;
  Set<String> resourceNames;
  Map<String, Integer> oreRequirement;

  public Advent14() {
    super(14);
  }

  @Override
  protected void parseInput() {
    rules = new ArrayList<>();
    resources = new TreeMap<>();
    oreRequirement = new TreeMap<>();
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
    }
  }

  @Override
  protected Object part1() {
    resources.put("FUEL", 1);
    while (resources.size() > 1 || !resources.containsKey("ORE")) {
      sopl(resources);
      pause();
      var requiredResources = new TreeSet<>(resources.keySet());
      for (var resource : requiredResources) {
        if ("ORE".equals(resource)) {
          continue;
        }
        var amount = resources.get(resource);
        for (var entry : requirementFor(resource, amount).entrySet()) {
          int currentAmount = resources.getOrDefault(entry.getKey(), 0);
          resources.put(entry.getKey(), currentAmount + entry.getValue());
        }
        resources.remove(resource);
      }
    }
    return resources.get("ORE");
  }

  private Map<String, Integer> requirementFor(String name, int amount) {
    for (Rule rule : rules) {
      if (rule.product.equals(name)) {
        return rule.requirement(name, amount);
      }
    }
    throw new NoSuchElementException(name + " not found in resources");
  }

  static int ceil(int a, int b) {
    return a % b == 0 ? a/b : a/b + 1;
  }

  @Override
  protected Object part2() {
    return null;
  }

  static class Rule {

    Map<String, Integer> reagents;
    String product;
    Integer amount;

    Rule(String[] reagentArray, String productString) {
      reagents = new TreeMap<>();
      for (String reagent : reagentArray) {
        String[] parts = reagent.split(" ");
        Integer howMuch = Integer.parseInt(parts[0]);
        String name = parts[1];
        reagents.put(name, howMuch);
      }
      String[] productParts = productString.split(" ");
      amount = Integer.parseInt(productParts[0]);
      product = productParts[1];
    }

    Map<String,Integer> requirement(String name, int amount) {
      int factor = amount > this.amount ? ceil(amount, this.amount) : 1;
      var result = new TreeMap<>(reagents);
      if (factor > 1) {
        result.replaceAll((k,v) -> v*factor);
      }
      return result;
    }

    boolean sufficientResources(Map<String, Integer> resources) {
      return reagents.entrySet().stream()
        .allMatch((var e) -> resources.getOrDefault(e.getKey(), 0) >= e.getValue());
    }

    Map<String, Integer> react(Map<String, Integer> resources) {
      var result = new TreeMap<>(resources);
      for (var reagent : reagents.entrySet()) {
        int currentAmount = resources.get(reagent);
        result.put(reagent.getKey(), currentAmount - reagent.getValue());
      }
      return result;
    }
  }
}
