import pygame
import sys
import os
import numpy as np
pygame.init()



bg = pygame.image.load(os.path.join('images', 'background_wood.png'))
offset_x = 50
offset_y = 50
black_1 =pygame.image.load(os.path.join('images', 'stones', 'black_1.png'))
print(type(bg))

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


    def draw(self, win):
        """Draw the text image to the screen."""
        win.blit(self.img, self.pos)

class Button():
    def __init__(self, text, x, y, colour):
        self.text = text
        self.x = x
        self.y = y
        self.colour = colour
        self.width = 100
        self.height = 40


    def draw(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (0, 255, 255))
        win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2), self.y + round(self.height / 2) - round(text.get_height() / 2)))


    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False



class StoneButtons():
    
    def __init__(self):
        self.width = 35
        self.height = 63
        self.gap_x = 3
        self.gap_y = 20
        self.colours = ['black', 'red', 'blue', 'yellow']
        self.buttons = {c: {} for c in self.colours}
        self.image_path = os.path.relpath(os.path.join('images', 'stones'))
        self.files = os.listdir(self.image_path)
        #print(self.files)
        self.buttons['black'][1] = pygame.image.load(os.path.join(self.image_path, self.files[0]))
        #self.width = self.im.get_width()
        #self.height = self.im.get_height()
        #self.


    
    def index_to_pos(self, index):
        x = index[0]
        y = index[1]
        px_x = offset_x + x * (self.width + self.gap_x)
        px_y = offset_y + y * (self.height + self.gap_y)
        return [px_x, px_y]

    #@staticmethod
    def draw(self, win, grid):
        for i in range(5):
            for j in range(5):
                if grid[i, j] is not None:
                    win.blit(black_1, self.index_to_pos([i, j]))
        



stonebuttons = StoneButtons()
grid = np.full((28, 6), stonebuttons.buttons['black'][1])
print(grid)


width = 1100
height = 600


win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rummikub Client")


#ready_btn = Button("Ready", 800, 400, (255, 0, 0))
#string = 'Hallo Welt!'
#text = Text(string, (100, 100), colour=(255, 0, 0))
clock = pygame.time.Clock()

while True:
    clock.tick(5)
    win.blit(bg, (0, 0))
    stonebuttons.draw(win, grid)
    #ready_btn.draw(win)
    #text.draw(win)
    pygame.display.update()
    for event in pygame.event.get():
        #print(event)
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()


