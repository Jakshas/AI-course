from Jungle import Pos
import random 
import time

class Reversi:
    def __init__(self):
        self.turn= 1
        self.other = 0
        self.dirs = [Pos(1,0), Pos(1,1), Pos(0,1), Pos(-1,1), Pos(-1,0), Pos(-1,-1), Pos(0,-1), Pos(1,-1)]
        self.history = []
        self.hending = []
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.board[4][4] = 1
        self.board[3][3] = 1
        self.board[4][3] = 0
        self.board[3][4] = 0
        self.fields = set(Pos(x,y) for x in range(8) for y in range(8) if self.board[y][x] is None)

    def __getitem__(self, pos):
        if 0 <= pos[0] < 8 and 0 <= pos[1] < 8:
            return self.board[pos[1]][pos[0]]
        return None

    def __setitem__(self, pos, val):
        self.board[pos[1]][pos[0]] = val

    def __hash__(self):
        return hash(''.join('.' if self.board[y][x] is None else str(self.board[y][x]) for x in range(8) for y in range(8)))

    def copy(self):
        c = Reversi()
        c.turn = self.turn
        c.other = self.other
        c.history = self.history.copy()
        c.hending = self.hending.copy()
        c.board = [row.copy() for row in self.board]
        c.fields = self.fields.copy()
        return c

    def beat(self, pos, d):
        pos = pos.copy()
        pos += d
        flipped = False
        while self[pos] == self.other:
            pos += d
            flipped = True
        return flipped and self[pos] == self.turn

    def get_moves(self):
        moves = []
        for pos in self.fields:
            if any(self.beat(pos, d) for d in self.dirs):
                moves.append(pos)
        return moves

    def move(self, pos):
        if pos is None:
            self.turn, self.other = self.other, self.turn
            self.history.append(None)
            self.hending.append(None)
            return
        self.fields.remove(pos)
        beated = []
        ends = []
        for d in self.dirs:
            npos = pos + d
            counter = 0
            while self[npos] == self.other:
                beated.append(npos)
                npos = npos+d
                counter += 1
            if self[npos] != self.turn and counter > 0:
                beated = beated[:-counter]
                npos = pos+d
            ends.append(npos)
        self.history.append(pos)
        self.hending.append(ends)
        for p in beated:
            self[p] = self.turn
        self[pos] = self.turn
        self.turn, self.other = self.other, self.turn

    def score(self):
        s = 0
        for x in range(8):
            for y in range(8):
                if self[x,y] == 1:
                    s += 1
                else:
                    if self[x,y] == 0:
                        s -= 1
        return s

    def winner(self): 
        diff = self.score()
        return 1 if diff > 0 else 0 

    def reverse_move(self):
        pos = self.history.pop()
        ends = self.hending.pop()
        self.turn, self.other = self.other, self.turn
        if pos is None:
            return
        self.fields.add(pos)
        self[pos] = None
        for d, end in zip(self.dirs, ends):
            npos = pos + d
            while npos != end:
                self[npos] = self.other
                npos += d

    def ifend(self):
        if len(self.history) < 8:
            return False
        if self.history[-1] == self.history[-2] == None:
            return True
        if len(self.fields) == 0:
            return True
        if sum(1 for move in self.history if move is not None) >= 60: 
            return True
        return False

    def pewniaczki(self, player):
        stable = set()
        right, down, left, up = Pos(1,0), Pos(0,1), Pos(-1,0), Pos(0,-1)
        if self[0,0] == player:
            stable.add(Pos(0,0))
            pos = Pos(1,0)
            while(self[pos]==player):
                stable.add(pos)
                pos += right
            pos = down.copy()
            while(self[pos]==player):
                stable.add(pos)
                pos += down
        if self[7,0] == player:
            stable.add(Pos(7,0))
            pos = Pos(7,0)+left
            while(self[pos]==player):
                stable.add(pos)
                pos += left
            pos = Pos(7,0)+down
            while(self[pos]==player):
                stable.add(pos)
                pos += down
        if self[7,7] == player:
            stable.add(Pos(7,7))
            pos = Pos(7,7)+left
            while(self[pos]==player):
                stable.add(pos)
                pos += left
            pos = Pos(7,7)+up
            while(self[pos]==player):
                stable.add(pos)
                pos += up
        if self[0,7] == player:
            stable.add(Pos(0,7))
            pos = Pos(1,0)
            while(self[pos]==player):
                stable.add(pos)
                pos += right
            pos = Pos(0,7)+up
            while(self[pos]==player):
                stable.add(pos)
                pos += up
        for i in range(1,6):
            for j in range(1,6):
                pos = Pos(i,j)
                if self[pos] == player and self.checkpewniaczki(stable, pos):
                    stable.add(pos)
        return stable

    def checkpewniaczki(self,stable,pos):
        var = 0
        for d in self.dirs:
            temp = pos.copy()
            temp += d
            if temp in stable:
                var += 1
        return var > 3

