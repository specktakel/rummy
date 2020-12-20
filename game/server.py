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

def threaded_client(conn, ID):
    global game_start
    global players_ready
    conn.send(str.encode(str(ID)))
   
    reply = ""
    while True:
        '''Listen for data, if data comes in, let game play out, send data back'''
        try:
            data = pickle.loads(conn.recv(4096))
            if not data:
                break
            else:
                if data == "ready":
                    players_ready += 1
                    reply = "copied"
                    print(f"client {ID} is ready")
                elif data == "get_ready":
                    # print("asked if all players are ready")
                    if players_ready == num_players - 1:
                        reply = True
                    else:
                        reply = False
                else:
                    pass
                conn.sendall(pickle.dumps(reply))
        except:
            break
    '''If game is over, delete game instance and close the connection.'''
    conn.close()
    print("Disconnected from server")



while True:
    # accept new connection
    conn, addr = s.accept()
    print("Connected to", addr)
    # start thread for new client with connection and unique playerID
    start_new_thread(threaded_client, (conn, playerID))
    # increase playerID for next client
    playerID +=1
    num_players += 1
    # if enough players have joined, start game
    if players_ready == playerID:
        game_start = True
        print("Game starting!")
    # nothing else, rest is in threaded_client
