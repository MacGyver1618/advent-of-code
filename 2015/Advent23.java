import java.util.*;
import java.util.stream.*;

public class Advent23 extends Advent {


  public Advent23() {
    super(23);
  }

  @Override
  protected void readInput() {

  }

  @Override
  protected void parseInput() {

  }

  @Override
  protected String part1() {
    GameTree tree = new GameTree();
    tree.populate();
    return "" + tree.minManaToWin();
  }

  class GameTree {
    GameTreeNode root = new GameTreeNode(new Scenario());

    void populate() {
      root.populate();
    }

    int depth() {
      return root.depth();
    }

    long minManaToWin() {
      root.allScenarios()
          .stream()
          //.map(e -> e.status)
          //.filter(e -> e.status == Status.PLAYER_WIN)
          .forEach(e -> System.out.println(e.mana_used));
      return 0;
    }
  }

  class GameTreeNode {
    Scenario scenario;
    List<GameTreeNode> children = new LinkedList<>();

    GameTreeNode(Scenario scenario) {
      this.scenario = scenario;
    }

    void populate() {
      for (Spell spell : scenario.availableSpells()) {
        Scenario child = scenario.cast(spell);
        child.takeTurns();
        children.add(new GameTreeNode(child));
      }
      for (GameTreeNode child : children) {
        child.populate();
      }
    }

    Set<Scenario> allScenarios() {
      Set<Scenario> result = new HashSet<>();
      result.add(this.scenario);
      for (GameTreeNode child : children) {
        result.addAll(child.allScenarios());
      }
      return result;
    }

    int depth() {
      if (children.isEmpty())
        return 1;
      int maxDepth = 0;
      for (GameTreeNode child : children) {
        int childDepth = child.depth();
        if (childDepth > maxDepth)
          maxDepth = childDepth;
      }
      return maxDepth + 1;
    }
  }

  enum Spell {
    MAGIC_MISSILE(53),
    DRAIN(73),
    SHIELD(113),
    POISON(173),
    RECHARGE(229),
    WAIT(0);

    int cost;

    Spell(int cost) {
      this.cost = cost;
    }
  }

  enum Status {
    PLAYING,
    PLAYER_WIN,
    BOSS_WIN;
  }

  class Scenario implements Cloneable {
    int player_hp,
        player_mana,
        shield_timer,
        poison_timer,
        recharge_timer,
        mana_used,
        boss_hp,
        boss_dmg;

    Status status;

    Scenario() {
      player_hp = 50;
      player_mana = 500;
      boss_hp = 58;
      boss_dmg = 9;
      shield_timer = 0;
      poison_timer = 0;
      recharge_timer = 0;
      mana_used = 0;
      status = Status.PLAYING;
    }

    Set<Spell> availableSpells() {
      Set<Spell> result = new HashSet<>();
      if (status == Status.PLAYER_WIN || status == Status.BOSS_WIN)
        return result;
      if (player_mana >= 53) result.add(Spell.MAGIC_MISSILE);
      if (player_mana >= 73) result.add(Spell.DRAIN);
      if (player_mana >= 113 && shield_timer < 1) result.add(Spell.SHIELD);
      if (player_mana >= 173 && poison_timer < 1) result.add(Spell.POISON);
      if (player_mana >= 229 && recharge_timer < 1) result.add(Spell.RECHARGE);
      if (result.isEmpty() && recharge_timer > 0)
        result.add(Spell.WAIT);
      return result;
    }

    void takeTurns() {
      // Boss turn effects
      if (shield_timer > 0)
        shield_timer--;
      if (recharge_timer > 0) {
        player_mana += 101;
        recharge_timer--;
      }
      if (poison_timer > 0) {
        boss_hp -= 3;
        poison_timer--;
        if (boss_hp < 1) {
          status = Status.PLAYER_WIN;
          return;
        }
      }

      // Boss attack
      int dmg = boss_dmg;
      if (shield_timer > 0)
        dmg -= 7;
      player_hp -= dmg;
      if (player_hp < 1) {
        status = Status.BOSS_WIN;
        return;
      }

      // Player turn effects
      player_hp--;
      if (shield_timer > 0)
        shield_timer--;
      if (recharge_timer > 0)
        player_mana += 101;
        recharge_timer--;
      if (poison_timer > 0) {
        boss_hp -= 3;
        poison_timer--;
        if (boss_hp < 1) {
          status = Status.PLAYER_WIN;
          return;
        }
      }
      // Yield to cast()
    }

    Scenario cast(Spell spell) {
      Scenario result = null;
      try {
        result = (Scenario) this.clone();
        result.player_mana -= spell.cost;
        result.mana_used += spell.cost;
        switch (spell) {
          case MAGIC_MISSILE:
            result.boss_hp -= 4;
            if (result.boss_hp < 1) {
              result.status = Status.PLAYER_WIN;
              return result;
            }
            break;
          case DRAIN:
            result.boss_hp -= 2;
            result.player_hp += 2;
            if (result.boss_hp < 1) {
              result.status = Status.PLAYER_WIN;
              return result;
            }
            break;
          case SHIELD:
            result.shield_timer = 6;
            break;
          case POISON:
            result.poison_timer = 6;
            break;
          case RECHARGE:
            result.recharge_timer = 5;
            break;
        }
      } catch (CloneNotSupportedException e) {
        sopl("Couldn't clone scenario");
      } finally {
        return result;
      }

    }
  }


}
