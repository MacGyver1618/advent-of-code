import java.util.*;
import java.util.stream.*;

import static java.util.stream.Collectors.toList;

public class Advent04 extends Advent {

  List<Map<String,String>> passports = new ArrayList<>();

  public Advent04() {
    super(4);
  }

  @Override
  protected void parseInput() {
    var current = new HashMap<String, String>();
    for (String line : input) {
      if (line.length() == 0) {
        passports.add(current);
        current = new HashMap<>();
        continue;
      }
      var pairs = line.split(" ");
      for (var pair : pairs) {
        var kvp = pair.split(":");
        current.put(kvp[0], kvp[1]);
      }
    }
    passports.add(current);
  }

  @Override
  protected Object part1() {
    return passports.stream().filter(this::isValid).count();
  }

  private boolean isValid(Map<String, String> passport) {
    return passport.keySet().containsAll(Set.of("byr", "iyr", "eyr", "hgt","hcl","ecl", "pid"));
  }

  private boolean isValid2(Map<String, String> p) {
    try {
      var byr = Integer.parseInt(p.get("byr"));
      var iyr = Integer.parseInt(p.get("iyr"));
      var eyr = Integer.parseInt(p.get("eyr"));
      var hgt = p.get("hgt");
      return byr >= 1920 && byr <= 2002
        && iyr >= 2010 && iyr <= 2020
        && eyr >= 2020 && eyr <= 2030
        && hgtValid(hgt)
        && p.get("hcl").matches("^#[0-9-a-f]{6}$")
        && List.of("amb","blu", "brn", "gry", "grn","hzl","oth").contains(p.get("ecl"))
        && p.get("pid").matches("^\\d{9}$");
    } catch (Exception e) {
      return false;
    }
  }

  private boolean hgtValid(String hgt) {
    if (hgt.contains("cm")) {
      var h = Integer.parseInt(hgt.split("cm")[0]);
      return h >= 150 && h <= 193;
    }
    if (hgt.contains("in")) {
      var h = Integer.parseInt(hgt.split("in")[0]);
      return h >= 59 && h <= 76;
    }
    return false;
  }

  @Override
  protected Object part2() {
    return passports.stream().filter(this::isValid2).count();
  }
}
