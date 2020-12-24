import pygame
import sys
import os
import numpy as np
# import yaml      # TODO write pixel configs in yaml-dicts for layout...
pygame.init()
width = 1100
height = 600


# TODO rewrite: StoneButtons() is class for the images of the stones.
## define class for table and inventory which contain grid with stone or None,
## give grid and coords to StoneButton.blit() for displaying.

bg = pygame.image.load(os.path.join('images', 'background_wood.png'))
offset_x = 25
offset_y = 25
black_1 =pygame.image.load(os.path.join('images', 'stones', 'black_1.png'))
#print(type(bg))


class Text():
    def __init__(self, text, pos, **kwargs):
        self.text = text
        self.fontsize = kwargs.get('fontsize', 50)
        self.fontname = kwargs.get('fontname', 'Computer Modern Serif')
        self.pos = pos
        self.colour = kwargs.get('colour', (255, 255, 255))
        self.set_font()
        self.render()


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
    def __init__(self, text, x, y, colour, width=None, height=None):
        self.text = text
        self.x = x
        self.y = y
        self.colour = colour
        if width is None:
            self.width = 100
        else:
            self.width = width
        if height is None:
            self.height = 40
        else:
            self.height = height
        #self.buttons.append(self)


    def blit(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255, 255, 255))
        win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2), self.y + round(self.height / 2) - round(text.get_height() / 2)))


    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False

'''
class Collection():
    places = {}
    def __init__(self, name, obj):
        self.places['name'] = name
        self.places['obj'] = obj


    def check_click(self, places, win, pos):
        obj = places['inventory']
        inv_active = obj.active
        for i in range(obj.y_slots):
            for j in range(obj.x_slots):
                if obj.button_grid[i, j].click(pos) and self.active == [None, None] and self.grid[i, j] != 0:
                    obj.active = [i, j]
                elif obj.button_grid[i, j].click(pos) and obj.active != [None, None] and obj.grid[i, j] == 0:
                    obj.move(obj.active, [i, j])
                    obj.active = [None, None]
                else:
                    pass
        obj = places['inventory']
        for i in range(obj.y_slots):
            for j in range(obj.x_slots):
                if inv_active != [None, None] and obj.button_grid[i, j].click(pos)
                if obj.button_grid[i, j].click(pos) and obj.active == [None, None] and obj.grid[i, j] != 0:
                    obj.active = [i, j]
                elif obj.button_grid[i, j].click(pos) and obj.active != [None, None] and obj.grid[i, j] == 0:
                    obj.move(obj.active, [i, j])
                    obj.active = [None, None]
                else:
                    pass
'''


class Inventory():
    '''Contains all info of the player's inventory.
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
        print(coordinates.shape)
        for i in range(self.y_slots):
            for j in range(self.x_slots):
                coordinates[i, j, 0] = self.x + self.gap_x  + j * (self.slot_width + self.gap_x)
                #coordinates[i, j, 1] = coordinates[i, j, 0] + self.slot_width
                coordinates[i, j, 1] = self.y + self.gap_y + i * (self.slot_height + self.gap_y)
                #coordinates[i, j, 3] = coordinates[i, j, 0] + self.slot_height
                print(coordinates[i, j, 0], coordinates[i, j, 1])
        return coordinates


    def def_slots(self):
        dt = np.dtype(Button)
        buttons = np.zeros((self.y_slots, self.x_slots), dtype=dt)
        print(buttons.shape)
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
    def check_click(win, pos):
        tab = Inventory.places['table']
        inv = Inventory.places['inventory']
        if tab.active == [None, None]:
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




active_thing = {'active': False, 'owner': None, 'index': [None, None]}



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
        self.buttons['black'][1] = pygame.image.load(os.path.join(self.image_path, self.files[0]))

    '''
    def index_to_pos(self, index):
        x = index[0]
        y = index[1]
        px_x = offset_x + x * (self.width + self.gap_x)
        px_y = offset_y + y * (self.height + self.gap_y)
        return [px_x, px_y]


    def pos_to_index(self, pixel):
        px_x = pixel[0]
        px_y = pixel[1]
        
        

    def blit(self, win, grid, coords):
        for i, v in enumerate(grid):
            for j, w in enumerate(v):
                if grid[i, j] is not None:
                    win.blit(grid[i, j], self.index_to_pos([i, j]))


    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False
    ''' 
        
drawbutton = Button("Draw", 950, 450, (255, 0, 0))
nextbutton = Button("Next", 950, 510, (255, 0, 0))
menubuttons = [drawbutton, nextbutton]

stonebuttons = StoneButtons()
#table = Table()

#table = np.full((28, 5), stonebuttons.buttons['black'][1])
#table[0, 0] = None
#print(grid)


table = Inventory(name='table', x=25, y=25, width=800, x_slots=28, y_slots=5, gap_y=20)
inventory = Inventory(name='inventory', x=25, y=440, width=875, height=135, x_slots=10, y_slots=2, gap_x=3, gap_y=3, colour=(100, 100, 100))
print(Inventory.places)
#inventory = Inventory()
#inventory.stones = np.full((inventory.y_slots, inventory.x_slots), stonebuttons.buttons['black'][1])
inventory.grid[0, 0] = stonebuttons.buttons['black'][1]
table.grid[0, 0] = stonebuttons.buttons['black'][1]
print(inventory.grid)
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rummikub Client")

#ready_btn = Button("Ready", 800, 400, (255, 0, 0))
#string = 'Hallo Welt!'
#text = Text(string, (100, 100), colour=(255, 0, 0))
clock = pygame.time.Clock()

while True:
    clock.tick(30)
    win.blit(bg, (0, 0))
    for btn in menubuttons:
        btn.blit(win)
    #drawbutton.blit(win)
    #stonebuttons.blit(win, table, table_grid)
    inventory.blit(win)
    #win.blit(inventory.grid[0, 0], inventory.coords[0, 0])
    #ready_btn.draw(win)
    #text.draw(win)
    
    for event in pygame.event.get():
        #print(event)
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            Inventory.check_click(win, pos)
            #table.check_click(win, pos)
    inventory.blit_stones(win)
    table.blit_stones(win)
    pygame.display.update()


