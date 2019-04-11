import java.util.*;
import java.io.*;
import java.util.stream.Collectors;

public class SynacorChallenge {

  private static int pc;
  private static int[] memory = new int[32768];
  private static int[] regs = new int[8];
  private static Stack<Integer> stack = new Stack<>();
  private static boolean halt = false;
  private static boolean debug = false;
  private static Deque<Character> buffer = new ArrayDeque<>();

  public static void main(String... args) {
    readProgram("challenge.bin");
    runProgram();
    //parseProgram();
  }

  private static String printRegs() {
    String out = "";
    for (int i = 0; i < regs.length; i++) {
      out += " " + regs[i];
    }
    return out;
  }

  private static void debug(String s) {
    if (debug) System.out.println(s + printRegs());
  }

  private static void readProgram(String s) {
    try {
      FileInputStream stream = new FileInputStream(s);
      int i = 0;
      int word = readWord(stream);
      while (word > -1) {
        memory[i++] = word;
        word = readWord(stream);
      }
    } catch (FileNotFoundException e) {
      e.printStackTrace();
    }
  }

  private static int readWord(FileInputStream stream) {
    try {
      int low = stream.read();
      int high = stream.read();
      return (high << 8) + low;
    } catch (IOException e) {
      return -1;
    }
  }

  private static void runProgram() {
    while (!halt) {
      evaluate(memory[pc]);
    }
  }

  private static void evaluate(int opcode) {
    switch (opcode) {
      case 0:
        halt();
        break;
      case 1:
        set();
        break;
      case 2:
        push();
        break;
      case 3:
        pop();
        break;
      case 4:
        eq();
        break;
      case 5:
        gt();
        break;
      case 6:
        jmp();
        break;
      case 7:
        jt();
        break;
      case 8:
        jf();
        break;
      case 9:
        add();
        break;
      case 10:
        mult();
        break;
      case 11:
        mod();
        break;
      case 12:
        and();
        break;
      case 13:
        or();
        break;
      case 14:
        not();
        break;
      case 15:
        rmem();
        break;
      case 16:
        wmem();
        break;
      case 17:
        call();
        break;
      case 18:
        ret();
        break;
      case 19:
        out();
        break;
      case 20:
        in();
        break;
      case 21:
      default:
        noop();
        break;

    }
  }

  private static void halt() {
    debug((pc) + ": 'halt'");
    halt = true;
  }

  private static void set() {
    int reg = readNextRaw() % 32768;
    int val = readNextRaw();
    debug((pc - 2) + ": 'set " + reg + " " + val + "'");
    regs[reg] = read(val);
    pc++;
  }

  private static void push() {
    int val = readNext();
    debug((pc - 1) + ": 'push " + val + "'");
    debug("Stack size: " + stack.size());
    stack.push(val);
    pc++;
  }

  private static void pop() {
    int val = readNextRaw();
    debug((pc - 1) + ": 'pop " + val + "'");
    debug("Stack size: " + stack.size());
    if (!stack.empty()) {
      write(val, stack.pop());
      pc++;
    } else {
      error("Tried to pop empty stack");
    }
  }

  private static void eq() {
    int target = readNextRaw();
    int b = readNext();
    int c = readNext();
    debug((pc - 3) + ": 'eq " + target + " " + b + " " + c + "'");
    write(target, b == c ? 1 : 0);
    pc++;
  }

  private static void gt() {
    int target = readNextRaw();
    int b = readNext();
    int c = readNext();
    debug((pc - 3) + ": 'gt " + target + " " + b + " " + c + "'");
    write(target, b > c ? 1 : 0);
    pc++;
  }

  private static void jmp() {
    int target = readNext();
    debug((pc - 1) + ": 'jmp " + target + "'");
    pc = target;
  }

  private static void jt() {
    int a = readNextRaw();
    int target = readNextRaw();
    debug((pc - 2) + ": 'jt " + a + " " + target + "'");
    pc = read(a) != 0 ? read(target) : pc + 1;
  }

  private static void jf() {
    int a = readNextRaw();
    int target = readNextRaw();
    debug((pc - 2) + ": 'jf " + a + " " + target + "'");
    pc = read(a) == 0 ? read(target) : pc + 1;
  }

  private static void add() {
    int target = readNextRaw();
    int b = readNext();
    int c = readNext();
    debug((pc - 3) + ": 'add " + target + " " + b + " " + c + "'");
    write(target, (b + c) % 32768);
    pc++;
  }

  private static void mult() {
    int target = readNextRaw();
    int b = readNext();
    int c = readNext();
    debug((pc - 4) + ": 'mult " + target + " " + b + " " + c + "'");
    write(target, (b * c) % 32768);
    pc++;
  }

  private static void mod() {
    int target = readNextRaw();
    int b = readNext();
    int c = readNext();
    debug((pc - 3) + ": 'mod " + target + " " + b + " " + c + "'");
    write(target, (b % c));
    pc++;
  }

  private static void and() {
    int target = readNextRaw();
    int b = readNext();
    int c = readNext();
    debug((pc - 3) + ": 'and " + target + " " + b + " " + c + "'");
    write(target, b & c);
    pc++;
  }

  private static void or() {
    int target = readNextRaw();
    int b = readNext();
    int c = readNext();
    debug((pc - 3) + ": 'or " + target + " " + b + " " + c + "'");
    write(target, b | c);
    pc++;
  }

