import java.util.*;
import java.util.regex.*;
import java.util.stream.*;

public class Advent12 extends Advent {

  Pattern pattern = Pattern.compile("<x=(-?\\d+), y=(-?\\d+), z=(-?\\d+)>");

  int[][] moons;
  int[][] initial;

  long xperiod = -1;
  long yperiod = -1;
  long zperiod = -1;

  long xmin = Integer.MAX_VALUE;
  long ymin = Integer.MAX_VALUE;
  long zmin = Integer.MAX_VALUE;
  long xmax = Integer.MIN_VALUE;
  long ymax = Integer.MIN_VALUE;
  long zmax = Integer.MIN_VALUE;

  long[][] limits;

  public Advent12() {
    super(12);
  }

  @Override
  protected void parseInput() {
    moons = new int[input.size()][6];
    for (int i = 0; i < input.size(); i++) {
      String line = input.get(i);
      Matcher m = pattern.matcher(line);
      m.find();
      int[] moon = new int[6];
      moon[0] = Integer.parseInt(m.group(1));
      moon[1] = Integer.parseInt(m.group(2));
      moon[2] = Integer.parseInt(m.group(3));
      moons[i] = moon;
    }
    initial = deepCopy();
  }

  @Override
  protected Object part1() {
    for (int i = 0; i < 1000; i++) {
      applyGravity();
      applyVelocity();
    }
    return totalEnergy();
  }

  private void applyGravity() {
    for (int i = 0; i < moons.length; i++) {
      int[] moon = moons[i];
      for (int j = 0; j < moons.length; j++) {
        if (j == i) continue;
        int[] other = moons[j];
        for (int k = 0; k < 3; k++) {
          moon[k+3] += sign(other[k]-moon[k]);
        }
      }
    }
  }

  private void applyVelocity() {
    for (int i = 0; i < moons.length; i++) {
      int[] moon = moons[i];
      for (int k = 0; k < 3; k++) {
        moon[k] += moon[k+3];
      }
    }
  }

  private int totalEnergy() {
    int energy = 0;
    for (int i = 0; i < moons.length; i++) {
      int[] moon = moons[i];
      int potential = 0;
      potential += Math.abs(moon[0]);
      potential += Math.abs(moon[1]);
      potential += Math.abs(moon[2]);
      int kinetic = 0;
      kinetic += Math.abs(moon[3]);
      kinetic += Math.abs(moon[4]);
      kinetic += Math.abs(moon[5]);
      energy += kinetic*potential;
    }
    return energy;
  }

  private int sign(int n) {
    return n == 0 ? 0 : n < 0 ? -1 : 1;
  }

  @Override
  protected Object part2() {
    long cycles = 0;
    parseInput();
    while (xperiod == -1 || yperiod == -1 || zperiod == -1) {
      applyGravity();
      applyVelocity();
      cycles++;
      checkPeriods(cycles);
      checkBounds();
    }
    limits = new long[][] {
      new long[] {xmin, xmax},
      new long[] {ymin, ymax},
      new long[] {zmin, zmax},
    };
    long scaleFactor = 1;
    int fps = 20;
    long cycle = 0;
    while (cycle >= 0) {
      applyGravity();
      applyVelocity();
      if (cycle % scaleFactor == 0) {
        drawPlanets(2,1);
        try {
          Thread.sleep(1000 / fps);
        } catch (Exception e) {}
      }
      cycle++;
    }
    return lcm(lcm(xperiod, yperiod), zperiod);
    //return lcm(yperiod, zperiod);
  }

  private void drawPlanets(int xdim, int ydim) {
    StringBuffer screen = new StringBuffer();
    long xblock = (limits[xdim][1]-limits[xdim][0])/165;
    long yblock = (limits[ydim][1]-limits[ydim][0])/46;
    for (int y = 0; y < 46; y++) {
      for (int x = 0; x < 165; x++) {
        long xmn = limits[xdim][0] + x*xblock;
        long xmx = limits[xdim][0] + (x+1)*xblock;
        long ymn = limits[ydim][0] + y*yblock;
        long ymx = limits[ydim][0] + (y+1)*yblock;
        int moonInBlock = -1;
        for (int i = 0; i < moons.length; i++) {
          int[] moon = moons[i];
          if (moon[xdim] >= xmn && moon[xdim] < xmx
           && moon[ydim] >= ymn && moon[ydim] < ymx) {
            moonInBlock = i;
          }
        }
        if (moonInBlock != -1) {
          screen.append(moonInBlock);
        } else {
          screen.append(' ');
        }
      }
      screen.append('\n');
    }
    sopl(screen.toString());
  }

  private long lcm(long x, long y) {
    return x*y/gcd(x,y);
  }

  private long gcd(long x, long y) {
    if (y == 0) {
        return x;
    }
    return gcd(y, x % y);
  }

  private void checkPeriods(long cycles) {
    boolean xrepeat = true;
    boolean yrepeat = true;
    boolean zrepeat = true;
    for (int i = 0; i < moons.length; i++) {
      xrepeat &= moons[i][0] == initial[i][0] && moons[i][3] == initial[i][3];
      yrepeat &= moons[i][1] == initial[i][1] && moons[i][4] == initial[i][4];
      zrepeat &= moons[i][2] == initial[i][2] && moons[i][5] == initial[i][5];
    }
    if (xrepeat && xperiod == -1) xperiod = cycles;
    if (yrepeat && yperiod == -1) yperiod = cycles;
    if (zrepeat && zperiod == -1) zperiod = cycles;
  }

  private void checkBounds() {
    for (int i = 0; i < moons.length; i++) {
      if (moons[i][0] < xmin) xmin = moons[i][0];
      if (moons[i][0] > xmax) xmax = moons[i][0];
      if (moons[i][1] < ymin) ymin = moons[i][1];
      if (moons[i][1] > ymax) ymax = moons[i][1];
      if (moons[i][2] < zmin) zmin = moons[i][2];
      if (moons[i][2] > zmax) zmax = moons[i][2];
    }
  }

  private int[][] deepCopy() {
    int[][] copy = new int[4][6];
    for (int i = 0; i < moons.length; i++) {
      copy[i] = Arrays.copyOf(moons[i], moons[i].length);
    }
    return copy;
  }
}
