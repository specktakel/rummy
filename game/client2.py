import pygame
from network import Network
import sys
import pickle
pygame.init()

try:
    name = sys.argv[1]
except IndexError:
    name = None
print(name)
bg = pygame.image.load('images/background.png')




class Text():
    def __init__(self, text, pos, **kwargs):
        self.text = text
        self.fontsize = kwargs.get('fontsize', 50)
        self.fontname = kwargs.get('fontname', 'Computer Modern Serif')
        self.colour = kwargs.get('colour', (255, 255, 255))
        self.bold = kwargs.get('bold', False)


    def set_font(self):
        """Set the font from its name and size."""
        self.font = pygame.font.SysFont(self.fontname, self.fontsize, bold=self.bold)


    def render(self):
        """Render the text into an image."""
        self.img = self.font.render(self.text, 1, self.fontcolor)
        #self.rect = self.img.get_rect()
        #self.rect.topleft = self.pos


    def draw(self):
        """Draw the text image to the screen."""
        self.screen.blit(self.img, self.pos)

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



def add_player_font(win, player_dict):
    for k, v in player_dict.keys():
        name = Text(v['name']
    



width = 1100
height = 600

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rummikub Client")

ready_btn = Button("Ready", 800, 400, (255, 0, 0))

def menu_screen():
    n = Network()
    ID = int(n.getP())
    print(f"You are player {ID}")
    n.send({'name': name, 'ready': False})
    run = True
    clock = pygame.time.Clock()
    ready = False
    ready_sent = False
    others_ready = False
    board = Text("Players:", (950, 50), colour=(255, 255, 255), bold=True)
    while run:
        clock.tick(60)
        win.blit(bg, (0, 0))
        ready_btn.draw(win)
        try:
            player_dict = n.send("get_players")
            show_players(win, player_dict)
            player_dict.pop(ID)
            others_ready = all(list(player_dict[key]['ready'] for key in player_dict.keys()))
        except:
            pass
        font = pygame.font.SysFont("Computer Modern Serif", 60)
        if not others_ready:
            waiting_text = font.render("Waiting for other players", 1, (255,255,255))
        elif others_ready and not ready:
            waiting_text = font.render("Hurry up, the others are ready!", 1, (255, 255, 255))
        if not ready:
            ready_text = font.render("Are you ready? Press 'ready' button!", 1, (255, 255, 255))
        else:
            ready_text = font.render("You pressed ready!", 1, (255, 255, 255))
            if not ready_sent:
                ready_sent = n.send("ready")
            else:
                pass
        if others_ready and ready:
            game_start = True
            run = False


        win.blit(waiting_text, (width/2 - waiting_text.get_width()/2, height/2 - waiting_text.get_height()/2))
        
        win.blit(ready_text, (width/2 - ready_text.get_width()/2, height/2 - ready_text.get_height()/2-100))
        pygame.display.update()
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if ready_btn.click(pos):
                    ready = True
                else:
                    pass
            else:
                pass
    main()


def main():
    while True:
        state = n.send("get_state")
    #print("Game started!")
    #pygame.quit()
    #sys.exit()

while True:
    menu_screen()
