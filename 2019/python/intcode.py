import enum
from collections import deque, defaultdict

from common.advent_lib import read_lines


class AddressMode:

    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2

class ArgType:
    IN=0
    OUT=1

class Opcode:
    ADD,MUL,IN,OUT,JIT,JIF,LT,EQ,RBO,STOP=1,2,3,4,5,6,7,8,9,99

class Status:
    READY,RUNNING,WAITING,FINISHED=0,1,2,3

class IntCodeMachine:
    def __init__(self, program):
        self._program = defaultdict(int, {i:v for i,v in enumerate(program.copy())})
        self._pc = 0
        self._rb = 0
        self._inputs = deque()
        self._outputs = deque()
        self._status = Status.READY

    def stop(self):
        self._status = Status.FINISHED

    def add(self,a,b,c):
        self._program[c]= a + b

    def mul(self,a,b,c):
        self._program[c]= a * b

    def _in(self,a):
        if self._inputs:
            self._program[a]=self._inputs.popleft()
        else:
            self._status = Status.WAITING
            self._pc -= 2

    def out(self,a):
        self._outputs.append(a)

    def jit(self,a,b):
        if a:
            self._pc = b-3

    def jif(self,a,b):
        if not a:
            self._pc = b-3

    def lt(self,a,b,c):
        self._program[c] = 1 if a < b else 0

    def eq(self,a,b,c):
        self._program[c] = 1 if a == b else 0

    def rbo(self, a):
        self._rb+=a

    opcodes = {
        Opcode.ADD: ((0,0,1),add),
        Opcode.MUL: ((0,0,1),mul),
        Opcode.IN: ((1,),_in),
        Opcode.OUT: ((0,),out),
        Opcode.JIT: ((0,0),jit),
        Opcode.JIF: ((0,0),jif),
        Opcode.LT: ((0,0,1),lt),
        Opcode.EQ: ((0,0,1),eq),
        Opcode.RBO: ((0,),rbo),
        Opcode.STOP: ((),stop)
    }

    def resolve_arg(self, arg_type, address_mode, pc_offset):
        val = self._program[self._pc + pc_offset]
        if arg_type == ArgType.OUT:
            if address_mode == AddressMode.RELATIVE:
                val += self._rb
            return val
        elif address_mode == AddressMode.IMMEDIATE:
            return val
        elif address_mode == AddressMode.POSITION:
            return self._program[val]
        elif address_mode == AddressMode.RELATIVE:
            return self._program[val+self._rb]
        raise ValueError("Unsupported address mode")

    def handle_op(self):
        instruction = self._program[self._pc]
        opcode = instruction % 100
        mode_a = (instruction//100) % 10
        mode_b = (instruction//1000) % 10
        mode_c = (instruction//10000) % 10
        argv,fn = IntCodeMachine.opcodes[opcode]
        argc=len(argv)
        args = [self.resolve_arg(argv[i],mode, i + 1) for i, mode in enumerate([mode_a, mode_b, mode_c][:argc])]
        fn(self,*args)
        self._pc += argc + 1

    def run(self):
        self._status = Status.RUNNING
        while self._status == Status.RUNNING:
            self.handle_op()

    def val_at(self, position):
        return self._program[position]

    def set_val(self, position, val):
        self._program[position]=val

    def input(self, *vals):
        for val in vals:
            self._inputs.append(val)

    def inputs_queued(self):
        return len(self._inputs) > 0

    def input_line(self, line):
        self._inputs.extend([ord(c) for c in line])
        self.input(ord("\n"))

    def read(self):
        return self._outputs.popleft()

    def read_n(self, n):
        return [self.read() for _ in range(n)]

    def read_all(self):
        return [self._outputs.popleft() for _ in range(len(self._outputs))]

    def read_string(self):
        return "".join(chr(self._outputs.popleft()) for _ in range(len(self._outputs)))

    def outputs_queued(self):
        return len(self._outputs) > 0

    def finished(self):
        return self._status == Status.FINISHED

    @staticmethod
    def from_day_input(n):
        return IntCodeMachine([*map(int,read_lines(n)[0].split(","))])
