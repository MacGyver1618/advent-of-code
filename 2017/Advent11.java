import java.util.*;
import java.util.stream.*;

public class Advent11 extends Advent {

  List<String> instructions = new LinkedList<>();
  int maxdist = 0;

  public Advent11() {
    super(11);
  }


  @Override
  protected void parseInput() {
    String inputString = input.get(0);
    StringTokenizer st = new StringTokenizer(inputString, ",");
    while(st.hasMoreTokens())
      instructions.add(st.nextToken());
  }

  @Override
  protected String part1() {
    int x = 0, y = 0, z = 0;
    int curdist = 0;
    for (String instr : instructions) {
      switch(instr) {
        case "n":
          y++;
          z--;
          break;
        case "ne":
          x++;
          z--;
          break;
        case "se":
          x++;
          y--;
          break;
        case "s":
          y--;
          z++;
          break;
        case "sw":
          x--;
          z++;
          break;
        case "nw":
          x--;
          y++;
          break;
      }
      curdist = distance(x,y,z);
      if (curdist > maxdist)
        maxdist = curdist;
    }

    return "("+x+","+y+","+z+"): " + curdist;
  }

  private int distance (int x, int y, int z) {
    return (Math.abs(x) + Math.abs(y) + Math.abs(z)) / 2;
  }

  @Override
  protected String part2() {
    return "" + maxdist;
  }
}
