import random, heapq

class Pair:
    def __init__(self, a, b):
        self.x = a
        self.y = b
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __getitem__(self, num):
        return [self.x, self.y][num]
    def __repr__(self):
        return f"({self.x}, {self.y})"
    def copy(self):
        return Pair(self.x, self.y)
    def __hash__(self):
        return hash((self.x, self.y))

def makmove(pos , move, board):
    x=pos.x
    y=pos.y
    if move == 0 and board[y][x+1] != '#':
        x=x+1
    elif move == 1 and board[y][x-1] != '#':
        x=x-1
    elif move == 2 and board[y+1][x] != '#':
        y=y+1
    elif move == 3 and board[y-1][x] != '#':
        y=y-1
    return Pair(x,y)

def back(r):
    if r == 0:
        return 1
    elif r == 1:
        return 0
    elif r == 2:
        return 3
    elif r == 3:
        return 2

def firstfaze(board , comandos , goals):
    route = []
    best = comandos
    j = 0
    while len(best)>2 or j<10000:
        j = j + 1
        router = []
        comandoss = comandos
        last = -1
        for i in range(150-(len(board))-(len(board[0]))):
            r = random.randint(0,3)
            while r == back(last):
                r = random.randint(0,3)
            last = r
            router.append(r)
            s = set()
            for instance in comandoss:
                s.add(makmove(instance, r , board))
            comandoss = s
            if len(comandoss) == 3:
                return comandoss, router
        if len(best) > len(comandoss):
            best = comandoss
            route = router.copy()
    return frozenset(best), route

def dist(com , goals):
    min = 100000
    for g in goals:
        p = abs(com.x - g.x) + abs(com.x - g.x)
        if p < min:
            min = p
    return min

def comandoongoal(comandos , goals):
    for com in comandos:
        if com not in goals:
            return False
    return True

def astar(board, comandos, goals, route):
    visited = set()
    heap = []
    visited.add(comandos)
    heapq.heappush(heap, heurystic(comandos, goals, route))
    pom = heapq.heappop(heap)
    com = pom[1]
    route = pom[2]
    while not comandoongoal(com , goals):
        for i in range(0,4):
            compom = set()
            for c in com:
                compom.add(makmove(c,i,board))
            if not (frozenset(compom) in visited):
                router = route.copy()
                router.append(i)
                visited.add(frozenset(compom))
                heapq.heappush(heap, heurystic(compom, goals, router))
        pom = heapq.heappop(heap)
        com = pom[1]
        route = pom[2]
    return route

def heurystic(comandos, goals, route):
    max = 0
    for c in comandos:
        p = dist(c, goals)
        if p > max:
            max = p
    return (max + len(route), comandos, route) 

with open("zad_input.txt", "r") as in_f:
    board = []
    for line in in_f:
        board.append(list(line[:-1]))
    goals = []
    comandos = []
    height = len(board)
    width = len(board[0])
    for y in range(height):
        for x in range(width):
            if board[y][x] == 'S':
                board[y][x] = ' '
                comandos.append(Pair(x,y))
            elif board[y][x] == 'B':
                board[y][x] = ' '
                comandos.append(Pair(x,y))
                goals.append(Pair(x,y))
            elif board[y][x] == 'G':
                board[y][x] = ' '
                goals.append(Pair(x,y))
    comandos = frozenset(comandos)
    goals = goals
    comandoss, route = firstfaze(board, comandos, goals)
    comandos = frozenset(comandoss)
    odp = astar(board, comandos, goals,route)
    print(len(odp))
    r = []
    for c in odp:
        if c == 0:
            r.append('R')
        elif c == 1:
            r.append('L')
        elif c == 2:
            r.append('D')
        elif c == 3:
            r.append('U')
        with open("zad_output.txt", "w") as out_f:
            out_f.write( ''.join(r) )