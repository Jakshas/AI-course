from random import randrange
from Jungle import Pos


availible_moves = {}

# 1 is max, 0 is min
class Reversi:
    def __init__(self):
        self.turn, self.other = 1, 0 # 1 starts
        self.width, self.height = 8, 8
        self.dirs = [Pos(1,0), Pos(1,1), Pos(0,1), Pos(-1,1), Pos(-1,0), Pos(-1,-1), Pos(0,-1), Pos(1,-1)]
        self.history = []
        self.history_ends = []
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.board[4][4] = 1
        self.board[3][3] = 1
        self.board[4][3] = 0
        self.board[3][4] = 0
        self.tiles = set(Pos(x,y) for x in range(8) for y in range(8) if self.board[y][x] is None)

    def copy(self):
        cpy = Reversi()
        cpy.turn, cpy.other = self.turn, self.other
        cpy.history = self.history.copy()
        cpy.history_ends = self.history_ends
        cpy.board = [row.copy() for row in self.board]
        cpy.tiles = self.tiles.copy()
        return cpy
        
    def __getitem__(self, pos):
        if 0<=pos[0]<self.width and 0<=pos[1]<self.height:
            return self.board[pos[1]][pos[0]]
        return None

    def __setitem__(self, pos, val):
        self.board[pos[1]][pos[0]] = val

    def beats(self, pos, d):
        pos = pos.copy()
        pos += d
        flipped = False
        while self[pos] == self.other:
            pos += d
            flipped = True
        return flipped and self[pos] == self.turn

    # 
    def get_moves(self):
        global availible_moves
        h = self.__hash__()+self.turn
        if h in availible_moves:
            return availible_moves[h]
        else:
            moves = []
            for pos in self.tiles:
                if any(self.beats(pos, d) for d in self.dirs):
                    moves.append(pos)
            if len(availible_moves) < 10000000:
                availible_moves[h] = moves
            return moves

    # 
    def get_enemy_moves(self):
        global availible_moves
        h = self.__hash__()+self.other
        if h in availible_moves:
            return availible_moves[h]
        else:
            moves = []
            self.turn, self.other = self.other, self.turn
            for pos in self.tiles:
                if any(self.beats(pos, d) for d in self.dirs):
                    moves.append(pos)
            self.turn, self.other = self.other, self.turn
            if len(availible_moves) < 10000000:
                availible_moves[h] = moves
            return moves

    # 
    def get_stable(self, player):
        stable = set()
        right, down, left, up = Pos(1,0), Pos(0,1), Pos(-1,0), Pos(0,-1)
        if self[0,0] == player:
            stable.add(Pos(0,0))
            pos = right.copy()
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
            pos = right.copy()
            while(self[pos]==player):
                stable.add(pos)
                pos += right
            pos = Pos(0,7)+up
            while(self[pos]==player):
                stable.add(pos)
                pos += up
        return stable

    # 
    def simulate(self, history):
        for move in history:
            self.move(move)

    # 
    def move(self, pos): # supply None if no move is possible
        if pos is None:
            self.turn, self.other = self.other, self.turn
            self.history.append(None)
            self.history_ends.append(None)
            return
        self.tiles.remove(pos)
        to_flip = []
        ends = []
        for d in self.dirs:
            npos = pos + d
            counter = 0
            while self[npos] == self.other:
                to_flip.append(npos)
                npos = npos+d
                counter += 1
            if self[npos] != self.turn and counter > 0:
                to_flip = to_flip[:-counter]
                npos = pos+d
            ends.append(npos)
        self.history.append(pos)
        self.history_ends.append(ends)
        for p in to_flip:
            self[p] = self.turn
        self[pos] = self.turn
        self.turn, self.other = self.other, self.turn

    # 
    def undo_move(self):
        pos = self.history.pop()
        ends = self.history_ends.pop()
        self.turn, self.other = self.other, self.turn
        if pos is None:
            return
        self.tiles.add(pos)
        self[pos] = None
        for d, end in zip(self.dirs, ends):
            npos = pos + d
            while npos != end:
                self[npos] = self.other
                npos += d

    # 
    def terminal(self):
        if len(self.history) < 8:
            return False
        if self.history[-1] == self.history[-2] == None:
            return True
        if len(self.tiles) == 0:
            return True
        if sum(1 for move in self.history if move is not None) >= 60: 
            return True
        return False

    # 
    def difference(self):
        return sum(1 if self[x,y]==1 else -1 if self[x,y]==0 else 0 for x in range(8) for y in range(8))

    def winner(self): # assuma game ended
        diff = self.difference()
        return 1 if diff > 0 else 0 if diff < 0 else 0.5

    def draw(self):
        for y in range(self.height):
            for x in range(self.width):
                print('.' if self.board[y][x] == None else self.board[y][x], end='')
            print()
        print()

    # 
    def __hash__(self):
        return hash(''.join('.' if self.board[y][x] is None else str(self.board[y][x]) for x in range(self.width) for y in range(self.height)))

