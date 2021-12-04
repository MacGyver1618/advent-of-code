import functools as func
import itertools as it
from numpy import array as A

def full_input(day):
    return str(open("../input/%02d.txt" % day).read())

def lines(day):
    return [line.rstrip() for line in open("../input/%02d.txt" % day).readlines()]

def to_nums(string_arr):
    return list(map(int, string_arr))

def intersection(iterable):
    return set(func.reduce(set.intersection, [set(i) for i in iterable]))

def union(iterable):
    return set(func.reduce(set.union, [set(i) for i in iterable]))

def powerset(iterable):
    s = list(iterable)
    return it.chain.from_iterable(it.combinations(s, r) for r in range(len(s)+1))

def product(iterable):
    return func.reduce(lambda a,x: a*x, iterable)

def first(iterable):
    return iterable[0]

def second(iterable):
    return iterable[1]

directions = {
    "N": A([0, -1]),
    "E": A([1, 0]),
    "S": A([0, 1]),
    "W": A([-1, 0]),
    "U": A([0, -1]),
    "R": A([1, 0]),
    "D": A([0, 1]),
    "L": A([-1, 0])
}
O = A([0,0])
R = A([[0, -1],
       [ 1, 0]])
L = R.T

abc = "abcdefghijklmnopqrstuvwxyz"
ABC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"