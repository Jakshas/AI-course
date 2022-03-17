import random, queue

class Pair:
    def __init__(self, a, b):
        self.x = a
        self.y = b
    def __eq__(self, other):
        return self.x == other[0] and self.y == other[1]
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
    while len(best)>2 or j<1000:
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
            if len(comandoss) == 2:
                return comandoss, router
        if len(best) > len(comandoss):
            best = comandoss
            route = router.copy()
    return best, route

def comandoongoal(comandos , goals):
    for com in comandos:
        if com not in goals:
            return False
    return True
    
def bfs(board, comandos, goals, route):
    que = queue.Queue()
    routeque = queue.Queue()
    que.put(comandos)
    routeque.put(route)
    visited = set()
    com = que.get()
    route = routeque.get()
    while not comandoongoal(com , goals):
        if not (frozenset(com) in visited):
            for i in range(0,4):
                pomcom = set()
                for c in com:
                    pomcom.add(makmove(c,i,board))
                que.put(pomcom)
                routepom = route.copy()
                routepom.append(i)
                routeque.put(routepom)
        visited.add(frozenset(com))
        com = que.get()
        route = routeque.get()
    return route

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
    odp = bfs(board,comandoss,goals,route)
    while len(odp)>150:
        comandoss, route = firstfaze(board, comandos, goals)
        odp = bfs(board,comandoss,goals,route)
    r = []
    print(len(odp))
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

