import java.util.*;
import java.util.stream.*;

public class Advent13 extends Advent {

  private char[][] grid;
  private int xMax;
  private int yMax;
  private List<Cart> carts = new LinkedList<>();
  private Comparator<Cart> cartComparator =
    Comparator.comparing((Cart c) -> c.position.y)
              .thenComparing((Cart c) -> c.position.x);

  public Advent13() {
    super(13);
  }

  @Override
  protected void parseInput() {
    yMax = input.size();
    xMax = input.stream()
                .mapToInt(String::length)
                .max()
                .orElseThrow(IllegalStateException::new);
    grid = new char[xMax][yMax];
    carts = new LinkedList<>();
    for (int y = 0; y < yMax; y++) {
      for (int x = 0; x < xMax; x++) {
        grid[x][y] = parseFrom(x,y);
      }
    }
  }

  private char parseFrom(int x, int y) {
    if (input.get(y).length() <= x) return ' ';
    char c = input.get(y).charAt(x);
    switch(c) {
      case '<': carts.add(new Cart(x, y, -1,  0)); return '-';
      case '>': carts.add(new Cart(x, y,  1,  0)); return '-';
      case '^': carts.add(new Cart(x, y,  0, -1)); return '|';
      case 'v': carts.add(new Cart(x, y,  0,  1)); return '|';
      default: return c;
    }
  }

  @Override
  protected String part1() {
    while(!collisions()) {
      for (Cart cart : orderedCarts()) {
        cart.advance();
        cart.turn(grid[cart.position.x][cart.position.y]);
        if (collisions()) {
          return findCollision() + "";
        }
      }
    }
    return "No collisions found";
  }

  private List<Cart> orderedCarts() {
    return carts.stream()
                .sorted(cartComparator)
                .collect(Collectors.toList());
  }

  private boolean collisions() {
    for (Cart cart : carts) {
      if (cart.dead) continue;
      for (Cart other : carts) {
        if (other.dead) continue;
        if (cart != other && cart.position.equals(other.position)) {
          return true;
        }
      }
    }
    return false;
  }

  private Point findCollision() {
    for (Cart cart : carts) {
      for (Cart other : carts) {
        if (cart != other && cart.position.equals(other.position)) {
          return cart.position;
        }
      }
    }
    throw new IllegalStateException();
  }

  @Override
  protected String part2() {
    parseInput();
    while(cartsRemaining() > 1) {
      for (Cart cart : orderedCarts()) {
        cart.advance();
        cart.turn(grid[cart.position.x][cart.position.y]);
        if (collisions()) {
          removeColliding(cart.position);
        }
      }
    }
    return "" + lastRemaining();
  }

  private long cartsRemaining() {
    return carts.stream().filter(c -> !c.dead).count();
  }

  private void removeColliding(Point p) {
    for (Cart cart : carts) {
      if (cart.position.equals(p)) {
        cart.dead = true;
      }
    }
  }

  private Point lastRemaining() {
    return carts.stream()
                .filter(c -> !c.dead)
                .map(c -> c.position)
                .findFirst()
                .orElseThrow(IllegalStateException::new);
  }

  class Cart {
    Point position;
    Point velocity;
    boolean dead = false;
    char nextTurn = 'L';

    Cart(int x, int y, int xv, int yv) {
      this.position = new Point(x, y);
      this.velocity = new Point(xv, yv);
    }

    void advance() {
      if (dead) return;
      this.position.x += this.velocity.x;
      this.position.y += this.velocity.y;
    }

    void turn(char c) {
      if (dead) return;
      switch (c) {
        case '+':
          this.velocity = nextVelocity(nextTurn);
          this.nextTurn = nextTurn(nextTurn);
          break;
        case '/':
        case '\\':
          this.velocity = nextVelocity(c);
          break;
      }
    }

    private Point nextVelocity(char c) {
      int x = this.velocity.x;
      int y = this.velocity.y;
      switch (c) {
        case '/':  return new Point(-y,-x);
        case '\\': return new Point( y, x);
        case 'R':  return new Point(-y, x);
        case 'L':  return new Point( y,-x);
        default:   return this.velocity;
      }
    }

    private char nextTurn(char c) {
      return c == 'L' ? 'S' : c == 'S' ? 'R' : 'L';
    }

    @Override
    public String toString() {
      if (velocity.x > 0) return position + ">";
      if (velocity.x < 0) return position + "<";
      if (velocity.y > 0) return position + "v";
      if (velocity.y < 0) return position + "^";
      throw new IllegalStateException();
    }
  }
}
