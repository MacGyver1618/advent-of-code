import java.util.*;
import java.util.regex.*;
import java.util.stream.*;

public class Advent20 extends Advent {

  List<Particle> particles = new LinkedList<>();
  Pattern pattern = Pattern.compile("p=<(-?\\d+),(-?\\d+),(-?\\d+)>, v=<(-?\\d+),(-?\\d+),(-?\\d+)>, a=<(-?\\d+),(-?\\d+),(-?\\d+)>");

  public Advent20() {
    super(20);
  }

  @Override
  protected void parseInput() {
    for (int i = 0; i < input.size(); i++) {
      particles.add(parseParticle(i, input.get(i)));
    }
  }

  private Particle parseParticle(int number, String props) {
    Matcher m = pattern.matcher(props);
    m.find();
    Particle particle = new Particle();
    particle.number = number;
    particle.px = number(1, m);
    particle.py = number(2, m);
    particle.pz = number(3, m);
    particle.vx = number(4, m);
    particle.vy = number(5, m);
    particle.vz = number(6, m);
    particle.ax = number(7, m);
    particle.ay = number(8, m);
    particle.az = number(9, m);
    return particle;
  }

  private int number(int group, Matcher matcher) {
    return Integer.parseInt(matcher.group(group));
  }

  @Override
  protected String part1() {
    int result = particles.stream()
                          .sorted(Comparator.comparing(e -> Math.abs(e.ax) + Math.abs(e.ay) + Math.abs(e.az)))
                          .mapToInt(e -> e.number)
                          .findFirst()
                          .orElse(-1);
    return "" + result;
  }

  @Override
  protected String part2() {
    int previousSize, currentSize = 0;
    int sameSize = 0;
    while (sameSize < 1_000) {
      particles.stream().forEach(p -> p.tick());
      previousSize = particles.size();
      filterCollisions();
      currentSize = particles.size();
      if (previousSize == currentSize)
        sameSize++;
      else
        sameSize = 0;
    }
    return "" + currentSize;
  }

  private void filterCollisions() {
    List<Particle> result = new LinkedList<>();
    for (Particle particle : particles) {
      long collisions = particles.stream()
                                 .filter(e -> e.distance(particle) == 0)
                                 .count();
      //sopl(collisions, " collisions for ", particle);
      if (collisions == 1)
        result.add(particle);
    }
    particles = result;
  }

  class Particle {
    int number;
    int px, py, pz;
    int vx, vy, vz;
    int ax, ay, az;

    @Override
    public String toString() {
      return "Particle " + number +
             ": p=(" + px + "," + py + "," + pz +
             "), v=(" + vx + "," + vy + "," + vz +
             "), a=(" + ax + "," + ay + "," + az + ")";
    }

    void tick() {
      vx += ax;
      vy += ay;
      vz += az;
      px += vx;
      py += vy;
      pz += vz;
    }

    int distance(Particle other) {
      return Math.abs(px - other.px) + Math.abs(py - other.py) + Math.abs(pz - other.pz);
    }
  }
}
