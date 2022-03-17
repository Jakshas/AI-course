import chess
import random

class Agent:
    def __init__(self, a, weights, board : chess.Board):
        self.a = a
        self.weights = weights
        self.board : chess.Board = board
        self.won = 0

    def __lt__(self, value):
        return self.won > value.won

    def move(self):
        m = [(float("-inf"), "")]
        for move in self.board.legal_moves:
            h = self.heuristic(move)
            if m[0][0] < h:
                m = [(h, move)]
            if h == float('inf'):
                return "M"
            elif m[0][0] == h:
                m.append((h, move)) 
        r = random.randint(0, len(m) - 1)
        self.board.push(m[r][1])

    def getscore(self, color):
        s = 0
        for a, p in self.board.piece_map().items():
            if p.color == color:
                s += self.weights[p.symbol().upper()]
        return s

    def heuristic(self, move):
        self.board.push(move)
        if self.board.is_checkmate():
            return float('inf')
        self.board.turn = not self.board.turn
        val = self.getscore(self.board.turn)
        val -= self.getscore(not self.board.turn)
        val += self.a * self.board.legal_moves.count()
        self.board.turn = not self.board.turn
        val -= self.a * self.board.legal_moves.count()
        self.board.turn = not self.board.turn
        self.board.pop()
        return val

def winner(board : chess.Board):
    scoreWeights = { "N" : 3, "B" : 3, "R" : 5, "Q" : 9, "K" : 0, "P" : 1 }
    if board.outcome() == None:
        s1 = 0
        s2 = 0
        for a, p in board.piece_map().items():
            if p.color == True:
                s1 += scoreWeights[p.symbol().upper()]
            else:
                s2 += scoreWeights[p.symbol().upper()]
        return "D" if s1 == s2 else s1 > s2
    else:
        return board.outcome().winner

def randomweight():
    a = { }
    for p in ["N", "B", "R", "Q"]:
        a.update({p : random.randint(3, 9)}) 
    a.update({"P" : 1, "K" : 0})
    return a

def game(A1 : Agent, A2: Agent, gameBoard : chess.Board):
    gameBoard.reset()
    while ( not gameBoard.is_game_over() ) and gameBoard.fullmove_number < 100:
        A1.move()
        if gameBoard.is_game_over():
            break
        A2.move()
    w = winner(gameBoard)
    if w != "D":
        if w:
            A1.won += 1
        else:
            A2.won += 1
    gameBoard.reset()
    while ( not gameBoard.is_game_over() ) and gameBoard.fullmove_number < 100:
        A2.move()
        if gameBoard.is_game_over():
            break
        A2.move()
    w = winner(gameBoard)
    if w != "D":
        if w:
            A2.won += 1
        else:
            A1.won += 1

board = chess.Board()
players = [Agent( random.random() * 1, randomweight(), board ) for _ in range(10)]
for i in range(10):
    print(i)
    for j in range(i + 1, 10):
        game(players[i], players[j], board)
players.sort()
for p in players:
    print(p.won)
    print(p.weights)
