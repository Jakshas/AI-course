from copy import deepcopy

class Pos:
    def __init__(self, a, b=None):
        self.x, self.y = a if b is None else (a, b)
    def __add__(self, other):
        return Pos(self.x+other.x, self.y+other.y)
    def __iadd__(self, other):
        self.x+=other.x
        self.y+=other.y
        return self
    def __sub__(self, other):
        return Pos(self.x-other.x, self.y-other.y)
    def __eq__(self, other):
        return other is not None and self.x == other.x and self.y == other.y
    def copy(self):
        return Pos(self.x, self.y)
    def __hash__(self):
        return hash((self.x, self.y))
    def __getitem__(self, num):
        return self.x if num == 0 else self.y
    def __lt__(self, other):
        return self.x<other.x or (self.x==other.x and self.y < other.y)

class Jungle: 
    def __init__(self, top_animals=None, bot_animals=None, animals=None, animal_board=None, turn=None, last_capture=None):
        self.width = 7
        self.height = 9
        self.directions = [Pos(1,0), Pos(0,1), Pos(-1,0), Pos(0,-1)]
        if turn is None:
            self.turn = 'bot'
            self.other = 'top'
            self.last_capture = 0
        else:
            self.turn = turn
            if turn == 'top':
                self.other = 'bot'
            else: 
                self.other = 'top'
            self.last_capture = last_capture
        self.board = ['..#%#..', 
                      '...#...', 
                      '.......', 
                      '.~~.~~.', 
                      '.~~.~~.', 
                      '.~~.~~.', 
                      '.......', 
                      '...#...', 
                      '..#*#..']
        self.strengths = {'r':1, 'c':2, 'd':3, 'w':4, 'j':5, 't':6, 'l':7, 'e':8,
                          'R':1, 'C':2, 'D':3, 'W':4, 'J':5, 'T':6, 'L':7, 'E':8}
        if top_animals is None:
            self.top_animals = set('LDRJTCEW')
            self.bot_animals = set('ldrjtcew')
            self.animals = {'L':Pos(0,0), 'D':Pos(1,1), 'R':Pos(0,2), 'J':Pos(2,2),'T':Pos(6,0), 'C':Pos(5,1), 'E':Pos(6,2), 'W':Pos(4,2),'l':Pos(6,8), 'd':Pos(5,7), 'r':Pos(6,6), 'j':Pos(4,6),'t':Pos(0,8), 'c':Pos(1,7), 'e':Pos(0,6), 'w':Pos(2,6)}
            self.animal_board = [[',' for _ in range(self.width)] for _ in range(self.height)]
            for animal, pos in self.animals.items():
                self.animal_board[pos.y][pos.x] = animal
        else:
            self.top_animals = top_animals
            self.bot_animals = bot_animals
            self.animals = animals
            self.animal_board = animal_board

    def copy(self):
        return Jungle(self.top_animals.copy(), self.bot_animals.copy(), self.animals.copy(), deepcopy(self.animal_board), self.turn, self.last_capture)

    def can_move(self, predator, direction):
        field = self.board[self.animals[predator].y][self.animals[predator].x]
        newpos = self.animals[predator]+self.directions[direction]
        if not (0<=newpos.x<self.width and 0<=newpos.y<self.height):
            return False
        newfield = self.board[newpos.y][newpos.x]
        prey = self.animal_board[newpos.y][newpos.x]
        if predator in 'tTlL' and newfield == '~': 
            while newfield != '.':
                if prey == 'rR':
                    return False
                newpos += self.directions[direction]
                newfield = self.board[newpos.y][newpos.x]
                prey = self.animal_board[newpos.y][newpos.x]
        prey = self.animal_board[newpos.y][newpos.x]
        if newfield == '.' and prey == ',': 
            return True
        if predator in 'rcdwjtle' and prey in 'rcdwjtle':
            return False
        if predator in 'RCDWJTLE' and prey in 'RCDWJTLE':
            return False
        if newfield == '~' and predator not in 'rRtTlL':
            return False
        if predator in 'rR' and field == '~' and newfield == '.' and prey != ',': 
            return False
        if predator in 'rR' and newfield == '~': 
            return True
        if predator in 'rcdwjtle' and newfield == '*': 
            return False
        if predator in 'RCDWJTLE' and newfield == '%': 
            return False
        if field == '#' and prey != ',': 
            return False
        if newfield == '#': 
            return True
        if predator in 'rcdwjtle' and newfield == '%': 
            return True
        if predator in 'RCDWJTLE' and newfield == '*': 
            return True
        if predator in 'rR' and prey in 'eE': 
            return True
        if predator in 'eE' and prey in 'rR': 
            return False
        if self.strengths[predator] >= self.strengths[prey]: 
            return True
        else:
            return False
            
    def get_moves(self):
        moves = []
        for animal in (self.top_animals if self.turn == 'top' else self.bot_animals):
            for direction in range(4):
                if self.can_move(animal, direction):
                    moves.append((animal, direction))
        return moves

    def move(self, animal, direction):
        pos = self.animals[animal]
        d = self.directions[direction]
        npos = pos + d
        newfield = self.board[npos.y][npos.x]
        if animal in 'tTlL' and newfield == '~':
            while newfield != '.':
                npos += d
                newfield = self.board[npos.y][npos.x]
        prey = self.animal_board[npos.y][npos.x]
        if prey != ',':
            if prey in self.top_animals:
                self.top_animals.remove(prey)
            else:
                self.bot_animals.remove(prey)
            del self.animals[prey]
            self.last_capture = 0
        else:
            self.last_capture += 1
        self.animal_board[pos.y][pos.x] = ','
        self.animal_board[npos.y][npos.x] = animal
        self.animals[animal] = npos
        temp = self.turn
        self.turn = self.other
        self.other = temp

    def draw(self):
        for y in range(self.height):
            print(''.join(self.board[y])+' '+''.join(['.' if self.animal_board[y][x] == '/' else self.animal_board[y][x] for x in range(self.width)]))
        print()

    def winner(self):
        if self.animal_board[0][3] != ',':
            return 'bot'
        if self.animal_board[8][3] != ',':
            return 'top'
        if len(self.top_animals) == 0:
            return 'bot'
        if len(self.bot_animals) == 0:
            return 'top'
        if self.last_capture >= 30:
            top = tuple(sorted(map(lambda x: self.strengths[x], self.top_animals)))
            bot = tuple(sorted(map(lambda x: self.strengths[x], self.bot_animals)))
            if bot > top:
                return 'bot'
            elif top > bot:
                return 'top'
            else:
                return 'top'
        return None

if __name__ == '__main__':
    test = Jungle()
    while True:
        test.draw()
        l=[]
        lk = list('WSEN')
        for t in test.get_moves():
            l.append((t[0],lk[t[1]]))
        print("Możliwe ruchy")
        print(l)
        i = input()
        test.move(i[0], lk.index(i[1]))
        win = test.winner()
        if(win is not None):
            print(f'Winner is {win}')
            break