def move1(rev:Reversi):
    moves = rev.get_moves()
    if len(moves) == 0:
        return None
    r = random.randint(0,len(moves)-1)
    return moves[r]

def draw(rev:Reversi):
    for i in range(0,8):
        for j in range(0,8):
            if rev.board[i][j] == None:
                print(".",end="")
            if rev.board[i][j] == 0:
                print("#",end="")
            if rev.board[i][j] == 1:
                print("o",end="")
        print()
    print()

values = [[20, -6, 11, 8, 8, 11, -2, 20],
    	[-6, -6, -4, 1, 1, -4, -6, -2],
    	[11, -4, 2, 2, 2, 2, -4, 11],
    	[8, 1, 2, -3, -3, 2, 1, 8],
    	[8, 1, 2, -3, -3, 2, 1, 8],
    	[11, -4, 2, 2, 2, 2, -4, 11],
    	[-2, -6, -4, 1, 1, -4, -6, -6],
    	[20, -2, 11, 8, 8, 11, -6, 20]]

def heuristic(board: Reversi):
    positioning , mobility, domination, stability = 0, 0, 0, 0
    if len(board.history) < 20:
        for y in range(8):
            for x in range(8):
                if board[x,y]==1:
                    positioning += values[y][x]
                elif board[x,y]==0:
                    positioning -= values[y][x]
    if len(board.history) < 50:
        mobility = (len(board.get_moves()))*(2*board.turn-1)
    if len(board.history) > 49:
        domination = board.score()
    if len(board.history) < 50:
        stability = len(board.pewniaczki(1)) - len(board.pewniaczki(0))
    return positioning + mobility + domination + stability*100

def alphabeta(board, depth, turn, other, alpha=float('-inf'), beta=float('inf'), original=False):
    if board.ifend():
        diff = board.score()
        if diff > 0:
            return -10000000
        elif diff < 0:
            return 10000000
        else:
            return 0
    if depth == 0:
        return heuristic(board)
    if turn == 1:
        best = float('-inf')
        best_move = None
        for mv in board.get_moves():
            board.move(mv)        
            value = alphabeta(board, depth-1, other, turn, alpha, beta)
            board.reverse_move()
            if value > best:
                best = value
                best_move = mv
            alpha = max(alpha, best)
            if alpha >= beta:
                break
            if best >= beta:
                if original: 
                    return best, best_move
                return best
        if original:
            return best_move
        return best
    else:
        best = float('inf')
        best_move = None
        for mv in board.get_moves():
            board.move(mv)
            value = alphabeta(board, depth-1, other, turn, alpha, beta)
            board.reverse_move()
            if value < best:
                best = value
                best_move = mv
            beta = min(beta, best)
            if alpha >= beta:
                break
            if best <= alpha:
                if original: 
                    return best, best_move
                return best
        if original:
            return best_move
        return best

def alphabeta_move(board):
    depth = 2
    moves = board.get_moves()
    if len(moves) == 0:
        return None
    move = alphabeta(board, depth, turn=board.turn, other=board.other, original=True)
    return move

def test():
    w1 = 0
    w2 = 0
    start = time.time()
    for i in range(100):
        print(i)
        end = [0,0]
        rev = Reversi()
        t = i % 2
        while(True):
            if rev.turn == t:
                move = move1(rev)
            else:
                move = alphabeta_move(rev)
            if move == None:
                end[rev.other] = 1
            rev.move(move)
            if end[0] == 1 and end[1] == 1 :
                if rev.winner() == t:
                    w1 += 1
                else:
                    w2 += 1
                break
    end = time.time()
    print(end - start)
    return w1,w2

print(test())

