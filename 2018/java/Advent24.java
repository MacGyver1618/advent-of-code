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

  int boost = 0;

  public Advent24() {
    super(24);
  }

  @Override
  protected void parseInput() {
    groups.clear();
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
    int baseDamage = Integer.parseInt(m.group(11));
    int damage = faction.equals("Immune System") ? baseDamage + boost : baseDamage;
    group.damage = damage;
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
    playGame();
    return "" + winnersAlive();
  }

  private void playGame() {
    Map<Group, Group> targets;
    while (bothFactionsAlive()) {
      targets = findTargets();
      if (targets.isEmpty()) {
        return;
      }
      for (var pair : targets.entrySet()) {
        pair.getKey().attack(pair.getValue());
      }
    }
  }

  private boolean bothFactionsAlive() {
    return infectionCount() > 0 && immuneCount() > 0;
  }

  private long infectionCount() {
    return groups.stream()
                 .filter(g -> g.faction.equals("Infection"))
                 .filter(Group::alive)
                 .count();
  }

  private long immuneCount() {
    return groups.stream()
                 .filter(g -> !g.faction.equals("Infection"))
                 .filter(Group::alive)
                 .count();
  }

  private Map<Group, Group> findTargets() {
    Map<Group, Group> result = new TreeMap<>(Comparator.comparingInt((Group g) -> g.initiative).reversed());
    List<Group> eligibleGroups = groups.stream()
                                       .filter(Group::alive)
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
                  .filter(Group::alive)
                  .filter(g -> !g.faction.equals(group.faction))
                  .filter(g -> group.damageTo(g) > 0)
                  .sorted(damageComparator(group))
                  .findFirst()
                  .orElse(null);
  }

  private Comparator<Group> damageComparator(Group group) {
    return Comparator.comparingInt((Group g) -> group.damageTo(g))
                     .thenComparingInt((Group g) -> g.effectivePower())
                     .thenComparingInt((Group g) -> g.initiative)
                     .reversed();
  }

  private long winnersAlive() {
    return groups.stream()
    .filter(Group::alive)
    .mapToInt(g -> g.units)
    .sum();
  }

  @Override
  protected String part2() {
    while (!winner().equals("Immune System")) {
      ++boost;
      parseInput();
      playGame();
    }
    return "" + winnersAlive();
  }

  private String winner() {
    List<String> factionsAlive = groups.stream()
                                       .filter(Group::alive)
                                       .map(g -> g.faction)
                                       .distinct()
                                       .collect(Collectors.toList());
    return factionsAlive.size() > 1 ? "Deadlock" : factionsAlive.get(0);
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

    boolean alive() {
      return units > 0;
    }

    int damageTo(Group other) {
      if (other.immunities.contains(this.attackType)) return 0;
      int factor = other.weaknesses.contains(this.attackType) ? 2 : 1;
      return this.units*this.damage*factor;
    }

    int effectivePower() {
      return this.units*this.damage;
    }

    void attack(Group other) {
      if (!this.alive()) return;
      int damage = this.damageTo(other);
      int killed = Math.min(damage / other.hp, other.units);
      if (debug) sopl("Killed ", killed);
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
