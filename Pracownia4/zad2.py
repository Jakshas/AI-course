from typing import List
from random import randint, random

import chess
import chess.engine

defaultWeights = { "N" : 3, "B" : 3, "R" : 5, "Q" : 9, "K" : 0, "P" : 1 }

PLAYERS_NUM = 90
FULLMOVES_TERMINATION = 65

engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")

class ChessAgent:

    def __init__(self, α, weights, board : chess.Board ) -> None:
        self.α = α
        self.weights = weights
        self.board : chess.Board = board
        self.gamesWon = 0

    def move():
        pass

    def getPiecesOfColor(self, ifWhite):
        sum = 0
        for _, p in self.board.piece_map().items():
            if p.color == ifWhite:
                sum += self.weights[p.symbol().upper()]
        return sum

    def __getαMovePossibilitiesCount(self):
        return self.α * self.board.legal_moves.count()

    def __calculateHeuristic(self) -> int:        
        h = self.getPiecesOfColor(self.board.turn)
        h += -self.getPiecesOfColor(not self.board.turn)
        h += self.__getαMovePossibilitiesCount()
        self.board.turn = not self.board.turn
        h -= self.__getαMovePossibilitiesCount()
        self.board.turn = not self.board.turn
        return h

    def __calculateHeuristicWrapper(self, mv):
        self.board.push(mv)
        if self.board.is_checkmate():
            return 10000000

        self.board.turn = not self.board.turn
        h = self.__calculateHeuristic()
        self.board.pop()
        return h

    def move(self):
        max = [(-100000, "")]
        for mv in self.board.legal_moves:
            h = self.__calculateHeuristicWrapper(mv)
            if max[0][0] < h:
                max = [(h, mv)]
            if h == 10000000:
                return "M"
            elif max[0][0] == h:
                max.append( (h, mv) ) 
        self.board.push( max[randint(0, len(max) - 1)][1] )

def genRandomWeights():
    a = { p : randint(3, 9) for p in ["N", "B", "R", "Q"] }
    a.update({"P" : 1, "K" : 0})
    return a

def getWinner(board):
    score : chess.engine.Score = engine.analyse(board, chess.engine.Limit(time=0.3) )["score"].white()
    if score.is_mate():
        return score.mate() > 0
    return "D" if score.score() == 0 else score.score() > 0

def playGame(pA : ChessAgent, pB : ChessAgent, gameBoard):
    gameBoard.reset()

    while ( not gameBoard.is_game_over() ) and gameBoard.fullmove_number < FULLMOVES_TERMINATION:
        pA.move()
        if gameBoard.is_game_over():
            break
        pB.move()

    if gameBoard.outcome() == None:
        res = getWinner(gameBoard)
        if res == False:
            pB.gamesWon += 1
        elif res != 'D':
            pA.gamesWon += 1
        
    else:
        if gameBoard.outcome().winner == True:
            pA.gamesWon += 1
        elif gameBoard.outcome().winner != None:
            pB.gamesWon += 1
    
    gameBoard.reset()
    while ( not gameBoard.is_game_over() ) and gameBoard.fullmove_number < FULLMOVES_TERMINATION:
        pB.move()
        if gameBoard.is_game_over():
            break
        pB.move()

    if gameBoard.outcome() == None:
        res = getWinner(gameBoard)
        if res == True:
            pB.gamesWon += 1
        elif res != 'D':
            pA.gamesWon += 1

    else:
        if gameBoard.outcome().winner == False:
            pA.gamesWon += 1
        elif gameBoard.outcome().winner != None:
            pB.gamesWon += 1

def genRandomPlayer(board) -> ChessAgent:
    return ChessAgent( random() * 1, genRandomWeights(), board )

def genRandomPlayers(board) -> List[ChessAgent]:
    return [ genRandomPlayer(board) for _ in range(PLAYERS_NUM) ]

def writeAgentsToFile(tab : List[ChessAgent]):
    with open('zad2agents.txt', 'a') as out:
        for agent in tab:
            out.write(f"α: {agent.α}, weights: {agent.weights}, won: {agent.gamesWon} \n" )

def performSimulation():
    board = chess.Board()
    players : List[ChessAgent] = genRandomPlayers(board)
    for i in range(PLAYERS_NUM):
        print(i)
        for j in range(i + 1, PLAYERS_NUM):
            playGame( players[i], players[j], board )
    players.sort(key=lambda x : x.gamesWon, reverse=True)

    writeAgentsToFile(players)

performSimulation()
engine.quit()