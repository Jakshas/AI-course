from Jungle import Jungle
import random 
from Jungle3 import makemove2
from JungleMonte import makemove3
import time

def makemoves(j:Jungle):
    getm = j.get_moves()
    bestt = [-1,0]
    bestb = [-1,0]
    N = int(20000/len(getm))
    for m in getm:
        newj = j.copy()
        newj.move(m[0],m[1])
        h = heuristic(newj, N)
        if(h[0]>bestt[0]):
            bestt[0]=h[0]
            bestt[1]=m
        if(h[1]>bestb[0]):
            bestb[0]=h[1]
            bestb[1]=m
    if j.turn == 'top':
        return bestt[1]
    else:
        return bestb[1]
    

def heuristic(j:Jungle, N):
    wt = 0
    wb = 0
    j1 = j.copy()
    for i in range(0,N):
        nm = j1.get_moves()
        r = random.randint(0,len(nm)-1)
        j1.move(nm[r][0],nm[r][1])
        w = j1.winner()
        if(w != None):
            if(w == 'top'):
                wt = wt + 1
            else:
                wb = wb + 1
            j1 = j.copy()
    return (wt,wb)

def makemove1(j:Jungle):
    return makemoves(j)

def test():
    w1 = 0
    w2 = 0
    for i in range(0,1):
        jungle = Jungle()
        while(True):
            # jungle.draw()
            if jungle.turn == 'top':
                # start = time.time()
                move = makemove3(jungle)
                # end = time.time()
                # print(end - start)
            else:
                move = makemove1(jungle)
            jungle.move(move[0],move[1])
            if jungle.winner() != None:
                if jungle.winner() == 'top':
                    w1 += 1
                else:
                    w2 += 1
                break
    return w1 ,w2

print(test())