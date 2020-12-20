import numpy as np
import random


class table():
    colours = np.array(['red', 'blue', 'yellow', 'black'])
    numbers = np.arange(1, 14, dtype=int)
    stones = []    # this list contains all the stones currently NOT in players' hands
    players = []
    blocks = []
    grid = [[None for j in range(28)] for i in range(6)]   #i:j, i:row, j:column, is 6 rows by 28 columns
    def __init__(self, *player_names):
        for c in self.colours:
            for num in self.numbers:
                stone(colour=c, number=num)
                stone(colour=c, number=num)
                # print(c, num)
        #self.stones.append(stone(j=True))
        #self.stones.append(stone(j=True))
        for name in player_names:
            player(name=name)
        #print(self.players)
        # distribute stones randomly into players' inventories:
        rand_order = np.array(random.sample(range(len(self.stones)), len(self.players) * 14), dtype=int)
        print(rand_order)
        for c, p in enumerate(self.players):
            for i in range(c * 14, (c + 1) * 14):
                self.stones[rand_order[i]].owner = p.name
                p.inventory.append(self.stones[rand_order[i]])
        self.stones = [s for c, s in enumerate(self.stones) if c not in rand_order]


    def draw_stone(self, p):
        pass
        # take random from un-distributed stones
        # s.owner = p
        # return s


    def set_stone(self, index):
        pass


    def take_stone(self, index):
        pass


    def build_block(self, indices):
        pass

    
            
class stone(table):
    '''Class to define stones, their behaviour etc.
    '''
    width = 50
    height = 150
    def __init__(self, colour=None, number=None, j=False):
        '''Initialize stones from file.
        '''
        
        if j:
            self.joker = True
            self.num = None
            self.c = None
        else:
            self.joker = False
            self.num = number
            self.c = colour
            if self.num == 13:
                self.n_h = 1
            else:
                self.n_h = self.num + 1
            
            if self.num == 1:
                self.n_l = 13
            else:
                self.n_l = self.num -1
    
        self.owner = 'table'
        super(stone, self).stones.append(self)
        
class player(table):
    def __init__(self, name=None):
        self.inventory = []
        self.name = name
        super(player, self).players.append(self)
        print(self.name)
    
    def set_stone(self):
        pass

class block(table):
    def __init__(self, stones):
        self.stones = stones
        super(block, self).blocks.append(self)
        self.valid = self.check_rules()
        

    def check_rules(self):
        self.colours = np.array([s.c for s in self.stones])
        self.numbers = np.array([s.num for s in self.stones])
        self.same_colours = self._same_colours()
        self.diff_colours = self._diff_colours()
        self.same_numbers = self._same_numbers()
        self.cons_numbers = self._cons_numbers()
        self.length = len(self.stones)
        if self.same_colours and self.cons_numbers and self.length >= 3:
            self.valid = True
        elif self.diff_colours and self.same_numbers and self.lengt >= 3:
            self.vaild = True
        else:
            self.valid = False
        return self.valid
        #self.consecutive_numbers = 
        #if  # and consecutive numbers:
        #    return True
        #elif np.all([i == self.numbers[0] for i in self.numbers]) # and different colours:
        #    return True
        #else:
        #    return False

    def _same_colours(self):
        return np.all([i == self.colours[0] for i in self.colours])
    
    def _diff_colours(self):
        if len(self.colours) == len(set(self.colours)):
            return True
        else:
            return False
    
    def _same_numbers(self):
        return np.all([i == self.numbers[0] for i in self.numbers])
        
        
    def _cons_numbers(self):  
        self.stones_out = self.stones[1:].copy()
        self.stones_in = [self.stones[0]]
        # print(self.stones_in[0].num)
        diff = True
        while diff:
            for c, s_out in enumerate(self.stones_out):
                if s_out.num == self.stones_in[-1].n_h:
                    self.stones_in.append(s_out)
                    self.stones_out.pop(c)
                    break
                elif s_out.num == self.stones_in[0].n_l:
                    self.stones_in.insert(0, s_out)
                    self.stones_out.pop(c)
                    break
            else:
                diff = False
    
        if len(self.stones_out) == 0:
            self.stones = self.stones_in.copy()
            del self.stones_out
            del self.stones_in
            return True
        else:
            del self.stones_out
            del self.stones_in
        return False



class Game:
    def __init__(self, id):
        self.p1Went = False
        self.p2Went = False
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.wins = [0,0]
        self.ties = 0

    def get_player_move(self, p):
        """
        :param p: [0,1]
        :return: Move
        """
        return self.moves[p]

    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

    def connected(self):
        return self.ready

    def bothWent(self):
        return self.p1Went and self.p2Went

    def winner(self):

        p1 = self.moves[0].upper()[0]
        p2 = self.moves[1].upper()[0]

        winner = -1
        if p1 == "R" and p2 == "S":
            winner = 0
        elif p1 == "S" and p2 == "R":
            winner = 1
        elif p1 == "P" and p2 == "R":
            winner = 0
        elif p1 == "R" and p2 == "P":
            winner = 1
        elif p1 == "S" and p2 == "P":
            winner = 0
        elif p1 == "P" and p2 == "S":
            winner = 1

        return winner

    def resetWent(self):
        self.p1Went = False
        self.p2Went = False
