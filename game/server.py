from _thread import *
import socket
import sys
# from player import Player
import pickle
from rummy import *
server = "192.168.178.21"
port = 5555


'''Establish connection'''
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((server, port))
except socket.error as e:
    print(e)


s.listen(3)
print("Waiting")


#connected = set()
playerID = 0
game_started = False
players_ready = 0
num_players = 0
player_order = []
player_dict = {}
game = Table()
active_player = 0
order = {}
def threaded_client(conn, ID):
    global active_player
    global order
    global game
    global game_started
    global players_ready
    global num_players
    global player_dict
    global player_order
    
    print(ID)
    if False:   #game_started:
        print("The game already started, disconnecting client", ID)
        conn.send(str.encode(str(-1)))
        conn.close()
    else:
        conn.send(str.encode(str(ID)))
    try:
        data = pickle.loads(conn.recv(4096))
        if not data:
            pass
        else:
            player_dict[ID] = data
        print(player_dict)
        conn.send(pickle.dumps(player_dict))
        player = game.add_player(player_dict[ID]['name'], ID)
        for pl in game.players:
            if pl.number == ID:
                player = pl
                print(f"player with id {ID} in game instance")
                break
        else:
            print(f"no player with id {ID} found")
    except:
        pass
    

    while True:
        '''concerning the lobby.'''
        reply = ""
        try:
            data = pickle.loads(conn.recv(4096))
            if not data:
                continue
            else:
                if data == "quit":
                    conn.sendall(pickle.dumps(False))
                    conn.close()
                    player_dict.pop(ID)
                    break
                    print(f"Disconnected {ID} from server.")
                elif data == "ready" and not player_dict[ID]['ready']:
                    player_dict[ID]['ready'] = True
                    reply = True
                    print(f"client {ID} is ready")
                    print(player_dict)
                    if all(list(player_dict[key]['ready'] for key in player_dict.keys())):
                        print("All players are now ready")
                        game.start_game()
                        game_started = True
                        num_players = len(player_dict)
                        player_order = random.sample(range(num_players), num_players)
                        #break
                elif data == "get_players":
                    # print("asked if all players are ready")
                    reply = player_dict
                else:
                    pass
                conn.sendall(pickle.dumps(reply))
        except:
            break
        if all(list(player_dict[key]['ready'] for key in player_dict.keys())):
            print("Game starting")
            break
        else:
            pass
        

    first = True
    while True:
        #print("number of players", num_players)
        # print("Game started by server!")
        '''Game loop goes here'''
        if first:
            print(f"in Game loop {ID}")
            first = False
            print("player order", player_order)
        reply = ""
        try:
            data = pickle.loads(conn.recv(4096*8))
            if not data:
                break
            else:
                if data == "quit":
                    conn.sendall(pickle.dumps(False))
                    break

                elif data == "get_self":
                    reply = player
                elif data == "get_table":
                    reply = game.grid
                elif data == "draw":
                    valid = game.draw_stone(ID)
                    if valid:
                        reply = player
                    else:
                        reply = False
                elif data == "next":
                    valid = game.move_done()
                    if valid:
                        active_player += 1
                        game.next_player(player_order)
                        
                    else:
                        
                        pass # should check if moves are valid
        except:
            pass
        conn.sendall(pickle.dumps(reply))



        
        




    '''If game is over, delete game instance and close the connection.'''
    conn.close()
    player_dict.pop(ID)
    print("Disconnected from server")



while True:
    if not game_started:
    # accept new connection
        conn, addr = s.accept()
        print("Connected to", addr)
    # start thread for new client with connection and unique playerID
        start_new_thread(threaded_client, (conn, playerID))
        playerID += 1
    # increase playerID for next client
    # if enough players have joined, start game
    #if players_ready == playerID:
    #    game_start = True
    #    print("Game starting!")
    # nothing else, rest is in threaded_client
