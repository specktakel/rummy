import numpy as np
import pygame
import os



class Text():
    def __init__(self, text, pos, **kwargs):
        self.text = text
        self.fontsize = kwargs.get('fontsize', 50)
        self.fontname = kwargs.get('fontname', 'Computer Modern Serif')

        self.colour = kwargs.get('colour', (255, 255, 255))
        self.size = kwargs.get('size', (1100, 600))
        self.set_font()
        self.render()
        if pos == "cen_u":
            self.pos = (self.size[0]/2 - self.img.get_width()/2, \
                        self.size[1]/2 - self.img.get_height()/2-100)
        elif pos == "cen_l":
            self.pos = (self.size[0]/2 - self.img.get_width()/2, \
                        self.size[1]/2 - self.img.get_height()/2+100)
        else:
            self.pos = pos


    def set_font(self):
        """Set the font from its name and size."""
        self.font = pygame.font.SysFont(self.fontname, self.fontsize)


    def render(self):
        """Render the text into an image."""
        self.img = self.font.render(self.text, 1, self.colour)
        #self.rect = self.img.get_rect()
        #self.rect.topleft = self.pos


    def blit(self, win):
        """Draw the text image to the screen."""
        win.blit(self.img, self.pos)


class Button():
    def __init__(self, text, x, y, colour=(255, 0, 0), width=None, height=None):
        self.x = x
        self.y = y
        self.colour = colour
        self.text = text
        if width is None:
            self.width = 100
        else:
            self.width = width
        if height is None:
            self.height = 40
        else:
            self.height = height
        self.text = Text(text, (0, 0), fontsize=40)
        self.text.pos = (self.x + round(self.width / 2) - round(self.text.img.get_width() / 2), self.y + round(self.height / 2) - round(self.text.img.get_height() / 2))
        #self.buttons.append(self)


    def blit(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height))
        self.text.blit(win)


    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


