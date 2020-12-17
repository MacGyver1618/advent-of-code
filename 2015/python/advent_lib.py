import functools as func
import itertools as it

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

def iterate(f, seed):
    value = seed
    while True:
        yield value
        value = f(value)