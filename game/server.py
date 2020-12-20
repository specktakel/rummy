from _thread import *
import socket
import sys
# from player import Player
import pickle
from game import Game
server = "192.168.178.21"
port = 5555


'''Establish connection'''
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((server, port))
except socket.error as e:
    print(e)


s.listen(2)
print("Waiting")


connected = set()
playerID = 0
game_start = False
players_ready = 0
num_players = 0
player_dict = {}
def threaded_client(conn, ID):
    global game_start
    global players_ready
    global num_players
    global player_dict
    conn.send(str.encode(str(ID)))
    try:
        data = pickle.loads(conn.recv(4096))
        if not data:
            pass
        else:
            player_dict[ID] = data
        print(player_dict)
        conn.send(pickle.dumps(player_dict))
            
    except:
        pass
    reply = ""

    while True:
        '''concerning the lobby.'''
        try:
            data = pickle.loads(conn.recv(4096*8))
            if not data:
                break
            else:
                if data == "ready" and not player_dict[ID]['ready']:
                    player_dict[ID]['ready'] = True
                    reply = True
                    print(f"client {ID} is ready")
                    print(player_dict)
                elif data == "get_players":
                    # print("asked if all players are ready")
                    reply = player_dict
                else:
                    pass
                conn.sendall(pickle.dumps(reply))
        except:
            break
        if all(list(player_dict[key]['ready'] for key in player_dict.keys())):
            game_start = True
            break



    while True:
    #'''Game loop goes here'''
        try:
            data = pickle.loads(conn.recv(4096*8))
            if not data:
                break
            elif data == "get_state":
                





        except:
            break




    '''If game is over, delete game instance and close the connection.'''
    conn.close()
    player_dict.pop(ID)
    print("Disconnected from server")



while True:
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