  private static void not() {
    int target = readNextRaw();
    int b = readNext();
    debug((pc - 2) + ": 'not " + target + " " + b + "'");
    write(target, (~b) & 32767);
    pc++;
  }

  private static void rmem() {
    int target = readNextRaw();
    int address = readNext();
    debug((pc - 2) + ": 'rmem " + target + " " + address + "'");
    write(target, memory[address]);
    pc++;
  }

  private static void wmem() {
    int address = readNext();
    int value = readNext();
    debug((pc - 2) + ": 'wmem " + address + " " + value + "'");
    memory[address] = value;
    pc++;
  }

  private static void call() {
    int jumpTo = readNext();
    int nextInstruction = pc + 1;
    debug((pc - 1) + ": 'call " + jumpTo + "'");
    stack.push(nextInstruction);
    pc = jumpTo;
  }

  private static void ret() {
    debug((pc) + ": 'ret'");
    if (!stack.empty()) {
      pc = stack.pop();
    } else {
      halt();
    }
  }

  private static void out() {
    char c = (char) readNext();
    debug((pc - 1) + ": 'out " + c + "'");
    System.out.print(c);
    pc++;
  }

  private static void in() {
    int target = readNextRaw();
    debug((pc - 1) + ": 'in " + target + "'");
    write(target, nextInputChar());
    pc++;
  }

  private static int nextInputChar() {
    if (buffer.isEmpty()) {
      Scanner scanner = new Scanner(System.in);
      String line = scanner.nextLine();
      if (!line.startsWith("/")) {
        for (char a : line.toCharArray()) {
          buffer.add(a);
        }
        buffer.add('\n');
      } else {
        doShellCommand(line);
        return '\n';
      }
    }
    return buffer.removeFirst();
  }

  private static void doShellCommand(String line) {
    StringTokenizer st = new StringTokenizer(line);
    String op = st.nextToken();
    switch (op) {
      case "/dumpmem":
        dumpMemory();
        break;
      case "/pc":
        System.out.println(pc);
        break;
      case "/regs":
        System.out.println(printRegs());
        break;
      case "/mem":
        int address = st.hasMoreTokens() ? Integer.parseInt(st.nextToken()) : pc;
        System.out.println(memory[address]);
        break;
      case "/stack":
        System.out.println(printStack());
    }
  }

  private static String printStack() {
    List<Integer> list = new ArrayList<>(stack);
    return list.stream().map(e -> e.toString()).collect(Collectors.joining(" "));
  }

  private static void dumpMemory() {
    try {
      FileOutputStream out = new FileOutputStream("memdump.hex");
      for (int i = 0; i < memory.length; i++) {
        out.write(memory[i] & 255); // low byte
        out.write((memory[i] & 65280) >> 8); // high byte
      }
    } catch (IOException e) {
      e.printStackTrace();
    }
  }


  private static void noop() {
    debug((pc) + ": 'noop'");
    pc++;
  }

  private static void error(String msg) {
    System.out.println("System encountered error \"" + msg + "\" at " + pc + ": " + opname(memory[pc]));
    halt();
  }

  private static int readNext() {
    return read(memory[++pc]);
  }

  private static int readNextRaw() {
    return memory[++pc];
  }

  private static int read(int target) {
    if (target < 32768) {
      return target;
    } else if (target < 32776) {
      return regs[target - 32768];
    } else {
      error("Read target " + target + " out of bounds");
      return -1;
    }
  }

  private static void write(int target, int value) {
    if (target < 32768) {
      error("Tried to write to literal " + target);
    } else if (target < 32776) {
      regs[target - 32768] = value;
    } else {
      error("Write target " + target + " out of bounds");
    }
  }

  private static void parseProgram() {
    while (pc < memory.length) {
      System.out.println(pc + ": " + opname(memory[pc]));
      pc++;
    }
  }

  private static String opname(int opcode) {
    switch (opcode) {
      case 0:
        return "halt" + printRegs();
      case 1:
        return "set" + next(2) + printRegs();
      case 2:
        return "push" + next(1) + printRegs();
      case 3:
        return "pop" + next(1) + printRegs();
      case 4:
        return "eq" + next(3) + printRegs();
      case 5:
        return "gt" + next(3) + printRegs();
      case 6:
        return "jmp" + next(1) + printRegs();
      case 7:
        return "jt" + next(2) + printRegs();
      case 8:
        return "jf" + next(2) + printRegs();
      case 9:
        return "add" + next(3) + printRegs();
      case 10:
        return "mult" + next(3) + printRegs();
      case 11:
        return "mod" + next(3) + printRegs();
      case 12:
        return "and" + next(3) + printRegs();
      case 13:
        return "or" + next(3) + printRegs();
      case 14:
        return "not" + next(2) + printRegs();
      case 15:
        return "rmem" + next(2) + printRegs();
      case 16:
        return "wmem" + next(2) + printRegs();
      case 17:
        return "call" + next(1) + printRegs();
      case 18:
        return "ret" + printRegs();
      case 19:
        return "out" + next(1) + printRegs();
      case 20:
        return "in" + next(1) + printRegs();
      case 21:
        return "noop" + printRegs();
      default:
        return Integer.toString(opcode);
    }
  }

  private static String next(int n) {
    String out = "";
    for (int i = 0; i < n; i++) {
      out += " " + readNextRaw();
    }
    return out;
  }
}