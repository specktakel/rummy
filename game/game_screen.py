import pygame
import sys
import os
import numpy as np
from network import Network
import pickle
from gui import *
# import yaml      # TODO write pixel configs in yaml-dicts for layout...
width = 1100
height = 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rummikub Client")
pygame.init()
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rummikub Client")

try:
    name = sys.argv[1]
except IndexError:
    name = None
print(name)
clock = pygame.time.Clock()

def show_players(win, player_dict):  
    player_str = Text('Players:', (950, 20))
    for c, t in enumerate(player_dict.items(), 1):
        text = Text(t[1]['name'], (950, 20 + c * 40))
        text.blit(win)
    player_str.blit(win)

def menu():
    '''TODO: make everything a bit prettier, get handling on clients leaving the lobby'''
    run = True
    n = Network()
    ID = int(n.getP())
    print('ID:', ID)
    if ID < 0:
        print("The game already started, shutting down...")
        pygame.quit()
        sys.exit()
    else:
        print(f"You are player {ID}")
    player_dict = n.send({'name': name, 'ready': False})
    #print(player_dict)
    bg_menu = pygame.image.load('images/background.png')
    ready_btn = Button("Ready", 800, 400)
    menu_buttons = [ready_btn]
    waiting_text = Text("Waiting for other players", "cen_l")
    others_ready_text = Text("Hurry up, the others are ready!", "cen_l")
    ready_text = Text("You pressed ready!", "cen_u")
    not_ready_text = Text("Are you ready? Press 'Ready' button!", "cen_u")
    ready = False
    ready_sent = False
    others_ready = False

    #def show_players(player_dict):
    #    pass


    while run:
        clock.tick(30)
        win.blit(bg_menu, (0, 0))
        ready_btn.blit(win)

        # get current state of players
        try:
            player_dict = n.send("get_players")
            # print(player_dict)
            p_d = player_dict.copy()
            p_d.pop(ID)
            others_ready = all(list(p_d[key]['ready'] for key in p_d.keys()))
            show_players(win, player_dict)
            
        except:
            pass

        # see what needs to be printed to screen...
        if ready:
            if not ready_sent:
                ready_send = n.send("ready")
            else:
                pass
            ready_text.blit(win)

            if others_ready:
                run = False
                break
            else:
                waiting_text.blit(win)

        else:
            if others_ready:
                others_ready_text.blit(win)
                not_ready_text.blit(win)
            else:
                waiting_text.blit(win)
                not_ready_text.blit(win)
                

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = n.send("quit")
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

        


        pygame.display.update()
    return n, ID, player_dict




def game(n, ID, player_dict):
    stonebuttons = StoneButtons()
    table = Inventory(name='table', x=25, y=25, width=800, x_slots=28, y_slots=5, gap_y=20)
    inventory = Inventory(name='inventory', x=25, y=440, width=875, height=135, x_slots=10, y_slots=2, gap_x=3, gap_y=3, colour=(100, 100, 100))
    #print(Inventory.places)
    #inventory.grid[0, 0] = stonebuttons.buttons['black'][1]
    #table.grid[0, 0] = stonebuttons.buttons['black'][1]
    #print(inventory.grid)
    bg_game = pygame.image.load(os.path.join('images', 'background_wood.png'))
    offset_x = 25
    offset_y = 25
    black_1 = pygame.image.load(os.path.join('images', 'stones', 'black_1.png'))
    drawbutton = Button("Draw", 950, 450, (255, 0, 0))
    nextbutton = Button("Next", 950, 510, (255, 0, 0))
    gamebuttons = {'draw': drawbutton, 'next': nextbutton}
    try:
        player = n.send("get_self")
        print("got first player instance")
        inventory.init_sort(stonebuttons, player)
    except:
        pass
    print(player.number, player.name)
    #for i in player.inventory:
    #    print(type(i))

    #repl = n.send("quit")
    #pygame.quit()
    #sys.exit()
    while True:
        clock.tick(15)
        win.blit(bg_game, (0, 0))
        for k, v in gamebuttons.items():
            v.blit(win)
        inventory.blit(win)
        #win.blit(inventory.grid[0, 0], inventory.coords[0, 0])
        #ready_btn.draw(win)
        #text.draw(win)
        #board = n.send("get_table")
        changed = n.send("get_state")
        
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                run = n.send("quit")
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                Inventory.check_click(win, pos)
                if drawbutton.click(pos):
                    print("draw")
                    new_player = n.send("draw")
                    print(new_player)
                    if new_player:
                        print("sorting new stone")
                        inventory.sort_draw(stonebuttons, new_player)
                        player = new_player
                        #del new_player
                    else:
                        print("No more stones to draw from.")
                    print("next player's turn...")
                
                #table.check_click(win, pos)
        inventory.blit_stones(win)
        table.blit_stones(win)
        pygame.display.update()



while True:
    n, ID, player_dict = menu()
    game(n, ID, player_dict)

