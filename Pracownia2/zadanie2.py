import queue

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

def boxongoal(box , goals):
    for com in box:
        if com not in goals:
            return False
    return True

def bfs(board, sob, box, goals):
    route = []
    que = queue.Queue()
    routeque = queue.Queue()
    que.put((sob, box))
    routeque.put(route)
    visited = set()
    com = que.get()
    route = routeque.get()
    while not boxongoal(com[1] , goals):
        if not (com in visited):
            for i in range(0,4):
                pomcom = makmove(com[0], i, board, com[1])
                que.put(pomcom)
                routepom = route.copy()
                routepom.append(i)
                routeque.put(routepom)
        visited.add(com)
        com = que.get()
        route = routeque.get()
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
    odp = bfs(board,sokoban,frozenset(box),goals)
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
    
