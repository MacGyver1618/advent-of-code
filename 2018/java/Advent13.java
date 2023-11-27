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
      case '<':
        carts.add(new Cart(x, y, Direction.LEFT));
        return '-';
      case '>':
        carts.add(new Cart(x, y, Direction.RIGHT));
        return '-';
      case '^':
        carts.add(new Cart(x, y, Direction.UP));
        return '|';
      case 'v':
        carts.add(new Cart(x, y, Direction.DOWN));
        return '|';
      default:
        return c;
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
    Direction direction;
    Turn nextTurn;
    boolean dead = false;

    Cart(int x, int y, Direction direction) {
      this.position = new Point(x,y);
      this.direction = direction;
      this.nextTurn = Turn.LEFT;
    }

    void advance() {
      if (dead) return;
      switch (direction) {
        case UP:
          position.y--;
          break;
        case DOWN:
          position.y++;
          break;
        case LEFT:
          position.x--;
          break;
        case RIGHT:
          position.x++;
          break;
      }
    }

    void turn(char c) {
      if (dead) return;
      switch (c) {
        case '+':
          this.direction = direction.turn(nextTurn);
          this.nextTurn = nextTurn.nextTurn;
          break;
        case '/':
        case '\\':
          switch (direction) {
            case UP:
              this.direction = c == '/' ? Direction.RIGHT : Direction.LEFT;
              break;
            case DOWN:
              this.direction = c == '/' ? Direction.LEFT : Direction.RIGHT;
              break;
            case LEFT:
              this.direction = c == '/' ? Direction.DOWN : Direction.UP;
              break;
            case RIGHT:
              this.direction = c == '/' ? Direction.UP : Direction.DOWN;
              break;
          }
          break;
      }
    }

    @Override
    public String toString() {
      switch (direction) {
        case UP: return "^";
        case DOWN: return "v";
        case LEFT: return "<";
        case RIGHT: return ">";
      }
      return "O";
    }
  }

  enum Direction {
    UP,
    DOWN,
    LEFT,
    RIGHT;

    Direction leftTurn;
    Direction rightTurn;

    static {
      UP.leftTurn = LEFT;
      UP.rightTurn = RIGHT;
      DOWN.leftTurn = RIGHT;
      DOWN.rightTurn = LEFT;
      LEFT.leftTurn = DOWN;
      LEFT.rightTurn = UP;
      RIGHT.leftTurn = UP;
      RIGHT.rightTurn = DOWN;
    }

    Direction turn(Turn turn) {
      return turn == Turn.LEFT ? leftTurn : turn == Turn.RIGHT ? rightTurn : this;
    }
  }

  enum Turn {
    LEFT,
    STRAIGHT,
    RIGHT;

    Turn nextTurn;

    static {
      LEFT.nextTurn = STRAIGHT;
      STRAIGHT.nextTurn = RIGHT;
      RIGHT.nextTurn = LEFT;
    }
  }
}