def random_move(board):
    r = board.get_moves()
    if not r:
        return None
    return r[randrange(0,len(r))]

values = [[20, -3, 11, 8, 8, 11, -3, 20],
    	[-3, -7, -4, 1, 1, -4, -7, -3],
    	[11, -4, 2, 2, 2, 2, -4, 11],
    	[8, 1, 2, -3, -3, 2, 1, 8],
    	[8, 1, 2, -3, -3, 2, 1, 8],
    	[11, -4, 2, 2, 2, 2, -4, 11],
    	[-3, -7, -4, 1, 1, -4, -7, -3],
    	[20, -3, 11, 8, 8, 11, -3, 20]]

p = 0.1
m = 0.2 # 0.2
d = 1
s = 100 # 100

def heuristic(board: Reversi):
    positioning , mobility, domination, stability = 0, 0, 0, 0
    if len(board.history) < 20:
        for y in range(8):
            for x in range(8):
                if board[x,y]==1:
                    positioning += values[y][x]
                elif board[x,y]==0:
                    positioning -= values[y][x]

    if len(board.history) < 55:
        mobility = (len(board.get_moves()) - len(board.get_enemy_moves()))*(2*board.turn-1)

    if len(board.history) > 54:
        domination = board.difference()

    if len(board.history) < 54:
        stability = len(board.get_stable(1)) - len(board.get_stable(0))

    return positioning*p + mobility*m + domination*d + stability*s
        

def alphabeta(board, depth, turn, other, alpha=float('-inf'), beta=float('inf'), original=False):
    # turn = board.turn
    # other = board.other
    if board.terminal():
        diff = board.difference()
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
            board.undo_move()
            if value > best:
                best = value
                best_move = mv
            alpha = max(alpha, best)
            if alpha >= beta:
                break
        if original:
            return best, best_move
        return best
    else:
        best = float('inf')
        best_move = None
        for mv in board.get_moves():
            board.move(mv)
            value = alphabeta(board, depth-1, other, turn, alpha, beta)
            board.undo_move()
            if value < best:
                best = value
                best_move = mv
            beta = min(beta, best)
            if alpha >= beta:
                break
        if original:
            return best, best_move
        return best


def alphabeta_move(board, depth=2):
    moves = board.get_moves()
    if len(moves) == 0:
        return None
    # elif len(moves) == 1:
    #     return moves[0]
    value, move = alphabeta(board, depth, turn=board.turn, other=board.other, original=True)
    # assert move is not None
    return move

def tqdm(iterable):
    l = len(iterable)
    for i, e in enumerate(iterable):
        print('{}/{}'.format(i, l))
        yield e

if __name__ == '__main__':

    max_wins = 0
    min_wins = 0
    differences = []
    players = (random_move, alphabeta_move)
    for _ in tqdm(range(100)):
        game = Reversi()
        for move in range(70):
            mv = players[move%2](game)
            game.move(mv)
            if game.terminal():
                break
            # game.draw()
        if game.difference() > 0:
            max_wins += 1
        else:
            min_wins += 1
        differences.append(game.difference())
    print(max_wins, min_wins)