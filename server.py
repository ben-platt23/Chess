import threading
import socket
import random
import time

# REFERENCE VIDEO FOR THIS
# https://www.youtube.com/watch?v=nmzzeAvQHp8

# host address of server, this is my public IPv4 address
# Port chosen because it is inactive when I type "netstat" in bash and
# https://www.reddit.com/r/cybersecurity/comments/mg0lrv/what_is_a_safe_tcp_port_for_me_to_use_for_a/
# Ben
host = '192.168.1.204'
port = 50000

# create server object and start listening for connections
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# key = client, value = alias
clients = {}
# list of tuples, 2 elements in each tuple, they are the pairs of client aliases
pairs = []
# list to hold all clients currently in games
in_game = []

global client_main
global client_req


def printInstructions(client):
    client.send(("Welcome to online chess! Instructions:\n").encode('utf-8'))
    client.send(("1). If you are the first person to join the server, wait for someone to join and ask for a "
                 "game, or enter 'LIST' to refresh and see others in the server\n").encode('utf-8'))
    client.send(("2). If you would like to request a game with someone, simply enter their name "
                 "to request a game. You will be notified if they accept your request.\n").encode('utf-8'))
    client.send(("3). If the player denies your request to join, don't worry! You can refresh the list of other "
                 "players with 'LIST' and request games with others in the server\n").encode('utf-8'))
    client.send(("4). If the player accepts your request to join, you will be asked to 'ready up' by typing 'R'. "
                 "Once you type 'R', the match will begin.\n").encode('utf-8'))
    client.send(("5). If you need to see these instructions again, enter 'INSTR' "
                 "to print them again.\n").encode('utf-8'))


def send_all_aliases(client):
    if len(clients) == 1:
        client.send("You're the first client! PLease wait for someone to join and ask for a game, or "
                    "type 'LIST' to refresh and see others in the server...\n".encode('utf-8'))
        return

    client.send(("All clients currently in the server. Type a name to request a game.\n").encode('utf-8'))
    # client.send("".encode('utf-8'))

    for i in clients:
        # special case if the client is in a game already
        if i in in_game:
            cli_name = clients[i] + " [IN-GAME]\n"
            client.send(cli_name.encode('utf-8'))
            continue
        # special case if the client is the person requesting the list
        if i == client:
            cli_name = clients[i] + " (you)\n"
            client.send(cli_name.encode('utf-8'))
            continue
        # otherwise, just print the name of the client normally.
        cli_name = clients[i] + "\n"
        client.send(cli_name.encode('utf-8'))


