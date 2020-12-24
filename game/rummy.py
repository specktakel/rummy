import numpy as np
import random


class Table():
    def __init__(self):
        self.colours = np.array(['red', 'blue', 'yellow', 'black'])
        self.numbers = np.arange(1, 14, dtype=int)
        self.stones = []
        self.players = []
        # self.blocks = []     # can't access this attribute from child class, useless as of now
        self.grid = [[None for j in range(28)] for i in range(5)]   #i:j, i:row, j:column, is 6 rows by 28 columns
        for c in self.colours:
            for num in self.numbers:
                self.stones.append(Stone(colour=c, number=num))
                self.stones.append(Stone(colour=c, number=num))
                # print(c, num)
        #self.stones.append(stone(j=True))
        #self.stones.append(stone(j=True))
        #for c, name in enumerate(player_names):
        #    self.players.append(Player(name=name, num=c))
        #print(self.players)
        # distribute stones randomly into players' inventories:
        
        # print(rand_order)
        
        


    def add_player(self, name, num):
        print("Added player", name, num)
        player = Player(name=name, num=num)
        self.players.append(player)
        return player
        

    def start_game(self):
        print("Game started!")
        self.rand_order = np.array(random.sample(range(len(self.stones)), len(self.players) * 14))
        for c, p in enumerate(self.players):
            for i in range(c * 14, (c + 1) * 14):
                self.stones[self.rand_order[i]].owner = p.name
                p.inventory.append(self.stones[self.rand_order[i]])
        self.stones = [s for c, s in enumerate(self.stones) if not c in self.rand_order]

    def draw_stone(self, num):
        try:
            i = random.sample(range(len(self.stones)), 1)[0]
            self.stones[i].owner = self.players[num].name
            self.players[num].inventory.append(self.stones[i])
            self.stones.pop(i)
        except ValueError:
            print("No more stones left to draw from.")


    def display_grid(self):
        for row in table.grid:
            r = []
            for slot in row:
                try:
                    r.append([slot.num, slot.c])
                except:
                    r.append('nan')
            print(r)


    def move_stone(self, init, final):
        x1 = init[0]
        y1 = init[1]
        x2 = final[0]
        y2 = final[1]
        if self.grid[x2][y2] is None and self.grid[x1][y1] is not None:
            s = self.grid[x1][y1]
            self.grid[x2][y2] = s
            self.grid[x1][y1] = None
        else:
            print("Impossible move.")     # TODO maybe add reaction for the table to indicate impossible move!


    def set_stone(self, stone, final):
        x = final[0]
        y = final[1]
        if self.grid[x][y] is None:
            self.grid[x][y] = stone
        else:
            print("Impossible move.")


    def reset_all_moves(self):
        pass
        # need to write method to reset all stuff a
        
        
    def move_done(self):
        valid = self.build_blocks()
        return valid


    def build_blocks(self):
        for c, row in enumerate(self.grid):    # run through rows
            b = []
            start = False
            end = False
            for c_2, slot in enumerate(row):
                if slot is not None:
                    b.append(slot)
                    start = True
                    print("Found a stone")
                    print(b)
                else:
                    end = True
                if c_2 == len(row) - 1:
                    end = True
                else:
                    pass
                if end and b:
                    bl = Block(b)
                    try:
                        valid = np.append(valid, bl.check_rules())
                    except UnboundLocalError:
                        valid = np.array([bl.check_rules()])
                    finally:
                        #print(valid)
                        start = False
                        end = False
                    b = []
                    print(valid)
                else:
                    pass
        #print(valid)            
        return np.all(valid)
                        
                    
                
                    
            
class Stone(Table):
    '''Class to define stones, their behaviour etc.
    '''
    
    def __init__(self, colour=None, number=None, j=False):
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


class Player(Table):
    def __init__(self, name=None, num=None):
        self.inventory = []
        self.name = name
        self.number = num
        print(self.name)




class Block(Table):
    def __init__(self, stones):
        self.stones = stones
        self.valid = self.check_rules()


    def check_rules(self):
        self.colours = np.array([s.c for s in self.stones])
        self.numbers = np.array([s.num for s in self.stones])
        self.length = len(self.stones)
        self.same_colours = self._same_colours()
        self.diff_colours = self._diff_colours()
        self.same_numbers = self._same_numbers()
        try:
            self.cons_numbers = self._cons_numbers()
        except IndexError:
            self.valid = False
            return self.valid
        if self.same_colours and self.cons_numbers and self.length >= 3:
            self.valid = True
        elif self.diff_colours and self.same_numbers and self.length >= 3:
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

