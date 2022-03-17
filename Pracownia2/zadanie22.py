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
    def __lt__(self, other):
        return self.x < other.x

def makmove(pos , move, board, box):
    x=pos.x
    y=pos.y
    pombox = set(box.copy())
    if move == 0 and board[y][x+1] != 'W':
        if Pair(x + 1,y) not in pombox:
            x=x+1
        elif board[y][x+2] != 'W' and Pair(x+2,y) not in pombox:
            pombox.remove(Pair(x + 1,y))
            pombox.add(Pair(x + 2,y))
            x=x+1
    elif move == 1 and board[y][x-1] != 'W':
        if Pair(x - 1,y) not in pombox:
            x=x-1
        elif board[y][x-2] != 'W' and Pair(x-2,y) not in pombox:
            pombox.remove(Pair(x - 1,y))
            pombox.add(Pair(x - 2,y))
            x=x-1
    elif move == 2 and board[y+1][x] != 'W':
        if Pair(x ,y + 1) not in pombox:
            y=y+1
        elif board[y + 2][x] != 'W' and Pair(x,y+2) not in pombox:
            pombox.remove(Pair(x,y + 1))
            pombox.add(Pair(x ,y + 2))
            y=y+1
    elif move == 3 and board[y-1][x] != 'W':
        if Pair(x ,y - 1) not in pombox:
            y=y-1
        elif board[y - 2][x] != 'W' and Pair(x,y-2) not in pombox:
            pombox.remove(Pair(x,y - 1))
            pombox.add(Pair(x ,y - 2))
            y=y-1
    return (Pair(x,y), frozenset(pombox))

def dist(box , goals):
    min = 100000
    for g in goals:
        p = abs(box.x - g.x) + abs(box.x - g.x)
        if p < min:
            min = p
    return min

def heurystic(sob, box, goals, route):
    s = 0
    for c in box:
        s = s + dist(c, goals)
    return (s + len(route), (sob, box, route)) 

def boxongoal(box , goals):
    for com in box:
        if com not in goals:
            return False
    return True

def astar(board, sob, box, goals):
    route = []
    visited = set()
    heap = []
    heapq.heappush(heap, heurystic(sob, box, goals, route))
    pom = heapq.heappop(heap)
    com = pom[1]
    route = com[2]
    com = (com[0], com[1])
    visited.add(frozenset(com))
    while not boxongoal(com[1] , goals):
        for i in range(0,4):
            pomcom = makmove(com[0], i, board, com[1])
            if not (frozenset(pomcom) in visited):
                router = route.copy()
                router.append(i)
                visited.add(frozenset(pomcom))
                heapq.heappush(heap, heurystic(pomcom[0],pomcom[1], goals, router))
        pom = heapq.heappop(heap)
        com = pom[1]
        route = com[2]
        com = (com[0], com[1])
    return route

with open("zad_input.txt", "r") as in_f:
    board = []
    goals = []
    box = set()
    for line in in_f:
        board.append(list(line[:-1]))
    height = len(board)
    width = len(board[0])
    for x in range(width):
        for y in range(height):
            if board[y][x] == 'G':
                board[y][x] = '.'
                goals.append(Pair(x,y))
            elif board[y][x] == 'K':
                board[y][x] = '.'
                sokoban = Pair(x,y)
            elif board[y][x] == '+':
                board[y][x] = '.'
                goals.append(Pair(x,y))
                sokoban = Pair(x,y)
            elif board[y][x] == '*':
                board[y][x] = '.'
                box.add(Pair(x,y))
                goals.append(Pair(x,y))
            elif board[y][x] == 'B':
                board[y][x] = '.'
                box.add(Pair(x,y))
    odp = astar(board,sokoban,frozenset(box),goals)
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
    