class Inventory():
    '''Contains all info of the player's inventory and general table,
    grid can be filled with instances of StoneButtons().
    button_grid is filled with Button() instances.
    coords contains the upper left pixels of the fillable slots.
    '''
    places = {}
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', 'None')
        self.x = kwargs.get('x', 0)
        self.y = kwargs.get('y', 0)
        self.x_slots = kwargs.get('x_slots', 1)
        self.y_slots = kwargs.get('y_slots', 1)
        self.slot_width = kwargs.get('slot_width', 35)
        self.slot_height = kwargs.get('slot_height', 63)
        self.gap_x = kwargs.get('gap_x', 3)
        self.gap_y = kwargs.get('gap_y', 3)
        self.width = kwargs.get('width', 0)
        self.height = kwargs.get('height', self.y_slots * (self.slot_height + self.gap_y)+self.gap_y)
        self.active = [None, None]
        self.colour = kwargs.get('colour', (255, 255, 255))
        self.coords = self.def_coords()
        #print('coords', self.coords)
        #print(self.coords[0, 0, 0], self.coords[0, 0, 1])
        self.button_grid = self.def_slots()    # contains lots of Button() instances for klicking
        #print('grid', self.button_grid)
        self.grid = np.zeros((self.y_slots, self.x_slots), dtype=np.dtype(StoneButtons))
        #super().__init__('inventory', self)
        #print(self.grid)
        #self.stones = np.zeros((self.y_slots, self.x_slots))
        print('initialised obj:', self.name)
        self.places[self.name] = self


    def blit(self, win):
        '''Draws the background of the inventory, not the stones itself!'''
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height))


    def blit_stones(self, win):
        i, j = self.active
        if i is not None:
            pygame.draw.rect(win, (0, 128, 0),\
                             (self.coords[i, j, 0]-3, self.coords[i, j, 1]-3,\
                              self.slot_width+2*3, self.slot_height+2*3))
        for i in range(self.y_slots):
            for j in range(self.x_slots):
                s = self.grid[i, j]
                if s is not 0:
                    #print(type(s))
                    #print(type(s))
                    win.blit(s, self.coords[i, j])
                    #win.blit(inventory.grid[0, 0], inventory.coords[0, 0])


    def def_coords(self):
        coordinates = np.zeros((self.y_slots, self.x_slots, 2))   # order per slot: left_x, low_y, only nodes...
        #print(coordinates.shape)
        for i in range(self.y_slots):
            for j in range(self.x_slots):
                coordinates[i, j, 0] = self.x + self.gap_x  + j * (self.slot_width + self.gap_x)
                #coordinates[i, j, 1] = coordinates[i, j, 0] + self.slot_width
                coordinates[i, j, 1] = self.y + self.gap_y + i * (self.slot_height + self.gap_y)
                #coordinates[i, j, 3] = coordinates[i, j, 0] + self.slot_height
                #print(coordinates[i, j, 0], coordinates[i, j, 1])
        return coordinates


    def def_slots(self):
        dt = np.dtype(Button)
        buttons = np.zeros((self.y_slots, self.x_slots), dtype=dt)
        #print(buttons.shape)
        for i in range(self.y_slots):
            for j in range(self.x_slots):
                buttons[i, j] = Button('', self.coords[i, j, 0], \
                                       self.coords[i, j, 1], 0, \
                                       self.slot_width, self.slot_height)
        return buttons


    def move(self, init, final, other=None):
        y0, x0 = init
        y1, x1 = final
        if other is None:
            self.grid[y1, x1] = self.grid[y0, x0]
            self.grid[y0, x0] = 0
        else:
            other.grid[y1, x1] = self.grid[y0, x0]
            self.grid[y0, x0] = 0



        

    @staticmethod
    def check_click(win, pos, active):
        '''Move stones around the table. If a player is active (active=True), player is able
        to move stones from inventory to table. Else player is only allowed to move
        stones around the player's inventory.
        '''
        tab = Inventory.places['table']
        inv = Inventory.places['inventory']
        '''
        if not active or tab.active == [None, None]:      # If not player's turn or player's turn and no active stone on table.
        #if tab.active == [None, None]:
            for i in range(inv.y_slots):
                for j in range(inv.x_slots):
                    if inv.button_grid[i, j].click(pos) and inv.active == [None, None] and inv.grid[i, j] != 0:
                        inv.active = [i, j]
                    elif inv.button_grid[i, j].click(pos) and inv.active != [None, None] and inv.grid[i, j] == 0:
                        inv.move(inv.active, [i, j])
                        inv.active = [None, None]
                    elif inv.button_grid[i, j].click(pos) and inv.active == [i, j]:
                        inv.active = [None, None]
                    else:
                        pass
        elif active and tab.active != [None, None]:
            for i in range(tab.y_slots):
                for j in range(tab.x_slots):
                    if tab.button_grid[i, j].click(pos) and inv.active != [None, None]:
                        inv.move(inv.active, [i, j], tab)
                        inv.active = [None, None]
                    elif tab.button_grid[i, j].click(pos) and tab.active == [None, None] and tab.grid[i, j] != 0:
                        tab.active = [i, j]
                    elif tab.button_grid[i, j].click(pos) and tab.active != [None, None] and tab.grid[i, j] == 0:
                        tab.move(tab.active, [i, j])
                        tab.active = [None, None]
                    elif tab.button_grid[i, j].click(pos) and tab.active == [i, j]:
                        tab.active = [None, None]
                    else:
                        pass
        '''
        if active:
            check_inventory()
            check_table()
        else:
            check_inventory()




    @staticmethod
    def check_inventory(inv):
        '''Move stones around the inventory. Do not even consider the table here.'''
        for i in range(inv.y_slots):
            for j in range(inv.x_slots):
                if inv.button_grid[i, j].click(pos) and inv.active == [None, None] and inv.grid[i, j] != 0:
                    inv.active = [i, j]
                elif inv.button_grid[i, j].click(pos) and inv.active != [None, None] and inv.grid[i, j] == 0:
                    inv.move(inv.active, [i, j])
                    inv.active = [None, None]
                elif inv.button_grid[i, j].click(pos) and inv.active == [i, j]:
                    inv.active = [None, None]
                else:
                    pass

    @staticmethod
    def check_table(inv, tab):
        for i in range(tab.y_slots):
            for j in range(tab.x_slots):
                if tab.button_grid[i, j].click(pos) and inv.active != [None, None]:
                    inv.move(inv.active, [i, j], tab)
                    inv.active = [None, None]
                elif tab.button_grid[i, j].click(pos) and tab.active == [None, None] and tab.grid[i, j] != 0:
                    tab.active = [i, j]
                elif tab.button_grid[i, j].click(pos) and tab.active != [None, None] and tab.grid[i, j] == 0:
                    tab.move(tab.active, [i, j])
                    tab.active = [None, None]
                elif tab.button_grid[i, j].click(pos) and tab.active == [i, j]:
                    tab.active = [None, None]
                else:
                    pass


    def init_sort(self, stonebuttons, player):
        print("sorting initial inventory...")
        shape = self.grid.shape
        inv = self.grid.flatten()
        print(inv.shape)
        print(player.inventory)
        #for cou, s in enumerate(player.inventory):
        #    print(cou, s.c, s.num)
        #    print(stonebuttons.buttons[s.c][s.num])
        for counter, s in enumerate(player.inventory):
            inv[counter] = stonebuttons.buttons[s.c][s.num]
            #print(s.num, s.c)
        self.grid = np.reshape(inv, shape)
        print(self.grid)


    def sort_draw(self, stonebuttons, player):
        print(self.grid)
        new_stone = player.inventory[-1]
        print(new_stone.c, new_stone.num)
        shape = self.grid.shape
        inv = self.grid.flatten()
        print(inv)
        for cou, v in enumerate(inv):
            if not v:
                print(cou)
                inv[cou] = stonebuttons.buttons[new_stone.c][new_stone.num]
                break
        self.grid = np.reshape(inv, shape)
        print(self.grid)
        


class StoneButtons():
    '''This class contains all needed image objects which can be blitted (?)
       onto the surface. Sort instances of this object into grids of
       table or inventory. Drawing/blitting method should be called onto 
       filled slots, not this object.
       self.buttons[<colour-string>][<number>] contains the image object.
    '''
    def __init__(self):
        self.width = 35
        self.height = 63
        self.gap_x = 3
        self.gap_y = 20
        self.colours = ['black', 'red', 'blue', 'yellow']
        self.buttons = {c: {} for c in self.colours}
        self.image_path = os.path.relpath(os.path.join('images', 'stones'))
        self.files = os.listdir(self.image_path)
        for f in self.files:
            name = f.rstrip('.png')
            strs = name.split('_')
            num = int(strs[-1])
            col = strs[0]
            self.buttons[col][num] = pygame.image.load(os.path.join(self.image_path, f))
            
        #self.buttons['black'][1] = pygame.image.load(os.path.join(self.image_path, self.files[0]))

