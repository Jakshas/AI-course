from Jungle import Jungle
from Jungle import Pos

def dist(p1:Pos,p2:Pos):
    d = p1-p2
    return abs(d.x) + abs(d.y)

def makemove2(j:Jungle):
    best = [-1000000,0]
    for m in j.get_moves():
        j1 = j.copy()
        j1.move(m[0],m[1])
        h = heuristic(j1)
        if j.turn =='bot':
            h=(-1)*h
        if h>best[0]:
            best[0] = h
            best[1] = m
    return best[1]

def heuristic(j:Jungle):
    points = {'r':3, 'c':1, 'd':2, 'w':3, 'j':5, 't':7, 'l':8, 'e':10, 'R':3, 'C':1, 'D':2, 'W':3, 'J':5, 'T':7, 'L':8, 'E':10}
    ret = 0
    for animal in j.top_animals:
        ret += points[animal]*4
    for animal in j.bot_animals:
        ret -= points[animal]*4
    ret -= min((dist(j.animals[a], Pos(3, 8)) for a in j.top_animals), default=0)
    ret += min((dist(j.animals[a], Pos(3, 0)) for a in j.bot_animals), default=0)
    return ret