def handle_client(client):
    while True:
        try:
            # receive thread
            message = client.recv(1024)
            # print(message)
            message = message.decode('utf-8')
            alias = clients[client]
            message_caps = message.upper()

            # handle sending message to the clients' pair
            has_pair = False
            pair = client
            for i in pairs:
                if client in i:
                    has_pair = True
                    pair_index = (i.index(client) + 1) % 2
                    pair = i[pair_index]

            # only send the other pair the message directly if they are actively in the game.
            if has_pair and client in in_game:
                pair.send(message.encode('utf-8'))

            # handle sending game request
            for i in clients:
                if clients[i] == message:
                    global client_main
                    client_main = client
                    global client_req
                    client_main.send("Game request sent!\n".encode('utf-8'))
                    client_req = i
                    i.send(("Game request from " + clients[client] + ", approve? (Y/N). 'Y' will confirm "
                                                                     "and begin the team selection process!\n"
                            ).encode('utf-8'))

            # handle approving or denying game request, then start choosing pieces
            if message_caps == "Y":
                client.send(("Game accepted! Awaiting approval from " + clients[client_main] +
                             " \nto begin the team selection").encode('utf8'))
                client_main.send("Game request approved! Ready? Type 'R' to confirm match.\n".encode('utf-8'))
                pairs.append((client_main, client))
            elif message_caps == "N":
                client.send("Game deny successful, please keep trying to match with another client "
                            "\n(Enter 'INSTR' for clarification)".encode('utf-8'))
                client_main.send("Game request denied. Try requesting a match from other clients!\n".encode('utf-8'))

            if message_caps == "R":
                client.send("Time to decide which color pieces both players will be! To choose a color, \n"
                            "simply enter 'BLACK' or 'WHITE' to choose your preferred pieces. Note: The other player \n"
                            "must approve your preference to confirm. Otherwise, just type 'FLIP A COIN' to have the \n"
                            "server choose!".encode('utf-8'))
                pair.send("Confirmed! Time to decide which color pieces both players will be! To choose a color, \n"
                          "simply enter 'BLACK' or 'WHITE' to choose your preferred pieces. Note: The other player \n"
                          "must approve your preference to confirm. Otherwise, just type 'FLIP A COIN' to have the \n"
                          "server choose!".encode('utf-8'))

            # Handle flipping a coin to choose teams
            if message_caps == "FLIP A COIN":
                coin = random.randint(0, 1)
                if coin == 0:
                    client.send("YOUR PIECES ARE: WHITE\n".encode('utf-8'))
                    pair.send("Your opponent has opted to flip a coin, here are the results.\n".encode('utf-8'))
                    time.sleep(1)
                    pair.send("YOUR PIECES ARE: BLACK\n".encode('utf-8'))
                else:
                    client.send("YOUR PIECES ARE: BLACK\n".encode('utf-8'))
                    pair.send("Your opponent has opted to flip a coin, here are the results.\n".encode('utf-8'))
                    time.sleep(1)
                    pair.send("YOUR PIECES ARE: WHITE\n".encode('utf-8'))
                client.send("Please enter 'AGREE' to start game on these terms or enter 'DENY' to reject "
                            "these terms\n".encode('utf-8'))
                pair.send("Please enter 'AGREE' to start game on these terms or enter 'DENY' to reject "
                            "these terms\n".encode('utf-8'))

            # Handle negotiating team choices
            if message_caps == "WHITE":
                client.send("Choice request sent!\n".encode('utf-8'))
                pair.send("Your opponent has requested to be the WHITE pieces, making you the BLACK pieces, \n"
                          "please enter 'AGREE BLACK' to start the game on these terms. If you don't like this, type \n"
                          "'DENY' to inform your opponent. Then continue negotiating, or type 'FLIP A COIN' to have \n"
                          "the server decide!".encode('utf-8'))

            if message_caps == "BLACK":
                client.send("Choice request sent!\n".encode('utf-8'))
                pair.send("Your opponent has requested to be the BLACK pieces, making you the WHITE pieces, \n"
                          "please enter 'AGREE WHITE' to start the game on these terms. If you don't like this, type \n"
                          "'DENY' to inform your opponent. Then continue negotiating, or type 'FLIP A COIN' to have \n"
                          "the server decide!".encode('utf-8'))

            if message_caps == "AGREE BLACK":
                client.send("YOUR PIECES ARE: BLACK\n".encode('utf-8'))
                client.send("Starting game...".encode('utf-8'))
                in_game.append(client)
                pair.send("Your opponent has agreed to be the black pieces! Ready to start? "
                          "Enter 'READY' to begin the match!\n".encode('utf-8'))
                pair.send("YOUR PIECES ARE: WHITE\n".encode('utf-8'))
                in_game.append(pair)

            if message_caps == "AGREE WHITE":
                client.send("YOUR PIECES ARE: WHITE\n".encode('utf-8'))
                client.send("Starting game...".encode('utf-8'))
                in_game.append(client)
                pair.send("Your opponent has agreed to be the black pieces! Ready to start? "
                          "Enter 'READY' to begin the match!\n".encode('utf-8'))
                pair.send("YOUR PIECES ARE: BLACK\n".encode('utf-8'))
                in_game.append(pair)

            # handle starting the game after the client enters "READY"
            if message_caps == "READY":
                client.send("Starting game...\n".encode('utf-8'))

            # Handle starting the game after coin flip
            if message_caps == "AGREE":
                if pair in in_game:
                    client.send("Both opponents agree to the terms! Please enter 'READY' to start the game\n".encode('utf-8'))
                    in_game.append(client)
                    pair.send("Both opponents agree to the terms! Please enter 'READY' to start the game\n".encode('utf-8'))
                else:
                    client.send(("Awaiting agreement from " + clients[pair] + "...").encode('utf-8'))
                    in_game.append(client)

            # Handle denying team request
            if message_caps == "DENY":
                client.send("Enter another team preference, or enter 'FLIP A COIN' to have the server "
                            "decide.\n".encode('utf-8'))
                pair.send("Your opponent has denied the team selection. Enter another team preference, or enter "
                          "'FLIP A COIN' to have the server decide.\n".encode('utf-8'))
                if pair in in_game:
                    in_game.remove(pair)

            # Handle giving the client instructions for finding a match
            if message_caps == "INSTR":
                printInstructions(client)

            # Handle giving the client the list of all clients in the server
            if message_caps == "LIST":
                send_all_aliases(client)

            # Log the clients message in the server
            print(alias + ": " + message)
        except Exception as e:
            # get alias of lost client and print it out
            alias = clients[client]
            print(alias, ' has left the server!')
            print(e)
            # print(message)

            # close connection with dropped client
            del clients[client]
            break


# Main function to receive the clients connection
def receive():
    while True:
        # listen for connections
        print('Server is running and listening for connections...')

        # accept connections
        client, address = server.accept()
        print(f'connection is established with {str(address)}')

        # get alias of client
        client.send('What is your name?'.encode('utf-8'))
        alias = client.recv(1024).decode('utf-8')
        clients[client] = alias

        # Log new connection and inform client of successful connection
        print('The alias of the received client is ' + alias)

        # Send client instructions for connecting to a chess match
        printInstructions(client)
        client.send('Note: Connection successfully established to server.\n'.encode('utf-8'))

        # Give client information on other clients in the game
        send_all_aliases(client)

        # Need multi threading to handle multiple clients
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


if __name__ == "__main__":
    receive()
