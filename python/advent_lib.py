def lines(day):
    return [line.rstrip() for line in open("input/%02d.txt" % day).readlines()]

def to_nums(string_arr):
    return list(map(int, string_arr))
