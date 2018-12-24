import java.util.*;
import java.util.regex.*;
import java.util.stream.*;

public class Advent24 extends Advent {

  Pattern pattern = Pattern.compile("(\\d+) units each with (\\d+) hit points (\\((immune|weak) to (\\w+(, )?)+(; (immune|weak) to (\\w+(, )?)+)?\\) )?with an attack that does (\\d+) (\\w+) damage at initiative (\\d+)");

  Pattern weaknessPattern = Pattern.compile("weak to ((\\w+(, )?)+)");
  Pattern immunityPattern = Pattern.compile("immune to ((\\w+(, )?)+)");

  List<Group> groups = new ArrayList<>();

  Comparator<Group> groupComparator = Comparator.comparingInt((Group g) -> g.effectivePower())
                                                .thenComparingInt((Group g) -> g.initiative)
                                                .reversed();

  public Advent24() {
    super(24);
  }

  @Override
  protected void readInput() {
    //readExample();
    super.readInput();
  }

  @Override
  protected void parseInput() {
    String faction = null;
    for (String line : input) {
      if (line.endsWith(":")) {
        faction = line.substring(0, line.length() - 1);
      } else if (line.length() == 0) {
        continue;
      } else {
        parseLine(line, faction);
      }
    }
  }

  private void parseLine(String line, String faction) {
    Matcher m = pattern.matcher(line);
    m.find();
    Group group = new Group();
    group.faction = faction;
    group.units = Integer.parseInt(m.group(1));
    group.hp = Integer.parseInt(m.group(2));
    group.damage = Integer.parseInt(m.group(11));
    group.attackType = m.group(12);
    group.initiative = Integer.parseInt(m.group(13));
    String modifiers = m.group(3);
    group.weaknesses = parseWeaknesses(modifiers);
    group.immunities = parseImmunities(modifiers);
    groups.add(group);
  }

  private List<String> parseWeaknesses(String modifiers) {
    List<String> result = new ArrayList<>();
    if (modifiers == null) return result;
    Matcher m = weaknessPattern.matcher(modifiers);
    if (m.find()) {
      result.addAll(Arrays.asList(m.group(1).split(", ")));
    }
    return result;
  }

  private List<String> parseImmunities(String modifiers) {
    List<String> result = new ArrayList<>();
    if (modifiers == null) return result;
    Matcher m = immunityPattern.matcher(modifiers);
    if (m.find()) {
      result.addAll(Arrays.asList(m.group(1).split(", ")));
    }
    return result;
  }

  @Override
  protected String part1() {
    Map<Group, Group> targets;
    while (bothFactionsAlive()) {
      targets = findTargets();
      for (var pair : targets.entrySet()) {
        pair.getKey().attack(pair.getValue());
      }
    }
    return "" + groups.stream()
                      .filter(g -> g.units > 0)
                      .mapToInt(g -> g.units)
                      .sum();
  }

  private boolean bothFactionsAlive() {
    long infection = groups.stream()
                           .filter(g -> g.faction.equals("Infection"))
                           .filter(g -> g.units > 0)
                           .count();
    long immune = groups.stream()
                        .filter(g -> !g.faction.equals("Infection"))
                        .filter(g -> g.units > 0)
                        .count();
    return infection > 0 && immune > 0;
  }

  private Map<Group, Group> findTargets() {
    Map<Group, Group> result = new TreeMap<>(Comparator.comparingInt((Group g) -> g.initiative).reversed());
    List<Group> eligibleGroups = groups.stream()
                                       .filter(g -> g.units > 0)
                                       .sorted(groupComparator)
                                       .collect(Collectors.toList());
    List<Group> eligibleTargets = new ArrayList<>(eligibleGroups);
    while (!eligibleGroups.isEmpty()) {
      Group group = eligibleGroups.get(0);
      eligibleGroups.remove(0);
      Group target = findTarget(group, eligibleTargets);
      if (target != null) {
        result.put(group, target);
        eligibleTargets.remove(target);
      }
    }
    return result;
  }

  private Group findTarget(Group group, List<Group> targets) {
    return targets.stream()
                  .filter(g -> g.units > 0)
                  .filter(g -> !g.faction.equals(group.faction))
                  .sorted(damageComparator(group))
                  .findFirst()
                  .orElse(null);
  }

  private Comparator<Group> damageComparator(Group group) {
    return Comparator.comparingInt((Group g) -> group.damageTo(g))
                     .thenComparingInt((Group g) -> g.units*g.damage)
                     .thenComparingInt((Group g) -> g.initiative)
                     .reversed();
  }

  private int effectivePower(Group group) {
    return groups.stream()
                 .filter(g -> !g.faction.equals(group.faction))
                 .filter(g -> !g.immunities.contains(group.attackType))
                 .mapToInt(g -> (g.weaknesses.contains(group.attackType) ? 2 : 1)*group.units*group.damage)
                 .max()
                 .orElse(0);
  }

  @Override
  protected String part2() {
    return "";
  }

  class Group {
    String faction;
    int units;
    int hp;
    int damage;
    int initiative;
    String attackType;
    List<String> weaknesses;
    List<String> immunities;

    int damageTo(Group other) {
      if (other.immunities.contains(this.attackType)) return 0;
      int factor = other.weaknesses.contains(this.attackType) ? 2 : 1;
      return this.units*this.damage*factor;
    }

    int effectivePower() {
      return this.units*this.damage;
    }

    void attack(Group other) {
      int damage = this.damageTo(other);
      int killed = Math.min(damage / other.hp, other.units);
      other.units -= killed;
    }

    public String toString() {
      StringBuilder sb = new StringBuilder();
      sb.append("faction=").append(faction).append(", ")
        .append("units=").append(units).append(", ")
        .append("hp=").append(hp).append(", ")
        .append("damage=").append(damage).append(", ")
        .append("initiative=").append(initiative).append(", ")
        .append("attackType=").append(attackType).append(", ")
        .append("weaknesses=").append(weaknesses).append(", ")
        .append("immunities=").append(immunities);
      return sb.toString();
    }
  }
}
