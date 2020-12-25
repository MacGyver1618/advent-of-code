from advent_lib import *
from collections import deque

player1 = deque(to_nums(lines(22)[1:26]))
player2 = deque(to_nums(lines(22)[28:]))

while player1 and player2:
    p1 = player1.popleft()
    p2 = player2.popleft()
    if p2 > p1:
        player2 = player2 + deque([p2,p1])
    elif p1 > p2:
        player1 = player1 + deque([p1,p2])

def score(deck):
    tot = 0
    for i,card in enumerate(reversed(deck)):
        tot += (i+1)*card
    return tot

print("Part 1:", score(player1) if player1 else score(player2))



player1 = deque(to_nums(lines(22)[1:26]))
player2 = deque(to_nums(lines(22)[28:]))

def play_game(deck1, deck2):
    history = set()
    while deck1 and deck2:
        state = (tuple(deck1), tuple(deck2))
        if state in history:
            return deck1,deque()
        else:
            history.add(state)
        c1 = deck1.popleft()
        c2 = deck2.popleft()
        if c1 <= len(deck1) and c2 <= len(deck2):
            sg1,sg2 = play_game(deque(list(deck1)[:c1]),deque(list(deck2)[:c2]))
            if sg1:
                deck1 += deque([c1,c2])
            else:
                deck2 += deque([c2,c1])
        else:
            if c2 > c1:
                deck2 += deque([c2,c1])
            elif c1 > c2:
                deck1 += deque([c1,c2])
    return deck1,deck2

deck1, deck2 = play_game(player1,player2)

part2 = score(deck1) if deck1 else score(deck2)
print("Part 2:", part2)
