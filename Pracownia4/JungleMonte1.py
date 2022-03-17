from Jungle import Jungle
import math
import random 

def makemove3(j:Jungle):
    ver = [[1,1,0,0,j]]
    for i in range(100):
        curr = selection(ver)
        tab, wins, alls = expansion(ver, curr)
        ver.extend(tab)
        backup(ver, wins, alls, curr)
    tab = []
    for v in ver:
        if v[2] == 0:
           tab.append(v)
    best = 1
    for i in range(1,len(tab)):
        if tab[i][0]/tab[i][1] >= tab[best][0]/tab[best][1]:
            best = i
    moves = j.get_moves()
    return moves[best-1]

def selection(ver):
    points = []
    if len(ver) == 1:
        return 0
    points.append((ver[0][0]/ver[0][1]))
    for i in range(1,len(ver)):
        if(ver[i][3] == 0):
            val = (ver[i][0]/ver[i][1])+ math.sqrt(2)*math.sqrt(math.log(ver[ver[i][2]][1])/ver[i][1])
            points.append(val)
        else:
            points.append(0)
    best = 0
    for i in range(len(points)):
        if ver[i][3] == 0 and points[i] > points[best]:
            best = i
    return best

def expansion(ver,curr):
    nextver = ver[curr][4].get_moves()
    tab = []
    alls = 0
    wins = 0
    for n in nextver:
        cp = ver[curr][4].copy()
        cp.move(n[0],n[1])
        wol = simulation(ver,curr,n)
        if wol:
            tab.append([1,1,curr,0,cp])
            wins += 1
        else:
            tab.append([0,1,curr,0,cp])
        alls += 1
    ver[curr][3] = 1
    return tab, wins, alls

def simulation(ver,curr,n):
    cp = ver[curr][4].copy()
    cp.move(n[0],n[1])
    while cp.winner() == None:
        nextcp = cp.get_moves()
        r = random.randint(0,len(nextcp)-1)
        cp.move(nextcp[r][0],nextcp[r][1])
    return cp.winner() == ver[0][4].turn


def backup(ver,wins, alls, curr):
    ver[curr][0] += wins
    ver[curr][1] += alls
    while ver[curr][2] != curr:
        curr = ver[curr][2]
        ver[curr][0] += wins
        ver[curr][1] += alls