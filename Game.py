# Author: Ben Platt
# Last Update: 5/02/2023
from tkinter import *
from tkinter import messagebox, Tk
# If you can't install PIL (or if you're getting an error with the library, try installing Pillow
# instead with "pip install Pillow" since PIL is a fork of Pillow
from PIL import Image, ImageTk
# if playsound raises a weird error or doesn't work correctly try "pip install PyObjC"
from playsound import playsound
import client
import timekeeper
import threading

class Game:
    # ---------------------------- Begin: Variables and Initializations ----------------------------
    # initialize root and window geometry
    root: Tk = Tk()
    root.geometry("900x900")

    # Create timekeeper for white and black
    white_time = timekeeper.Timer("WHITE")
    black_time = timekeeper.Timer("BLACK")

    # Variables that define the start of the game. White goes first, no buttons have been pressed, nothing has been captured
    white_turn = True
    button_pressed = 0
    capture = False

    # online only
    # pieces = color of pieces
    pieces = "UNKNOWN"
    # boolean if the user will play online chess
    play_online = False
    # client class object from client.py
    client = client.Client()

    # Some castling variables
    wh_king_moved = False
    wh_queenside_rook_moved = False
    wh_kingside_rook_moved = False
    bl_king_moved = False
    bl_queenside_rook_moved = False
    bl_kingside_rook_moved = False

    # defines the indices of each row
    r1 = [*range(0, 8, 1)]
    r2 = [*range(8, 16, 1)]
    r3 = [*range(16, 24, 1)]
    r4 = [*range(24, 32, 1)]
    r5 = [*range(32, 40, 1)]
    r6 = [*range(40, 48, 1)]
    r7 = [*range(48, 56, 1)]
    r8 = [*range(56, 64, 1)]

    # for a bug with bishops and queens going off diagonal
    black_squares = [1, 3, 5, 7, 8, 10, 12, 14, 17, 19, 21, 23, 24, 26, 28, 30, 33, 35, 37, 39, 40, 42, 44, 46, 49, 51,
                     53, 55, 56, 58, 60, 62]
    white_squares = [2, 4, 6, 9, 11, 13, 15, 16, 18, 20, 22, 25, 27, 29, 31, 32, 34, 36, 38, 41, 43, 45, 47, 48, 50, 52,
                     54, 57, 59, 61, 63]

    # white pawn needs to reach row 1 to promote
    row1 = [0, 1, 2, 3, 4, 5, 6, 7]
    # black pawn needs to reach row 8 to promote
    row8 = [56, 57, 58, 59, 60, 61, 62, 63]

    promotion_buttons = [*range(0, 9, 1)]
    # ---------------------------- End: Variables and Initializations ----------------------------

    # ---------------------------- Begin: Stuff to put white into check ----------------------------
    # get row of white king (for check)
    def get_wh_ki_row(self, white_king_ind):
        if white_king_ind in self.r1:
            white_king_row = 1
        elif white_king_ind in self.r2:
            white_king_row = 2
        elif white_king_ind in self.r3:
            white_king_row = 3
        elif white_king_ind in self.r4:
            white_king_row = 4
        elif white_king_ind in self.r5:
            white_king_row = 5
        elif white_king_ind in self.r6:
            white_king_row = 6
        elif white_king_ind in self.r7:
            white_king_row = 7
        elif white_king_ind in self.r8:
            white_king_row = 8
        return white_king_row


    # checks if white is in check
    def white_in_check(self):
        button_indices = [*range(0, 64, 1)]
        # get index of white king (index_new)
        for i in button_indices:
            if buttons[i]["image"] is not "":
                if buttons[i]["image"] in white_pieces:
                    if buttons[i]["image"] in white_ki:
                        global white_king_ind
                        white_king_ind = i
                        break
        # get row of black king (row_new)
        white_king_row = self.get_wh_ki_row(white_king_ind)
        # loop through all black pieces and see if they can attack white king
        for i in button_indices:
            if buttons[i]["image"] is not "":
                if buttons[i]["image"] in black_pieces:
                    # pawn - need index and button
                    if buttons[i]["image"] in black_p:
                        button_pass = buttons[i]
                        global index_stored
                        index_stored = i
                        if self.black_pawn_move(white_king_ind, button_pass, self.r2):
                            return True
                    # knight - need index and row
                    if buttons[i]["image"] in black_kn:
                        index_stored = i
                        global row_stored
                        row_stored = self.get_piece_row()
                        if self.knight_move(white_king_ind, white_king_row):
                            return True
                    if buttons[i]["image"] in black_b:
                        index_stored = i
                        row_stored = self.get_piece_row()
                        if self.bishop_move(white_king_ind, white_king_row):
                            return True
                    if buttons[i]["image"] in black_r:
                        index_stored = i
                        row_stored = self.get_piece_row()
                        if self.rook_move(white_king_ind, white_king_row):
                            return True
                    if buttons[i]["image"] in black_q:
                        index_stored = i
                        row_stored = self.get_piece_row()
                        if self.queen_move(white_king_ind, white_king_row):
                            return True
                    if buttons[i]["image"] in black_ki:
                        index_stored = i
                        if self.king_move(white_king_ind, white_king_row):
                            return True


    # get row of specified piece. this can be applied to both white and black checks
    def get_piece_row(self):
        global row_stored
        if index_stored in self.r1:
            row_stored = 1
        elif index_stored in self.r2:
            row_stored = 2
        elif index_stored in self.r3:
            row_stored = 3
        elif index_stored in self.r4:
            row_stored = 4
        elif index_stored in self.r5:
            row_stored = 5
        elif index_stored in self.r6:
            row_stored = 6
        elif index_stored in self.r7:
            row_stored = 7
        elif index_stored in self.r8:
            row_stored = 8
        return row_stored

    # ---------------------------- End: Stuff to put white into check ----------------------------

    # ---------------------------- Begin: Stuff to put black into check ----------------------------
    # get row of black king
    def get_bl_ki_row(self, black_king_ind):
        if black_king_ind in self.r1:
            black_king_row = 1
        elif black_king_ind in self.r2:
            black_king_row = 2
        elif black_king_ind in self.r3:
            black_king_row = 3
        elif black_king_ind in self.r4:
            black_king_row = 4
        elif black_king_ind in self.r5:
            black_king_row = 5
        elif black_king_ind in self.r6:
            black_king_row = 6
        elif black_king_ind in self.r7:
            black_king_row = 7
        elif black_king_ind in self.r8:
            black_king_row = 8
        return black_king_row


    # checks if black is in check
    def black_in_check(self):
        button_indices = [*range(0, 64, 1)]
        # get index of black_king (index_new)
        for i in button_indices:
            if buttons[i]["image"] is not "":
                if buttons[i]["image"] in black_pieces:
                    if buttons[i]["image"] in black_ki:
                        global black_king_ind
                        black_king_ind = i
                        break
        # get row of black king (row_new)
        black_king_row = self.get_bl_ki_row(black_king_ind)
        # loop through all white pieces and see if they can attack black king
        for i in button_indices:
            if buttons[i]["image"] is not "":
                if buttons[i]["image"] in white_pieces:
                    # pawn - need index and button
                    if buttons[i]["image"] in white_p:
                        global button_pass
                        button_pass = buttons[i]
                        global index_stored
                        index_stored = i
                        global row_stored
                        row_stored = self.get_piece_row()
                        if self.white_pawn_move(black_king_ind, button_pass, self.r7):
                            return True
                    # knight - need index and row
                    if buttons[i]["image"] in white_kn:
                        index_stored = i
                        row_stored = self.get_piece_row()
                        if self.knight_move(black_king_ind, black_king_row):
                            return True
                    if buttons[i]["image"] in white_b:
                        index_stored = i
                        row_stored = self.get_piece_row()
                        if self.bishop_move(black_king_ind, black_king_row):
                            return True
                    if buttons[i]["image"] in white_r:
                        index_stored = i
                        row_stored = self.get_piece_row()
                        if self.rook_move(black_king_ind, black_king_row):
                            return True
                    if buttons[i]["image"] in white_q:
                        index_stored = i
                        row_stored = self.get_piece_row()
                        if self.queen_move(black_king_ind, black_king_row):
                            return True
                    if buttons[i]["image"] in white_ki:
                        index_stored = i
                        row_stored = self.get_piece_row()
                        if self.king_move(black_king_ind, black_king_row):
                            return True
    # ---------------------------- End: Stuff to put black into check ----------------------------


    # ---------------------------- Begin: Castling ----------------------------
    # checks if castling is possible for black
    def black_is_castling(self, diff):
        if not self.bl_king_moved:
            # queenside
            if diff == -2:
                if not self.bl_queenside_rook_moved:
                    # move rook before return
                    buttons[3].config(image=buttons[0]["image"])
                    buttons[0].config(image="")
                    return True
                else:
                    return False
            # kingside
            if diff == 2:
                if not self.bl_kingside_rook_moved:
                    # move rook before return
                    buttons[5].config(image=buttons[7]["image"])
                    buttons[7].config(image="")
                    return True
                else:
                    return False
        else:
            return False


    # checks if castling is possible for white
    def white_is_castling(self, diff):
        if not self.wh_king_moved:
            # queenside
            if diff == -2:
                if not self.wh_queenside_rook_moved:
                    buttons[59].config(image=buttons[56]["image"])
                    buttons[56].config(image="")
                    return True
                elif self.wh_queenside_rook_moved:
                    return False
            if diff == 2:
                if not self.wh_kingside_rook_moved:
                    buttons[61].config(image=buttons[63]["image"])
                    buttons[63].config(image="")
                    return True
                elif self.wh_kingside_rook_moved:
                    return False
        elif self.wh_king_moved:
            return False
    # ---------------------------- End: Castling ----------------------------

    # ---------------------------- Begin: Pawn Promotion ----------------------------
    # Creates a separate GUI window that allows the user to select which piece to promote the pawn to.
    # Destroys the window after piece is selected. Online: Also sends the promotion information to the server.
    # Separate functions for white and black promotion since the windows look different.
    def do_black_pawn_promotion(self, button):
        piece_chosen = button["image"]
        buttons[pawn_index].configure(image=piece_chosen)
        # Online only: send promotion info to other client
        if self.play_online:
            if button["image"] in black_q:
                promote = 0
            elif button["image"] in black_kn:
                promote = 1
            elif button["image"] in black_r:
                promote = 2
            elif button["image"] in black_b:
                promote = 3
            piece_select = self.combine_to_string(real_index_stored, row_stored)
            piece_move = self.combine_to_string(real_index_new, real_row_new, promote)
            result = piece_select + " " + piece_move
            self.client.client_send(result)
        self.promotion_buttons[4].destroy()
        self.promotion_buttons[5].destroy()
        self.promotion_buttons[6].destroy()
        self.promotion_buttons[7].destroy()
        self.root.geometry("900x900")

    def do_white_pawn_promotion(self, button):
        piece_chosen = button["image"]
        buttons[pawn_index].configure(image=piece_chosen)
        # Online only: send promotion info to other client
        if self.play_online:
            if button["image"] in white_q:
                promote = 0
            elif button["image"] in white_kn:
                promote = 1
            elif button["image"] in white_r:
                promote = 2
            elif button["image"] in white_b:
                promote = 3
            piece_select = self.combine_to_string(real_index_stored, row_stored)
            piece_move = self.combine_to_string(real_index_new, real_row_new, promote)
            result = piece_select + " " + piece_move
            self.client.client_send(result)
        # remove buttons
        self.promotion_buttons[0].destroy()
        self.promotion_buttons[1].destroy()
        self.promotion_buttons[2].destroy()
        self.promotion_buttons[3].destroy()
        self.root.geometry("900x900")

    # Displays and places the buttons for pawn promotion
    def black_pawn_promotion_menu(self, button):
        # fix the geometry of the GUI window
        self.root.geometry("1013x900")
        # Pawn promotion buttons - black
        self.promotion_buttons[4] = Button(self.root, bg="white", padx=51.5, pady=44.5, activebackground="#B2E77C",
                                      image=black_queen,
                                      command=lambda: self.do_black_pawn_promotion(self.promotion_buttons[4]))
        self.promotion_buttons[5] = Button(self.root, bg="white", padx=51.5, pady=44.5, activebackground="#B2E77C",
                                      image=black_knight,
                                      command=lambda: self.do_black_pawn_promotion(self.promotion_buttons[5]))
        self.promotion_buttons[6] = Button(self.root, bg="white", padx=51.5, pady=44.5, activebackground="#B2E77C",
                                      image=black_rook,
                                      command=lambda: self.do_black_pawn_promotion(self.promotion_buttons[6]))
        self.promotion_buttons[7] = Button(self.root, bg="white", padx=51.5, pady=44.5, activebackground="#B2E77C",
                                      image=black_bishop,
                                      command=lambda: self.do_black_pawn_promotion(self.promotion_buttons[7]))
        # place buttons
        self.promotion_buttons[4].place(x=900, y=900-112.5)
        self.promotion_buttons[5].place(x=900, y=900-(2*112.5))
        self.promotion_buttons[6].place(x=900, y=900-(3*112.5))
        self.promotion_buttons[7].place(x=900, y=900-(4*112.5))
        # add the rook to valid rook images
        black_r.append(self.promotion_buttons[6]["image"])

    def white_pawn_promotion_menu(self, button):
        # fix the geometry of the GUI window
        self.root.geometry("1013x900")
        # Create Pawn promotion buttons - White
        self.promotion_buttons[0] = Button(self.root, bg="white", padx=51.5, pady=44.5, activebackground="#B2E77C",
                                      image=white_queen,
                                      command=lambda: self.do_white_pawn_promotion(self.promotion_buttons[0]))
        self.promotion_buttons[1] = Button(self.root, bg="white", padx=51.5, pady=44.5, activebackground="#B2E77C",
                                      image=white_knight,
                                      command=lambda: self.do_white_pawn_promotion(self.promotion_buttons[1]))
        self.promotion_buttons[2] = Button(self.root, bg="white", padx=51.5, pady=44.5, activebackground="#B2E77C",
                                      image=white_rook,
                                      command=lambda: self.do_white_pawn_promotion(self.promotion_buttons[2]))
        self.promotion_buttons[3] = Button(self.root, bg="white", padx=51.5, pady=44.5, activebackground="#B2E77C",
                                      image=white_bishop,
                                      command=lambda: self.do_white_pawn_promotion(self.promotion_buttons[3]))
        # place buttons
        self.promotion_buttons[0].place(x=900, y=0)
        self.promotion_buttons[1].place(x=900, y=112.5)
        self.promotion_buttons[2].place(x=900, y=2*112.5)
        self.promotion_buttons[3].place(x=900, y=3*112.5)
        # add the rook to valid rook images
        white_r.append(self.promotion_buttons[2]["image"])

    # Pawn promotion checker function - works for black and white
    def check_pawn_promotion(self, index_new):
        # white pawn needs to reach row 1 to promote
        row1 = [0, 1, 2, 3, 4, 5, 6, 7]
        # black pawn needs to reach row 8 to promote
        row8 = [56, 57, 58, 59, 60, 61, 62, 63]
        if button_stored["image"] in white_pieces:
            if index_new in row1:
                return True
            else:
                return False
        elif button_stored["image"] in black_pieces:
            if index_new in row8:
                return True
            else:
                return False
    # ---------------------------- End: Pawn Promotion ----------------------------

    # ---------------------------- Begin: Special Functions for Online Play ----------------------------
    # convert the set of received moves into a string that can be sent over TCP (after encoding)
    def combine_to_string(self, num1, num2, num3=-2):
        # default string, no special actions (not castling or promoting pawns)
        if num3 == -2:
            num1 = str(num1)
            num2 = str(num2)
            result = num1 + " " + num2
            return result
        else:
            num1 = str(num1)
            num2 = str(num2)
            num3 = str(num3)
            result = num1 + " " + num2 + " " + num3
            return result

    # Convert the received string message into a list of ints that can be used as move input
    def convert_to_list(self, string):
        result = []
        start = 0
        end = 0
        # algorithm for pulling all the int values out of the string
        for i in range(len(string)):
            # normal case: not the end of the string
            if string[i] == " ":
                end = i
                substring = string[start:end]

                substring = int(substring)
                result.append(substring)
                start = i
            # edge case 1: when the last move is a single digit
            if i == len(string) - 1 and string[i - 1] == " ":
                substring = string[i]
                substring = int(substring)
                result.append(substring)
                return result
            # edge case 2: last move has multiple digits
            if i == len(string) - 1:
                end = i
                substring = string[start:end + 1]
                substring = int(substring)
                result.append(substring)
        return result

    # This is a special function that is run in a separate thread. It is designed to wait to a). receive a message from
    # the other player. b). turn that message into the move that was made by the other client. and c). perform that move.
    # Step 1: Parse the string and get the move information
    # Step 2: Convert the list of moves into separate ints
    # Step 3: Perform the move (configure the buttons and play the move sound)
    def update_board(self):
        # wait for message
        while self.client.message is "":
            continue
            # do nothing if we don't have the message yet

        # get list of moves
        move_string = self.client.message
        move_list = self.convert_to_list(move_string)

        # get individual moves
        if len(move_list) == 4:
            store_index = move_list[0]
            new_index = move_list[2]
            row = move_list[3]
        elif len(move_list) == 5:
            store_index = move_list[0]
            new_index = move_list[2]
            extra_move = move_list[4]

        if self.pieces == "WHITE":
            # perform the configuration if other client is black
            button_old = buttons[store_index]
            button_new = buttons[new_index]
            button_new.config(image=button_old["image"])
            button_old.config(image="")

            # castles for BLACK pieces, since this is waiting for BLACKs move
            if len(move_list) == 5 and extra_move == -1:
                diff = new_index - store_index
                # castle queenside, just need to move the rook
                if diff == -2:
                    buttons[3].config(image=buttons[0]["image"])
                    buttons[0].config(image="")
                # castle kingside
                elif diff == 2:
                    buttons[5].config(image=buttons[7]["image"])
                    buttons[7].config(image="")
            # pawn promotion for BLACK pieces
            elif len(move_list) == 5 and -1 < extra_move <= 3:
                # promote to queen
                if extra_move == 0:
                    button_new.config(image=black_queen)
                # to knight
                elif extra_move == 1:
                    button_new.config(image=black_knight)
                # to rook
                elif extra_move == 2:
                    button_new.config(image=black_rook)
                # to bishop
                elif extra_move == 3:
                    button_new.config(image=black_bishop)
            self.client.message = ""
            # Will RECURSIVELY create a new thread listening for the promotion piece if there is an enemy pawn in the home row
            # Pawn promotion: we need to wait and receieve a message detailing what piece it will be promoted to
            check_promotion = False
            # check if there is a black pawn in row 8, if so, we need to listen for promotion command
            for i in self.row8:
                button_check = buttons[i]
                if button_check["image"] in black_p:
                    check_promotion = True
            if check_promotion:
                promotion_thread = threading.Thread(target=self.update_board)
                promotion_thread.start()
            self.white_turn = True
            self.black_time.stop()
            print()
            print(self.white_time.show())
            print(self.black_time.show())
            print()
            self.white_time.start()
            if self.white_in_check():
                messagebox.showinfo(title="Check!", message="White's king is now in check!")
        elif self.pieces == "BLACK":
            # perform the configuration if other client is white
            button_old = buttons[store_index]
            button_new = buttons[new_index]
            button_new.config(image=button_old["image"])
            button_old.config(image="")

            # castles for WHITE pieces, since this is waiting for WHITEs move
            if len(move_list) == 5 and extra_move == -1:
                diff = new_index - store_index
                # castle queenside
                if diff == -2:
                    buttons[59].config(image=buttons[56]["image"])
                    buttons[56].config(image="")
                # castle kingside
                elif diff == 2:
                    buttons[61].config(image=buttons[63]["image"])
                    buttons[63].config(image="")
            # pawn promotion action for WHITE pieces
            elif len(move_list) == 5 and -1 < extra_move <= 3:
                # promote to queen
                if extra_move == 0:
                    button_new.config(image=white_queen)
                # to knight
                elif extra_move == 1:
                    button_new.config(image=white_knight)
                # to rook
                elif extra_move == 2:
                    button_new.config(image=white_rook)
                # to bishop
                elif extra_move == 3:
                    button_new.config(image=white_bishop)
            self.client.message = ""
            # Will RECURSIVELY create a new thread listening for the promotion piece if there is an enemy pawn in the home row
            # Pawn promotion: we need to wait and receieve a message detailing what piece it will be promoted to
            check_promotion = False
            # check if there is a black pawn in row 8, if so, we need to listen for promotion command
            for i in self.row1:
                button_check = buttons[i]
                if button_check["image"] in white_p:
                    check_promotion = True
            if check_promotion:
                promotion_thread = threading.Thread(target=self.update_board)
                promotion_thread.start()
            self.white_turn = False
            self.white_time.stop()
            print()
            print(self.white_time.show())
            print(self.black_time.show())
            print()
            self.black_time.start()
            if self.black_in_check():
                messagebox.showinfo(title="Check!", message="Black's king is now in check!")
        return

    # ---------------------------- Begin: Piece movement (white and black) ----------------------------
    # Defines legal moves for king. Works for both black and white
    def king_move(self, index_new, row):
        edges = [0, 7, 8, 15, 16, 23, 24, 31, 32, 39, 40, 47, 48, 55, 56, 63]
        diff = index_new - index_stored
        new_row = row_stored - row
        clear = False
        # left and right
        if abs(diff) == 1:
            # bug where king could travel across the board
            if index_new in edges and index_stored in edges:
                return False
            else:
                clear = True
        # up and down
        elif abs(diff) == 8:
            clear = True
        # right diagonal
        elif abs(diff) == 7 and new_row != 0:
            clear = True
        # Left diagonal
        elif abs(diff) == 9 and abs(new_row) == 1:
            clear = True
        # castling
        elif abs(diff) == 2:
            # checks if squares between are empty
            check_for_castling = True
            lower = index_stored
            upper = index_new
            if lower < upper:
                bounds = [*range(lower + 1, upper + 2, 1)]
            elif lower > upper:
                bounds = [*range(lower - 1, upper - 2, -1)]
            for i in bounds:
                if buttons[i]["image"] is not "":
                    if button_stored["image"] in white_pieces:
                        if buttons[i]["image"] in white_r_ks:
                            check_for_castling = True
                            break
                        elif buttons[i]["image"] is not "":
                            check_for_castling = False
                            break
                    elif button_stored["image"] in black_pieces:
                        if buttons[i]["image"] in black_r_ks:
                            check_for_castling = True
                            break
                        elif buttons[i]["image"] is not "":
                            check_for_castling = False
                            break
            if check_for_castling:
                if button_stored["image"] in white_pieces:
                    if self.white_is_castling(diff):
                        clear = True
                elif button_stored["image"] in black_pieces:
                    if self.black_is_castling(diff):
                        clear = True
            else:
                return False
        else:
            return False
        if clear:
            return True


    # Defines legal moves for queen. (really just a combination of code from knight and rook)
    def queen_move(self, index_new, row):
        diff = index_new - index_stored
        new_row = row_stored - row
        clear = True
        # handles right diagonal, takes into account that the farthest right position would also be 0 mod 7
        if diff % 7 == 0 and new_row != 0:
            # bug where white square queen could go along diagonal and climb one square (same as bishop)
            if index_new in self.black_squares and index_stored in self.white_squares:
                return False
            if index_new in self.white_squares and index_stored in self.black_squares:
                return False
            # checks if squares between are empty
            lower = index_stored
            upper = index_new
            if lower < upper:
                bounds = [*range(lower + 7, upper, 7)]
            elif lower > upper:
                bounds = [*range(lower - 7, upper, -7)]
            for i in bounds:
                if buttons[i]["image"] is not "":
                    clear = False
                    break
        # Handles left diagonal, doesn't care about rows because 9 is too large for it to matter
        elif diff % 9 == 0:
            # bug where black square queen could go along diagonal and climb one square (same as bishop)
            if index_new in self.white_squares and index_stored in self.black_squares:
                return False
            if index_new in self.black_squares and index_stored in self.white_squares:
                return False
            # checks if squares between are empty
            lower = index_stored
            upper = index_new
            if lower < upper:
                bounds = [*range(lower + 9, upper, 9)]
            elif lower > upper:
                bounds = [*range(lower - 9, upper, -9)]
            for i in bounds:
                if buttons[i]["image"] is not "":
                    clear = False
                    break
        # Vertical movement
        elif diff % 8 == 0:
            # checks if squares between are empty
            lower = index_stored
            upper = index_new
            if lower < upper:
                bounds = [*range(lower + 8, upper, 8)]
            elif lower > upper:
                bounds = [*range(lower - 8, upper, -8)]
            for i in bounds:
                if buttons[i]["image"] is not "":
                    clear = False
                    break
        # Horizontal movement (same row)
        elif row_stored == row:
            # checks if squares between are empty
            lower = index_stored
            upper = index_new
            if lower < upper:
                bounds = [*range(lower + 1, upper, 1)]
            elif lower > upper:
                bounds = [*range(lower - 1, upper, -1)]
            for i in bounds:
                if buttons[i]["image"] is not "":
                    clear = False
                    break
        else:
            return False
        if clear:
            return True


    # Defines legal moves for bishop. Works for both black and white
    def bishop_move(self, index_new, row):
        diff = index_new - index_stored
        new_row = row_stored - row
        clear = True
        # handles right diagonal, takes into account that the farthest right position would also be 0 mod 7
        if diff % 7 == 0 and new_row != 0:
            # bug where white bishop could go along diagonal and climb one square
            if index_new in self.black_squares and index_stored in self.white_squares:
                return False
            if index_new in self.white_squares and index_stored in self.black_squares:
                return False
            # checks if squares between are empty
            lower = index_stored
            upper = index_new
            if lower < upper:
                bounds = [*range(lower + 7, upper, 7)]
            elif lower > upper:
                bounds = [*range(lower - 7, upper, -7)]
            for i in bounds:
                if buttons[i]["image"] is not "":
                    clear = False
                    break
        # Handles left diagonal, doesn't care about rows because 9 is too large for it to matter
        elif diff % 9 == 0 and new_row != 0:
            # bug where green bishop could go along diagonal and climb one square
            if index_new in self.white_squares and index_stored in self.black_squares:
                return False
            if index_new in self.black_squares and index_stored in self.white_squares:
                return False
            # checks if squares between are empty
            lower = index_stored
            upper = index_new
            if lower < upper:
                bounds = [*range(lower + 9, upper, 9)]
            elif lower > upper:
                bounds = [*range(lower - 9, upper, -9)]
            for i in bounds:
                if buttons[i]["image"] is not "":
                    clear = False
                    break
        else:
            return False
        if clear:
            return True


    # Defines legal moves for knight. Works for both black and white
    def knight_move(self, index_new, row):
        # difference = final position - initial
        diff = index_new - index_stored
        # difference in row
        row_new = row_stored - row
        # up or down 1 then right 2 or left 2
        if abs(diff) == 6:
            return True
        # up or down 1 then left 2 or right 2
        elif abs(diff) == 10 and abs(row_new) == 1:
            return True
        # up or down 2 then right 1 or left 1
        elif abs(diff) == 15 and abs(row_new) == 2:
            return True
        # up or down 2 then left 1 or right 1
        elif abs(diff) == 17 and abs(row_new) == 2:
            return True
        else:
            return False


    # Defines legal rook moves. Works for both black and white
    def rook_move(self, index_new, row):
        diff = index_new-index_stored
        # var to check if squares are clear
        clear = True
        # VERTICAL ROOK MOVEMENT
        if diff % 8 == 0:
            # checks if squares between are empty
            lower = index_stored
            upper = index_new
            if lower < upper:
                bounds = [*range(lower+8, upper, 8)]
            elif lower > upper:
                bounds = [*range(lower-8, upper, -8)]
            for i in bounds:
                if buttons[i]["image"] is not "":
                    clear = False
                    break
        # HORIZONTAL ROOK MOVEMENT
        elif row_stored == row:
            # checks if squares between are empty
            lower = index_stored
            upper = index_new
            if lower < upper:
                bounds = [*range(lower + 1, upper, 1)]
            elif lower > upper:
                bounds = [*range(lower - 1, upper, -1)]
            for i in bounds:
                if buttons[i]["image"] is not "":
                    clear = False
                    break
        else:
            return False
        # capture the space as long as it is empty (last hurdle)
        if clear:
            return True


    # Defines legal pawn moves for black
    def black_pawn_move(self, index_new, button, row7):
        diff = index_new-index_stored
        # Pawn can move 1 square forward typically
        if diff == 8:
            if button["image"] is "":
                return True
        # Pawn can move 2 squares from first position
        elif diff == 16 and index_stored in row7:
            if button["image"] is "":
                return True
        # Capturing
        elif diff == 9 or diff == 7:
            if button["image"] is not "":
                return True
        else:
            return False


    # Defines legal pawn moves for white
    def white_pawn_move(self, index_new, button, row2):
        diff = index_new-index_stored
        # Pawn can move 1 square forward typically
        if diff == -8:
            if button["image"] is "":
                return True
        # Pawn can move 2 squares from first position
        elif diff == -16 and index_stored in row2:
            if button["image"] is "":
                return True
        # Capturing
        elif diff == -9 or diff == -7:
            if index_stored == 48 and index_new == 39:
                return False
            if button["image"] is not "":
                return True
        else:
            return False
    # ---------------------------- End: Piece movement (white and black) ----------------------------


    # ---------------------------- Begin: General Button Command (controls flow of game) ----------------------------
    # this happens when a button is clicked, accounts for the movement of pieces. Calls other functions that determine legal moves
    def button_clicked(self, button, index, row):
        # A bunch of global information that is used to make the game flow.
        # Need all the information about the button that was previously clicked in order to determine a legal move
        global white_turn
        global button_pressed
        global button_stored
        global piece_stored
        global capture
        global index_stored
        global real_index_stored
        global row_stored
        global color_stored
        global pawn_index
        global real_index_new
        global real_row_new

        # for castling
        global wh_king_moved
        global wh_queenside_rook_moved
        global wh_kingside_rook_moved
        global bl_king_moved
        global bl_queenside_rook_moved
        global bl_kingside_rook_moved

        # pawn move stuff, old but don't feel like refactoring
        row2 = [48, 49, 50, 51, 52, 53, 54, 55]
        row7 = [8, 9, 10, 11, 12, 13, 14, 15]

        # Determines if a piece can legally move to chosen space
        can_move = False

        # Online only - helpful local variables to tell the other client to check for castling.
        # Also, variables needed for online pawn promotion
        check_castling = False
        real_index_new = index
        real_row_new = row

        # Singleplayer only - sounds filenames for piece movement and capture
        capture_sound = 'capture.wav'
        movement_sound = 'movement.wav'

        # Both Online and Singleplayer - color of selected piece
        highlight_color = "#ebe834"

        # ---------------------------- SINGLEPLAYER CODE ----------------------------
        # White turn singleplayer
        if self.play_online is False and self.white_turn is True:
            # First button press - selects the piece to be moved
            if self.button_pressed == 0:
                # If there is no piece, doesn't select
                if button["image"] is "":
                    return
                # Only allowed if the piece is white
                elif button["image"] in white_pieces:
                    self.button_pressed = 1
                    # Storing important information about the piece, button, color, etc.
                    button_stored = button
                    real_index_stored = index
                    index_stored = index
                    row_stored = row
                    color_stored = button.cget('bg')
                    # highlighting the selected button for convenience of the player
                    button.config(bg=highlight_color)
            # Second button press - moves the piece
            elif self.button_pressed == 1:
                # set the color of the selected square back to the original
                button_stored.config(bg=color_stored)
                # prevents self destruct
                if button_stored is button:
                    self.button_pressed = 0
                    return
                # prevents friendly fire
                elif button["image"] in white_pieces:
                    self.button_pressed = 0
                    return
                # Checks legality of the move that is performed. These if statements are trying to deduce which piece was moved
                if button_stored["image"] in white_p:
                    if self.white_pawn_move(index, button, row2):
                        # check for promotion condition, then promotes
                        if self.check_pawn_promotion(index):
                            pawn_index = index
                            # pause game while white team selects the promotion piece
                            self.white_pawn_promotion_menu(button)
                        # if function deems the move legal and the pawn promotion menu isn't mapped, can_move is true
                        can_move = True
                    else:
                        self.button_pressed = 0
                elif button_stored["image"] in white_r_qs:
                    if self.rook_move(index, row):
                        self.wh_queenside_rook_moved = True
                        can_move = True
                    else:
                        self.button_pressed = 0
                elif button_stored["image"] in white_r_ks:
                    if self.rook_move(index, row):
                        self.wh_kingside_rook_moved = True
                        can_move = True
                    else:
                        self.button_pressed = 0
                elif button_stored["image"] in white_r:
                    if self.rook_move(index, row):
                        can_move = True
                    else:
                        self.button_pressed = 0
                elif button_stored["image"] in white_kn:
                    if self.knight_move(index, row):
                        can_move = True
                    else:
                        self.button_pressed = 0
                elif button_stored["image"] in white_b:
                    if self.bishop_move(index, row):
                        can_move = True
                    else:
                        self.button_pressed = 0
                elif button_stored["image"] in white_q:
                    if self.queen_move(index, row):
                        can_move = True
                    else:
                        self.button_pressed = 0
                elif button_stored["image"] in white_ki:
                    if self.king_move(index, row):
                        self.wh_king_moved = True
                        can_move = True
                    else:
                        self.button_pressed = 0
                if can_move is True:
                    if button["image"] is "":
                        # empty space movement sound
                        playsound(movement_sound)
                    elif button["image"] is not "":
                        # capture piece sound
                        playsound(capture_sound)
                    self.button_pressed = 0
                    # reverts if move places black into check
                    revert1 = button_stored["image"]
                    revert2 = button["image"]
                    # Second button that is pressed becomes the new piece
                    button.config(image=button_stored["image"])
                    # Deletes the old piece
                    button_stored.config(image="")
                    # Does this move place your king into check? if so, reverts and gives you another turn
                    if self.white_in_check():
                        button.config(image=revert2)
                        button_stored.config(image=revert1)
                        messagebox.showerror(title="Illegal!", message="That move would put your king into check! Try again")
                        self.button_pressed = 0
                        return
                    # is black king in check?
                    if self.black_in_check():
                        messagebox.showinfo(title="Check!", message="Black's king is now in check!")
                    # Now it's blacks turn
                    self.white_turn = False
                    self.white_time.stop()
                    # empty print statements in order to separate the times
                    print()
                    print(self.white_time.show())
                    print(self.black_time.show())
                    print()
                    self.black_time.start()

        # Black turn singleplayer
        elif self.play_online is False and self.white_turn is False:
            # First button press - selects the piece to be moved
            if self.button_pressed == 0:
                # If there is no piece, doesn't select
                if button["image"] is "":
                    return
                # Only allowed if the piece is black
                elif button["image"] in black_pieces:
                    self.button_pressed = 1
                    # Storing important information about the piece, button, color, etc.
                    button_stored = button
                    real_index_stored = index
                    index_stored = index
                    row_stored = row
                    color_stored = button.cget('bg')
                    # highlighting the selected button for convenience of the player
                    button.config(bg=highlight_color)
            # Second button press - moves the piece
            elif self.button_pressed == 1:
                # set the color of the selected square back to the original
                button_stored.config(bg=color_stored)
                # prevents self destruct
                if button_stored is button:
                    self.button_pressed = 0
                    return
                # prevents friendly fire
                elif button["image"] in black_pieces:
                    self.button_pressed = 0
                    return
                # Checks legality of the move that is performed. These if statements are trying to deduce which piece was moved
                if button_stored["image"] in black_p:
                    if self.black_pawn_move(index, button, row7):
                        # check for promotion condition, then promotes
                        if self.check_pawn_promotion(index):
                            pawn_index = index
                            self.black_pawn_promotion_menu(button)
                        # if function deems the move legal, can_move is true
                        can_move = True
                    else:
                        self.button_pressed = 0
                elif button_stored["image"] in black_r_qs:
                    if self.rook_move(index, row):
                        self.bl_queenside_rook_moved = True
                        can_move = True
                    else:
                        self.button_pressed = 0
                elif button_stored["image"] in black_r_ks:
                    if self.rook_move(index, row):
                        self.bl_kingside_rook_moved = True
                        can_move = True
                    else:
                        self.button_pressed = 0
                elif button_stored["image"] in black_r:
                    if self.rook_move(index, row):
                        can_move = True
                    else:
                        self.button_pressed = 0
                elif button_stored["image"] in black_kn:
                    if self.knight_move(index, row):
                        can_move = True
                    else:
                        self.button_pressed = 0
                elif button_stored["image"] in black_b:
                    if self.bishop_move(index, row):
                        can_move = True
                    else:
                        self.button_pressed = 0
                elif button_stored["image"] in black_q:
                    if self.queen_move(index, row):
                        can_move = True
                elif button_stored["image"] in black_ki:
                    if self.king_move(index, row):
                        self.bl_king_moved = True
                        can_move = True
                    else:
                        self.button_pressed = 0
                # if move is legal, captures space
                if can_move is True:
                    if button["image"] is "":
                        # not capture sound
                        playsound(movement_sound)
                    elif button["image"] is not "":
                        # capture sound
                        playsound(capture_sound)
                    self.button_pressed = 0
                    # reverts if move places black into check
                    revert1 = button_stored["image"]
                    revert2 = button["image"]
                    # Second button that is pressed becomes the new piece
                    button.config(image=button_stored["image"])
                    # Deletes the old piece
                    button_stored.config(image="")
                    # Does this move put black in check? if so, revert
                    if self.black_in_check():
                        button.config(image=revert2)
                        button_stored.config(image=revert1)
                        messagebox.showerror(title="Illegal!", message="That move would put your king into check! Try again")
                        self.button_pressed = 0
                        return
                    # is white king in check?
                    if self.white_in_check():
                        messagebox.showinfo(title="Check!", message="White's king is now in check!")
                    # Now it's white's turn
                    self.white_turn = True
                    self.black_time.stop()
                    print()
                    print(self.white_time.show())
                    print(self.black_time.show())
                    print()
                    self.white_time.start()

        # ---------------------------- ONLINE CODE ----------------------------
        # IF PLAYER IS WHITE PIECES
        if self.play_online is True and self.pieces == "WHITE":
            if self.white_turn is True:
                # First button press - selects the piece to be moved
                if self.button_pressed == 0:
                    # If there is no piece, doesn't select
                    if button["image"] is "":
                        return
                    # Only allowed if the piece is white
                    elif button["image"] in white_pieces:
                        self.button_pressed = 1
                        # Storing important information about the piece, button, color, etc.
                        button_stored = button
                        real_index_stored = index
                        index_stored = index
                        row_stored = row
                        color_stored = button.cget('bg')
                        # highlighting the selected button for convenience of the player
                        button.config(bg=highlight_color)
                # Second button press - moves the piece
                elif self.button_pressed == 1:
                    # set the color of the selected square back to the original
                    button_stored.config(bg=color_stored)
                    # prevents self destruct
                    if button_stored is button:
                        self.button_pressed = 0
                        return
                    # prevents friendly fire
                    elif button["image"] in white_pieces:
                        self.button_pressed = 0
                        return
                    # Checks legality of the move that is performed. These if statements are trying to deduce which piece was moved
                    if button_stored["image"] in white_p:
                        if self.white_pawn_move(index, button, row2):
                            # check for promotion condition, then promotes
                            if self.check_pawn_promotion(index):
                                pawn_index = index
                                # pause game while white team selects the promotion piece
                                self.white_pawn_promotion_menu(button)
                            # if function deems the move legal and the pawn promotion menu isn't mapped, can_move is true
                            can_move = True
                        else:
                            self.button_pressed = 0
                    elif button_stored["image"] in white_r_qs:
                        if self.rook_move(index, row):
                            self.wh_queenside_rook_moved = True
                            can_move = True
                        else:
                            self.button_pressed = 0
                    elif button_stored["image"] in white_r_ks:
                        if self.rook_move(index, row):
                            self.wh_kingside_rook_moved = True
                            can_move = True
                        else:
                            self.button_pressed = 0
                    elif button_stored["image"] in white_r:
                        if self.rook_move(index, row):
                            can_move = True
                        else:
                            self.button_pressed = 0
                    elif button_stored["image"] in white_kn:
                        if self.knight_move(index, row):
                            can_move = True
                        else:
                            self.button_pressed = 0
                    elif button_stored["image"] in white_b:
                        if self.bishop_move(index, row):
                            can_move = True
                        else:
                            self.button_pressed = 0
                    elif button_stored["image"] in white_q:
                        if self.queen_move(index, row):
                            can_move = True
                        else:
                            self.button_pressed = 0
                    elif button_stored["image"] in white_ki:
                        if self.king_move(index, row):
                            self.wh_king_moved = True
                            can_move = True
                            check_castling = True
                        else:
                            self.button_pressed = 0
                    # if move is legal, captures space
                    if can_move is True:
                        # No playsounds - doesn't function with the online portion
                        self.button_pressed = 0
                        # reverts if move places black into check
                        revert1 = button_stored["image"]
                        revert2 = button["image"]
                        # Second button that is pressed becomes the new piece
                        button.config(image=button_stored["image"])
                        # Deletes the old piece
                        button_stored.config(image="")
                        # Does this move place your king into check? if so, reverts and gives you another chance
                        if self.white_in_check():
                            button.config(image=revert2)
                            button_stored.config(image=revert1)
                            messagebox.showerror(title="Illegal!",
                                                 message="That move would put your king into check! Try again")
                            self.button_pressed = 0
                            return
                        # is opposing king in check?
                        if self.black_in_check():
                            messagebox.showinfo(title="Check!", message="Black's king is now in check!")
                        # ********** UNIQUE TO ONLINE ********** SEND OTHER CLIENT INFORMATION ABOUT THIS MOVE
                        if not check_castling:
                            piece_select = self.combine_to_string(real_index_stored, row_stored)
                            piece_move = self.combine_to_string(index, row)
                            result = piece_select +  " " + piece_move
                        if check_castling:
                            piece_select = self.combine_to_string(real_index_stored, row_stored)
                            piece_move = self.combine_to_string(index, row, -1)
                            result = piece_select + " " + piece_move
                            # set it back to False so it doesn't keep executing this code in subsequent turns
                            check_castling = False
                        self.client.client_send(result)
                        # Now it's blacks turn, but we need to wait for their move in the online game
                        self.white_turn = False
                        self.white_time.stop()
                        # print time usage
                        print()
                        print(self.white_time.show())
                        print(self.black_time.show())
                        print()
                        self.black_time.start()
                        # Creates an update thread that waits for the black pieces client to perform a move
                        # NOTE: this thread accounts for pawn promotion BY ITSELF
                        update_thread = threading.Thread(target=self.update_board)
                        update_thread.start()

        # IF PLAYER IS BLACK PIECES
        elif self.play_online is True and self.pieces == "BLACK":
            if self.white_turn is False:
                # First button press - selects the piece to be moved
                if self.button_pressed == 0:
                    # If there is no piece, doesn't select
                    if button["image"] is "":
                        return
                    # Only allowed if the piece is black
                    elif button["image"] in black_pieces:
                        self.button_pressed = 1
                        # Storing important information about the piece, button, color, etc.
                        button_stored = button
                        real_index_stored = index
                        index_stored = index
                        row_stored = row
                        color_stored = button.cget('bg')
                        # highlighting the selected button for convenience of the player
                        button.config(bg=highlight_color)
                # Second button press - moves the piece
                elif self.button_pressed == 1:
                    # set the color of the selected square back to the original
                    button_stored.config(bg=color_stored)
                    # prevents self destruct
                    if button_stored is button:
                        self.button_pressed = 0
                        return
                    # prevents friendly fire
                    elif button["image"] in black_pieces:
                        self.button_pressed = 0
                        return
                    # Checks legality of the move that is performed. These if statements are trying to deduce which piece was moved
                    if button_stored["image"] in black_p:
                        if self.black_pawn_move(index, button, row7):
                            # check for promotion condition, then promotes
                            if self.check_pawn_promotion(index):
                                pawn_index = index
                                self.black_pawn_promotion_menu(button)
                            # if function deems the move legal, can_move is true
                            can_move = True
                        else:
                            self.button_pressed = 0
                    elif button_stored["image"] in black_r_qs:
                        if self.rook_move(index, row):
                            self.bl_queenside_rook_moved = True
                            can_move = True
                        else:
                            self.button_pressed = 0
                    elif button_stored["image"] in black_r_ks:
                        if self.rook_move(index, row):
                            self.bl_kingside_rook_moved = True
                            can_move = True
                        else:
                            self.button_pressed = 0
                    elif button_stored["image"] in black_r:
                        if self.rook_move(index, row):
                            can_move = True
                        else:
                            self.button_pressed = 0
                    elif button_stored["image"] in black_kn:
                        if self.knight_move(index, row):
                            can_move = True
                        else:
                            self.button_pressed = 0
                    elif button_stored["image"] in black_b:
                        if self.bishop_move(index, row):
                            can_move = True
                        else:
                            self.button_pressed = 0
                    elif button_stored["image"] in black_q:
                        if self.queen_move(index, row):
                            can_move = True
                    elif button_stored["image"] in black_ki:
                        if self.king_move(index, row):
                            self.bl_king_moved = True
                            can_move = True
                            check_castling = True
                        else:
                            self.button_pressed = 0
                    # if move is legal, captures space
                    if can_move is True:
                        self.button_pressed = 0
                        # reverts if move places black into check
                        revert1 = button_stored["image"]
                        revert2 = button["image"]
                        # Second button that is pressed becomes the new piece
                        button.config(image=button_stored["image"])
                        # Deletes the old piece
                        button_stored.config(image="")
                        # Does this move put black in check? if so, revert
                        if self.black_in_check():
                            button.config(image=revert2)
                            button_stored.config(image=revert1)
                            messagebox.showerror(title="Illegal!",
                                                 message="That move would put your king into check! Try again")
                            self.button_pressed = 0
                            return
                        # is white king in check?
                        if self.white_in_check():
                            messagebox.showinfo(title="Check!", message="White's king is now in check!")
                        # ********** UNIQUE TO ONLINE ********** SEND OTHER CLIENT INFORMATION ABOUT THIS MOVE
                        if not check_castling:
                            piece_select = self.combine_to_string(real_index_stored, row_stored)
                            piece_move = self.combine_to_string(index, row)
                            result = piece_select + " " + piece_move
                        if check_castling:
                            piece_select = self.combine_to_string(real_index_stored, row_stored)
                            piece_move = self.combine_to_string(index, row, -1)
                            result = piece_select + " " + piece_move
                        self.client.client_send(result)
                        # Now it's white's turn, but we need to wait for their move in the online game
                        self.white_turn = True
                        self.black_time.stop()
                        print()
                        print(self.white_time.show())
                        print(self.black_time.show())
                        print()
                        self.white_time.start()
                        # Creates an update thread that waits for the white pieces client to perform a move
                        # NOTE: this thread accounts for pawn promotion BY ITSELF
                        update_thread = threading.Thread(target=self.update_board)
                        update_thread.start()

    # ---------------------------- End: General Button Command ----------------------------


    # ---------------------------- Begin: Board and Image Construction (Using array of buttons, labels and images downloaded on the internet) ----------------------------
    # Constructs the board using a list of 64 buttons and some labels (helpful to the user).
    def board(self):
        # white pieces variables,2 sets needed to calculate legal moves.
        # 1st set of variables is assigned to unified set of images (for determining teams)`
        # 2nd set is assigned to individual images (for determining individual moves)
        global white_pawn
        global white_rook_qs
        global white_rook_ks
        global white_knight
        global white_queen
        global white_king
        global white_bishop
        global white_rook

        global white_p
        global white_r_qs
        global white_r_ks
        global white_kn
        global white_q
        global white_ki
        global white_b
        global white_pieces

        # Defines each list for white's team pieces
        white_p = [*range(0, 1, 1)]
        white_r_qs = [*range(0, 1, 1)]
        white_r_ks = [*range(0, 1, 1)]
        white_kn = [*range(0, 1, 1)]
        white_q = [*range(0, 1, 1)]
        white_ki = [*range(0, 1, 1)]
        white_b = [*range(0, 1, 1)]
        white_pieces = [*range(0, 6, 1)]

        # black pieces variables, 2 sets needed to calculate legal moves
        # 1st set of variables is assigned to unified set of images (for determining teams)`
        # 2nd set is assigned to individual images (for determining individual moves)
        global black_pawn
        global black_rook_qs
        global black_rook_ks
        global black_knight
        global black_queen
        global black_king
        global black_bishop
        global black_rook

        global black_p
        global black_r_qs
        global black_r_ks
        global black_kn
        global black_q
        global black_ki
        global black_b
        global black_pieces

        # pawn promotion rooks
        global white_r
        global black_r

        # Defines each list for black's team pieces
        black_p = [*range(0, 1, 1)]
        black_r_qs = [*range(0, 1, 1)]
        black_r_ks = [*range(0, 1, 1)]
        black_kn = [*range(0, 1, 1)]
        black_q = [*range(0, 1, 1)]
        black_ki = [*range(0, 1, 1)]
        black_b = [*range(0, 1, 1)]
        black_pieces = [*range(0, 6, 1)]
        black_r = [*range(0, 1, 1)]
        white_r = [*range(0, 1, 1)]

        # Importing and resizing white piece images to fit board geometry ("raw" = not resized)
        white_pawn_raw = Image.open("White Pieces Images/white_pawn.png")
        white_pawn_raw = white_pawn_raw.resize((108, 108), Image.ANTIALIAS)
        white_pawn = ImageTk.PhotoImage(white_pawn_raw)

        white_rook_raw = Image.open("White Pieces Images/white_rook.png")
        white_rook_raw = white_rook_raw.resize((108, 108), Image.ANTIALIAS)
        white_rook = white_rook_qs = white_rook_ks = ImageTk.PhotoImage(white_rook_raw)

        white_knight_raw = Image.open("White Pieces Images/white_knight.png")
        white_knight_raw = white_knight_raw.resize((108, 108), Image.ANTIALIAS)
        white_knight = ImageTk.PhotoImage(white_knight_raw)

        white_queen_raw = Image.open("White Pieces Images/white_queen.png")
        white_queen_raw = white_queen_raw.resize((108, 108), Image.ANTIALIAS)
        white_queen = ImageTk.PhotoImage(white_queen_raw)

        white_king_raw = Image.open("White Pieces Images/white_king.png")
        white_king_raw = white_king_raw.resize((108, 108), Image.ANTIALIAS)
        white_king = ImageTk.PhotoImage(white_king_raw)

        white_bishop_raw = Image.open("White Pieces Images/white_bishop.png")
        white_bishop_raw = white_bishop_raw.resize((108, 108), Image.ANTIALIAS)
        white_bishop = ImageTk.PhotoImage(white_bishop_raw)

        # Importing and resizing black piece images to fit board geometry ("raw" = not resized)
        black_pawn_raw = Image.open("Black Pieces Images/black_pawn.png")
        black_pawn_raw = black_pawn_raw.resize((108, 108), Image.ANTIALIAS)
        black_pawn = ImageTk.PhotoImage(black_pawn_raw)

        black_rook_raw = Image.open("Black Pieces Images/black_rook.png")
        black_rook_raw = black_rook_raw.resize((108, 108), Image.ANTIALIAS)
        black_rook = black_rook_qs = black_rook_ks = ImageTk.PhotoImage(black_rook_raw)

        black_knight_raw = Image.open("Black Pieces Images/black_knight.png")
        black_knight_raw = black_knight_raw.resize((108, 108), Image.ANTIALIAS)
        black_knight = ImageTk.PhotoImage(black_knight_raw)

        black_queen_raw = Image.open("Black Pieces Images/black_queen.png")
        black_queen_raw = black_queen_raw.resize((108, 108), Image.ANTIALIAS)
        black_queen = ImageTk.PhotoImage(black_queen_raw)

        black_king_raw = Image.open("Black Pieces Images/black_king.png")
        black_king_raw = black_king_raw.resize((108, 108), Image.ANTIALIAS)
        black_king = ImageTk.PhotoImage(black_king_raw)

        black_bishop_raw = Image.open("Black Pieces Images/black_bishop.png")
        black_bishop_raw = black_bishop_raw.resize((108, 108), Image.ANTIALIAS)
        black_bishop = ImageTk.PhotoImage(black_bishop_raw)

        # buttons and labels, organized by which row of the board that they are found in. Each button has the same command (button_clicked())
        global buttons
        buttons = [*range(0, 64, 1)]
        # Row 1
        buttons[0] = Button(self.root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", image=black_rook_qs, command=lambda: self.button_clicked(buttons[0], 0, 8))
        l8 = Label(text="8", font=("Arial", 22), fg="#7d945d", bg="#eeeed5")
        l8.place(x=5, y=0)
        buttons[0].place(x=0, y=0)
        buttons[1] = Button(self.root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", image=black_knight, command=lambda: self.button_clicked(buttons[1], 1, 8))
        buttons[1].place(x=112.5, y=0)
        buttons[2] = Button(self.root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", image=black_bishop, command=lambda: self.button_clicked(buttons[2], 2, 8))
        buttons[2].place(x=225, y=0)
        buttons[3] = Button(self.root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", image=black_queen, command=lambda: self.button_clicked(buttons[3], 3, 8))
        buttons[3].place(x=337.5, y=0)
        buttons[4] = Button(self.root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", image=black_king, command=lambda: self.button_clicked(buttons[4], 4, 8))
        buttons[4].place(x=450, y=0)
        buttons[5] = Button(self.root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", image=black_bishop, command=lambda: self.button_clicked(buttons[5], 5, 8))
        buttons[5].place(x=562.5, y=0)
        buttons[6] = Button(self.root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", image=black_knight, command=lambda: self.button_clicked(buttons[6], 6, 8))
        buttons[6].place(x=675, y=0)
        buttons[7] = Button(self.root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", image=black_rook_ks, command=lambda: self.button_clicked(buttons[7], 7, 8))
        buttons[7].place(x=787.5, y=0)

        # Row 2
        buttons[8] = Button(self.root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", image=black_pawn, command=lambda: self.button_clicked(buttons[8], 8, 7))
        buttons[8].place(x=0, y=112.5)
        l7 = Label(text="7", font=("Arial", 22), fg="#eeeed5", bg="#7d945d")
        l7.place(x=5, y=125)
        buttons[9] = Button(self.root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", image=black_pawn, command=lambda: self.button_clicked(buttons[9], 9, 7))
        buttons[9].place(x=112.5, y=112.5)
        buttons[10] = Button(self.root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", image=black_pawn, command=lambda: self.button_clicked(buttons[10], 10, 7))
        buttons[10].place(x=225, y=112.5)
        buttons[11] = Button(self.root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", image=black_pawn, command=lambda: self.button_clicked(buttons[11], 11, 7))
        buttons[11].place(x=337.5, y=112.5)

        buttons[12] = Button(self.root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", image=black_pawn, command=lambda: self.button_clicked(buttons[12], 12, 7))
        buttons[12].place(x=450, y=112.5)
        buttons[13] = Button(self.root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", image=black_pawn, command=lambda: self.button_clicked(buttons[13], 13, 7))
        buttons[13].place(x=562.5, y=112.5)
        buttons[14] = Button(self.root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", image=black_pawn, command=lambda: self.button_clicked(buttons[14], 14, 7))
        buttons[14].place(x=675, y=112.5)
        buttons[15] = Button(self.root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", image=black_pawn, command=lambda: self.button_clicked(buttons[15], 15, 7))
        buttons[15].place(x=787.5, y=112.5)

        # Row 3
        buttons[16] = Button(self.root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: self.button_clicked(buttons[16], 16, 6))
        buttons[16].place(x=0, y=225)
        l6 = Label(text="6", font=("Arial", 22), fg="#7d945d", bg="#eeeed5")
        l6.place(x=5, y=240)
        buttons[17] = Button(self.root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: self.button_clicked(buttons[17], 17, 6))
        buttons[17].place(x=112.5, y=225)
        buttons[18] = Button(self.root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: self.button_clicked(buttons[18], 18, 6))
        buttons[18].place(x=225, y=225)
        buttons[19] = Button(self.root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: self.button_clicked(buttons[19], 19, 6))
        buttons[19].place(x=337.5, y=225)
        buttons[20] = Button(self.root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: self.button_clicked(buttons[20], 20, 6))
        buttons[20].place(x=450, y=225)
        buttons[21] = Button(self.root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: self.button_clicked(buttons[21], 21, 6))
        buttons[21].place(x=562.5, y=225)
        buttons[22] = Button(self.root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: self.button_clicked(buttons[22], 22, 6))
        buttons[22].place(x=675, y=225)
        buttons[23] = Button(self.root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: self.button_clicked(buttons[23], 23, 6))
        buttons[23].place(x=787.5, y=225)

        # Row 4
        buttons[24] = Button(self.root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: self.button_clicked(buttons[24], 24, 5))
        buttons[24].place(x=0, y=337.5)
        l5 = Label(text="5", font=("Arial", 22), fg="#eeeed5", bg="#7d945d")
        l5.place(x=5, y=350)
        buttons[25] = Button(self.root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: self.button_clicked(buttons[25], 25, 5))
        buttons[25].place(x=112.5, y=337.5)
        buttons[26] = Button(self.root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: self.button_clicked(buttons[26], 26, 5))
        buttons[26].place(x=225, y=337.5)
        buttons[27] = Button(self.root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: self.button_clicked(buttons[27], 27, 5))
        buttons[27].place(x=337.5, y=337.5)
        buttons[28] = Button(self.root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: self.button_clicked(buttons[28], 28, 5))
        buttons[28].place(x=450, y=337.5)
        buttons[29] = Button(self.root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: self.button_clicked(buttons[29], 29, 5))
        buttons[29].place(x=562.5, y=337.5)
        buttons[30] = Button(self.root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: self.button_clicked(buttons[30], 30, 5))
        buttons[30].place(x=675, y=337.5)
        buttons[31] = Button(self.root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: self.button_clicked(buttons[31], 31, 5))
        buttons[31].place(x=787.5, y=337.5)

        # Row 5
        buttons[32] = Button(self.root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: self.button_clicked(buttons[32], 32, 4))
        buttons[32].place(x=0, y=450)
        l4 = Label(text="4", font=("Arial", 22), fg="#7d945d", bg="#eeeed5")
        l4.place(x=5, y=455)
        buttons[33] = Button(self.root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: self.button_clicked(buttons[33], 33, 4))
        buttons[33].place(x=112.5, y=450)
        buttons[34] = Button(self.root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: self.button_clicked(buttons[34], 34, 4))
        buttons[34].place(x=225, y=450)
        buttons[35] = Button(self.root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: self.button_clicked(buttons[35], 35, 4))
        buttons[35].place(x=337.5, y=450)
        buttons[36] = Button(self.root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: self.button_clicked(buttons[36], 36, 4))
        buttons[36].place(x=450, y=450)
        buttons[37] = Button(self.root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: self.button_clicked(buttons[37], 37, 4))
        buttons[37].place(x=562.5, y=450)
        buttons[38] = Button(self.root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: self.button_clicked(buttons[38], 38, 4))
        buttons[38].place(x=675, y=450)
        buttons[39] = Button(self.root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: self.button_clicked(buttons[39], 39, 4))
        buttons[39].place(x=787.5, y=450)

        # Row 6
        buttons[40] = Button(self.root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: self.button_clicked(buttons[40], 40, 3))
        buttons[40].place(x=0, y=562.5)
        l3 = Label(text="3", font=("Arial", 22), fg="#eeeed5", bg="#7d945d")
        l3.place(x=5, y=565)
        buttons[41] = Button(self.root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: self.button_clicked(buttons[41], 41, 3))
        buttons[41].place(x=112.5, y=562.5)
        buttons[42] = Button(self.root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: self.button_clicked(buttons[42], 42, 3))
        buttons[42].place(x=225, y=562.5)
        buttons[43] = Button(self.root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: self.button_clicked(buttons[43], 43, 3))
        buttons[43].place(x=337.5, y=562.5)
        buttons[44] = Button(self.root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: self.button_clicked(buttons[44], 44, 3))
        buttons[44].place(x=450, y=562.5)
        buttons[45] = Button(self.root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: self.button_clicked(buttons[45], 45, 3))
        buttons[45].place(x=562.5, y=562.5)
        buttons[46] = Button(self.root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: self.button_clicked(buttons[46], 46, 3))
        buttons[46].place(x=675, y=562.5)
        buttons[47] = Button(self.root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: self.button_clicked(buttons[47], 47, 3))
        buttons[47].place(x=787.5, y=562.5)

        # Row 7
        buttons[48] = Button(self.root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", image=white_pawn, command=lambda: self.button_clicked(buttons[48], 48, 2))
        buttons[48].place(x=0, y=675)
        l2 = Label(text="2", font=("Arial", 22), fg="#7d945d", bg="#eeeed5")
        l2.place(x=5, y=680)
        buttons[49] = Button(self.root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", image=white_pawn, command=lambda: self.button_clicked(buttons[49], 49, 2))
        buttons[49].place(x=112.5, y=675)
        buttons[50] = Button(self.root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", image=white_pawn, command=lambda: self.button_clicked(buttons[50], 50, 2))
        buttons[50].place(x=225, y=675)
        buttons[51] = Button(self.root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", image=white_pawn, command=lambda: self.button_clicked(buttons[51], 51, 2))
        buttons[51].place(x=337.5, y=675)
        buttons[52] = Button(self.root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", image=white_pawn, command=lambda: self.button_clicked(buttons[52], 52, 2))
        buttons[52].place(x=450, y=675)
        buttons[53] = Button(self.root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", image=white_pawn, command=lambda: self.button_clicked(buttons[53], 53, 2))
        buttons[53].place(x=562.5, y=675)
        buttons[54] = Button(self.root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", image=white_pawn, command=lambda: self.button_clicked(buttons[54], 54, 2))
        buttons[54].place(x=675, y=675)
        buttons[55] = Button(self.root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", image=white_pawn, command=lambda: self.button_clicked(buttons[55], 55, 2))
        buttons[55].place(x=787.5, y=675)

        # Row 8 has many more labels (for columns)
        buttons[56] = Button(self.root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", image=white_rook_qs, command=lambda: self.button_clicked(buttons[56], 56, 1))
        buttons[56].place(x=0, y=787.5)

        l1 = Label(text="1", font=("Arial", 25), fg="#eeeed5", bg="#7d945d")
        l1.place(x=5, y=790)

        la = Label(text="a", font=("Arial", 20), fg="#eeeed5", bg="#7d945d")
        la.place(x=95, y=850)

        buttons[57] = Button(self.root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", image=white_knight, command=lambda: self.button_clicked(buttons[57], 57, 1))
        buttons[57].place(x=112.5, y=787.5)

        lb = Label(text="b", font=("Arial", 20), fg="#7d945d", bg="#eeeed5")
        lb.place(x=205, y=850)

        buttons[58] = Button(self.root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", image=white_bishop, command=lambda: self.button_clicked(buttons[58], 58, 1))
        buttons[58].place(x=225, y=787.5)

        lc = Label(text="c", font=("Arial", 20), fg="#eeeed5", bg="#7d945d")
        lc.place(x=320, y=850)

        buttons[59] = Button(self.root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", image=white_queen, command=lambda: self.button_clicked(buttons[59], 59, 1))
        buttons[59].place(x=337, y=787.5)

        ld = Label(text="d", font=("Arial", 20), fg="#7d945d", bg="#eeeed5")
        ld.place(x=430, y=850)

        buttons[60] = Button(self.root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", image=white_king, command=lambda: self.button_clicked(buttons[60], 60, 1))
        buttons[60].place(x=450, y=787.5)

        le = Label(text="e", font=("Arial", 20), fg="#eeeed5", bg="#7d945d")
        le.place(x=545, y=850)

        buttons[61] = Button(self.root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", image=white_bishop, command=lambda: self.button_clicked(buttons[61], 61, 1))
        buttons[61].place(x=562.5, y=787.5)

        lf = Label(text="f", font=("Arial", 20), fg="#7d945d", bg="#eeeed5")
        lf.place(x=660, y=850)

        buttons[62] = Button(self.root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", image=white_knight, command=lambda: self.button_clicked(buttons[62], 62, 1))
        buttons[62].place(x=675, y=787.5)

        lg = Label(text="g", font=("Arial", 20), fg="#eeeed5", bg="#7d945d")
        lg.place(x=770, y=850)

        buttons[63] = Button(self.root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", image=white_rook_ks, command=lambda: self.button_clicked(buttons[63], 63, 1))
        buttons[63].place(x=787.5, y=787.5)

        lh = Label(text="h", font=("Arial", 20), fg="#7d945d", bg="#eeeed5")
        lh.place(x=883, y=850)

        # List of white piece images
        # pawn
        white_pieces.append(buttons[48]["image"])
        white_p.append(buttons[48]["image"])
        # rook
        white_pieces.append(buttons[56]["image"])
        white_r_qs.append(buttons[56]["image"])
        white_r_ks.append(buttons[63]["image"])
        # knight
        white_pieces.append(buttons[57]["image"])
        white_kn.append(buttons[57]["image"])
        # bishop
        white_pieces.append(buttons[58]["image"])
        white_b.append(buttons[58]["image"])
        # queen
        white_pieces.append(buttons[59]["image"])
        white_q.append(buttons[59]["image"])
        # king
        white_pieces.append(buttons[60]["image"])
        white_ki.append(buttons[60]["image"])

        # List of black piece images
        # pawn
        black_pieces.append(buttons[8]["image"])
        black_p.append(buttons[8]["image"])
        # rook
        black_pieces.append(buttons[0]["image"])
        black_r_qs.append(buttons[0]["image"])
        black_r_ks.append(buttons[7]["image"])
        # knight
        black_pieces.append(buttons[1]["image"])
        black_kn.append(buttons[1]["image"])
        # bishop
        black_pieces.append(buttons[2]["image"])
        black_b.append(buttons[2]["image"])
        # queen
        black_pieces.append(buttons[3]["image"])
        black_q.append(buttons[3]["image"])
        # king
        black_pieces.append(buttons[4]["image"])
        black_ki.append(buttons[4]["image"])
    # ---------------------------- End: Board and Image Construction ----------------------------

    # ---------------------------- Begin: Online Chess Init ----------------------------
    def start_online(self):
        # These initial calls will run until the client is connected to another client via the server.
        self.client.get_alias()
        self.client.start()
        self.client.client_send()
    # ---------------------------- End: Online Chess Init ----------------------------

# ---------------------------- Begin: Run the Chess Program ----------------------------
if __name__ == "__main__":
    g = Game()
    # Ask user if they want to play online chess
    message = input("Play online chess? (Y/N)")
    message_caps = message.upper()
    if message_caps == "Y":
        g.play_online = True
        g.start_online()
    else:
        g.root.title("Singleplayer Chess")
        g.play_online = False
        print("Starting game...")
        g.white_time.start()
    # create board once the client is connected successfully and the team is set (online only)
    g.board()
    # Game start sound that is run when the GUI is first opened
    playsound("start.mp3")
    # Set the color pieces that the client can use (online only)
    if g.play_online:
        g.pieces = g.client.pieces
        player_name = g.client.alias
        window_title = "Online Chess. Player name: " + player_name + ", Pieces Color: " + g.pieces
        g.root.title(window_title)
        if g.pieces == "WHITE":
            g.white_time.start()
    # This thread is necessary so that the black team doesn't need to press a button to receive the first move from the white team
    if g.pieces == "BLACK":
        g.white_time.start()
        update_thread = threading.Thread(target=g.update_board)
        update_thread.start()
    # run GUI program
    g.root.mainloop()
# ---------------------------- End: Run the Program ----------------------------
