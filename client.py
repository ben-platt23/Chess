import socket
import threading


class Client:
    # Ben
    host_server = '192.168.1.204'
    port = 50000
    pieces = "UNKNOWN"
    alias = "UNKNOWN"
    # stored message that can be accessed by the game program
    message = ""

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def client_receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                message_caps = message.upper()
                # send the server my alias
                if message == "What is your name?":
                    self.client.send(self.alias.encode('utf-8'))
                # set my team which should be read by the GUI
                elif message == "YOUR PIECES ARE: WHITE" or message == "YOUR PIECES ARE: WHITE\n":
                    self.pieces = "WHITE"
                    print(message)
                elif message == "YOUR PIECES ARE: BLACK" or message == "YOUR PIECES ARE: BLACK\n":
                    self.pieces = "BLACK"
                    print(message)
                elif message == "Starting game..." or message == "Starting game...\n":
                    print(message)
                    self.message = ""
                elif message_caps == "READY" or message_caps == "READY\n":
                    self.message = ""
                else:
                    # Take the piece data that is received and turn it into a stored
                    # variable to do moves with
                    print(message)
                    self.message = message
                    # print(message)
            except:
                print("Error, closing connection")
                self.client.close()
                break

    def client_send(self, message="DEFAULT"):
        # Before the GUI launches, getting paired with another client which requires the user to send custom messages
        if message == "DEFAULT":
            # Keep getting user input messages until the user types "Y" which implies
            # that they have accepted a match and the server will pair them.
            while True:
                message = input("")
                self.client.send(message.encode('utf-8'))
                message_caps = message.upper()
                if message_caps == "AGREE BLACK" or message_caps == "AGREE WHITE" \
                        or message_caps == "READY":
                    break
        # Just sending the message that is passed through the argument. This is when the GUI has launched,
        # and we're just sending piece data
        else:
            self.client.send(message.encode('utf-8'))

    def start(self):
        self.client.connect((self.host_server, self.port))

        receive_thread = threading.Thread(target=self.client_receive)
        receive_thread.start()

        # send_thread = threading.Thread(target=self.client_send)
        # send_thread.start()

    def get_alias(self):
        self.alias = input("What is your name? (Note: this will be displayed to other users)")

    def set_message(self, message):
        self.message = message

    def set_flag(self, flag):
        self.flag = flag

