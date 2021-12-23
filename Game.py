# Author: Ben Platt
# Date: 12/20/2021
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from playsound import playsound

# initialize root and window geometry
root = Tk()
root.title("Chess - Ben Platt")
root.geometry("900x900")

# Variables that define the start of the game. White goes first, no buttons have been pressed, nothing has been captured
white_turn = True
button_pressed = 0
capture = False

# Some castling variables
wh_king_moved = False
wh_queenside_rook_moved = False
wh_kingside_rook_moved = False
bl_king_moved = False
bl_queenside_rook_moved = False
bl_kingside_rook_moved = False
black_king_ind = 4


# get row of white king (for check)
def get_wh_ki_row(white_king_ind):
    if white_king_ind in r1:
        white_king_row = 1
    elif white_king_ind in r2:
        white_king_row = 2
    elif white_king_ind in r3:
        white_king_row = 3
    elif white_king_ind in r4:
        white_king_row = 4
    elif white_king_ind in r5:
        white_king_row = 5
    elif white_king_ind in r6:
        white_king_row = 6
    elif white_king_ind in r7:
        white_king_row = 7
    elif white_king_ind in r8:
        white_king_row = 8
    return white_king_row


# checks if white is in check
def white_in_check():
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
    white_king_row = get_wh_ki_row(white_king_ind)
    # loop through all black pieces and see if they can attack white king
    for i in button_indices:
        if buttons[i]["image"] is not "":
            if buttons[i]["image"] in black_pieces:
                # pawn - need index and button
                if buttons[i]["image"] in black_p:
                    # get button of piece
                    button_pass = buttons[i]
                    # get index
                    global index_stored
                    index_stored = i
                    if black_pawn_move(white_king_ind, button_pass, r2):
                        print("pawn")
                        return True
                # knight - need index and row
                if buttons[i]["image"] in black_kn:
                    # get index
                    index_stored = i
                    # get row of piece (row_stored)
                    global row_stored
                    row_stored = get_piece_row()
                    if knight_move(white_king_ind, white_king_row):
                        print("knight")
                        return True
                if buttons[i]["image"] in black_b:
                    # get index
                    index_stored = i
                    # get row of piece (row_stored)
                    row_stored = get_piece_row()
                    if bishop_move(white_king_ind, white_king_row):
                        print("bishop")
                        return True
                if buttons[i]["image"] in black_r:
                    # get index
                    index_stored = i
                    # get row of piece (row_stored)
                    row_stored = get_piece_row()
                    if rook_move(white_king_ind, white_king_row):
                        print("rook")
                        return True
                if buttons[i]["image"] in black_q:
                    # get index
                    index_stored = i
                    # get row of piece (row_stored)
                    row_stored = get_piece_row()
                    if queen_move(white_king_ind, white_king_row):
                        print("queen")
                        return True
                if buttons[i]["image"] in black_ki:
                    # get index
                    index_stored = i
                    if king_move(white_king_ind, white_king_row):
                        print("king")
                        return True


# get row of specified piece
def get_piece_row():
    global row_stored
    if index_stored in r1:
        row_stored = 1
    elif index_stored in r2:
        row_stored = 2
    elif index_stored in r3:
        row_stored = 3
    elif index_stored in r4:
        row_stored = 4
    elif index_stored in r5:
        row_stored = 5
    elif index_stored in r6:
        row_stored = 6
    elif index_stored in r7:
        row_stored = 7
    elif index_stored in r8:
        row_stored = 8
    return row_stored


# get row of black king
def get_bl_ki_row(black_king_ind):
    if black_king_ind in r1:
        black_king_row = 1
    elif black_king_ind in r2:
        black_king_row = 2
    elif black_king_ind in r3:
        black_king_row = 3
    elif black_king_ind in r4:
        black_king_row = 4
    elif black_king_ind in r5:
        black_king_row = 5
    elif black_king_ind in r6:
        black_king_row = 6
    elif black_king_ind in r7:
        black_king_row = 7
    elif black_king_ind in r8:
        black_king_row = 8
    return black_king_row


# checks if black is in check
def black_in_check():
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
    black_king_row = get_bl_ki_row(black_king_ind)
    # loop through all white pieces and see if they can attack black king
    for i in button_indices:
        if buttons[i]["image"] is not "":
            if buttons[i]["image"] in white_pieces:
                # pawn - need index and button
                if buttons[i]["image"] in white_p:
                    # get button of piece
                    global button_pass
                    button_pass = buttons[i]
                    # get index
                    global index_stored
                    index_stored = i
                    # get row of piece (row_stored)
                    global row_stored
                    row_stored = get_piece_row()
                    if white_pawn_move(black_king_ind, button_pass, r7):
                        global attacking_piece
                        global attacking_index
                        global attacking_row
                        global pawn
                        pawn = "pawn"
                        attacking_piece = pawn
                        attacking_index = index_stored
                        attacking_row = row_stored
                        print("pawn")
                        return True
                # knight - need index and row
                if buttons[i]["image"] in white_kn:
                    # get index
                    index_stored = i
                    # get row of piece (row_stored)
                    row_stored = get_piece_row()
                    if knight_move(black_king_ind, black_king_row):
                        global knight
                        knight = "knight"
                        attacking_piece = knight
                        attacking_index = index_stored
                        attacking_row = row_stored
                        print("knight")
                        return True
                if buttons[i]["image"] in white_b:
                    # get index
                    index_stored = i
                    # get row of piece (row_stored)
                    row_stored = get_piece_row()
                    if bishop_move(black_king_ind, black_king_row):
                        global bishop
                        bishop = "bishop"
                        attacking_piece = bishop
                        attacking_index = index_stored
                        attacking_row = row_stored
                        print("bishop")
                        return True
                if buttons[i]["image"] in white_r:
                    # get index
                    index_stored = i
                    # get row of piece (row_stored)
                    row_stored = get_piece_row()
                    if rook_move(black_king_ind, black_king_row):
                        global rook
                        rook = "rook"
                        attacking_piece = rook
                        attacking_index = index_stored
                        attacking_row = row_stored
                        print("rook")
                        return True
                if buttons[i]["image"] in white_q:
                    # get index
                    index_stored = i
                    # get row of piece (row_stored)
                    row_stored = get_piece_row()
                    if queen_move(black_king_ind, black_king_row):
                        global queen
                        queen = "queen"
                        attacking_piece = queen
                        attacking_index = index_stored
                        attacking_row = row_stored
                        print("queen")
                        return True
                if buttons[i]["image"] in white_ki:
                    # get index
                    index_stored = i
                    # get row of piece (row_stored)
                    row_stored = get_piece_row()
                    if king_move(black_king_ind, black_king_row):
                        global king
                        king = "king"
                        attacking_piece = king
                        attacking_index = index_stored
                        attacking_row = row_stored
                        print("king")
                        return True


# checks if castling is possible for black, the king legal moves calls this function
def black_is_castling(diff):
    if not bl_king_moved:
        # queenside
        if diff == -2:
            if not bl_queenside_rook_moved:
                # move rook before return
                buttons[3].config(image=buttons[0]["image"])
                buttons[0].config(image="")
                return True
            else:
                return False
        # kingside
        if diff == 2:
            if not bl_kingside_rook_moved:
                # move rook before return
                buttons[5].config(image=buttons[7]["image"])
                buttons[7].config(image="")
                return True
            else:
                return False
    else:
        return False


# checks if castling is possible for white, the king legal moves calls this function
def white_is_castling(diff):
    if not wh_king_moved:
        # queenside
        if diff == -2:
            if not wh_queenside_rook_moved:
                buttons[59].config(image=buttons[56]["image"])
                buttons[56].config(image="")
                return True
            elif wh_queenside_rook_moved:
                return False
        if diff == 2:
            if not wh_kingside_rook_moved:
                buttons[61].config(image=buttons[63]["image"])
                buttons[63].config(image="")
                return True
            elif wh_kingside_rook_moved:
                return False
    elif wh_king_moved:
        return False


# does pawn promotion action for black
def do_black_pawn_promotion(button):
    piece_chosen = button["image"]
    buttons[pawn_index].configure(image=piece_chosen)
    promotion_buttons[4].destroy()
    promotion_buttons[5].destroy()
    promotion_buttons[6].destroy()
    promotion_buttons[7].destroy()
    root.geometry("900x900")


# does pawn promotion action for white
def do_white_pawn_promotion(button):
    piece_chosen = button["image"]
    buttons[pawn_index].configure(image=piece_chosen)
    promotion_buttons[0].destroy()
    promotion_buttons[1].destroy()
    promotion_buttons[2].destroy()
    promotion_buttons[3].destroy()
    root.geometry("900x900")


# Displays pawn promotion menu for black
def black_pawn_promotion_menu(button):
    root.geometry("1013x900")
    # place buttons
    promotion_buttons[4].place(x=900, y=900-112.5)
    promotion_buttons[5].place(x=900, y=900-(2*112.5))
    promotion_buttons[6].place(x=900, y=900-(3*112.5))
    promotion_buttons[7].place(x=900, y=900-(4*112.5))


# Displays pawn promotion menu for white
def white_pawn_promotion_menu(button):
    root.geometry("1013x900")
    # place buttons
    promotion_buttons[0].place(x=900, y=0)
    promotion_buttons[1].place(x=900, y=112.5)
    promotion_buttons[2].place(x=900, y=2*112.5)
    promotion_buttons[3].place(x=900, y=3*112.5)


# Pawn promotion checker function - works for black and white
def check_pawn_promotion(index_new):
    # white pawn needs to reach this row to promote
    row1 = [0, 1, 2, 3, 4, 5, 6, 7]
    # black pawn needs to reach this row to promote
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


# Defines legal moves for king. Works for both black and white
def king_move(index_new, row):
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
                if white_is_castling(diff):
                    clear = True
            elif button_stored["image"] in black_pieces:
                if black_is_castling(diff):
                    clear = True
        else:
            return False
    else:
        return False
    if clear:
        return True


# Defines legal moves for queen. (really just a combination of code from knight and rook)
def queen_move(index_new, row):
    diff = index_new - index_stored
    new_row = row_stored - row
    clear = True
    # handles right diagonal, takes into account that the farthest right position would also be 0 mod 7
    if diff % 7 == 0 and new_row != 0:
        # bug where white square queen could go along diagonal and climb one square (same as bishop)
        if index_new in green_squares and index_stored in white_squares:
            return False
        if index_new in white_squares and index_stored in green_squares:
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
        # bug where green green square queen could go along diagonal and climb one square (same as bishop)
        if index_new in white_squares and index_stored in green_squares:
            return False
        if index_new in green_squares and index_stored in white_squares:
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
def bishop_move(index_new, row):
    diff = index_new - index_stored
    new_row = row_stored - row
    clear = True
    # handles right diagonal, takes into account that the farthest right position would also be 0 mod 7
    if diff % 7 == 0 and new_row != 0:
        # bug where white bishop could go along diagonal and climb one square
        if index_new in green_squares and index_stored in white_squares:
            return False
        if index_new in white_squares and index_stored in green_squares:
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
        if index_new in white_squares and index_stored in green_squares:
            return False
        if index_new in green_squares and index_stored in white_squares:
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
def knight_move(index_new, row):
    # difference = final position - initial
    diff = index_new - index_stored
    # difference in row
    row_new = row_stored - row
    # up or down 1 and right 2 or left 2
    if abs(diff) == 6:
        return True
    # up or down 1 and left 2 or right 2
    elif abs(diff) == 10 and abs(row_new) == 1:
        return True
    # up or down 2 and right 1 or left 1
    elif abs(diff) == 15 and abs(row_new) == 2:
        return True
    # up or down 2 and left 1 or right 1
    elif abs(diff) == 17 and abs(row_new) == 2:
        return True
    else:
        return False


# Defines legal rook moves. Works for both black and white
def rook_move(index_new, row):
    diff = index_new-index_stored
    # var to check if squares are clear
    clear = True
    # Vertical movement
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
    # Capture space
    if clear:
        return True


# Defines legal pawn moves for black
def black_pawn_move(index_new, button, row7):
    diff = index_new-index_stored
    # Pawn can move 1 square forward only
    if diff == 8:
        if button["image"] is "":
            return True
    # Pawn can move 2 squares from first position
    elif diff == 16 and index_stored in row7:
        if button["image"] is "":
            return True
    # Capture condition
    elif diff == 9 or diff == 7:
        if button["image"] is not "":
            return True
    else:
        return False


# Defines legal pawn moves for white
def white_pawn_move(index_new, button, row2):
    diff = index_new-index_stored
    # Pawn can move 1 square forward only
    if diff == -8:
        if button["image"] is "":
            return True
    # Pawn can move 2 squares from first position
    elif diff == -16 and index_stored in row2:
        if button["image"] is "":
            return True
    # Capture condition
    elif diff == -9 or diff == -7:
        if index_stored == 48 and index_new == 39:
            return False
        if button["image"] is not "":
            return True
    else:
        return False


# this happens when a button is clicked, accounts for the movement of pieces. Calls other functions that determine legal moves
def button_clicked(button, index, row):
    # Used these global variables to make coding life easier, these are consistently used by other functions including this one
    # Necessary because I don't have to pass these parameters back and forth. Things would get messy very quick without these.
    global white_turn
    global button_pressed
    global button_stored
    global piece_stored
    global capture
    global index_stored
    global row_stored

    # for pawn promotion
    global pawn_index

    # for castling
    global wh_king_moved
    global wh_queenside_rook_moved
    global wh_kingside_rook_moved
    global bl_king_moved
    global bl_queenside_rook_moved
    global bl_kingside_rook_moved

    # rows for check function
    global r1
    global r2
    global r3
    global r4
    global r5
    global r6
    global r7
    global r8

    r1 = [*range(0, 8, 1)]
    r2 = [*range(8, 16, 1)]
    r3 = [*range(16, 24, 1)]
    r4 = [*range(24, 32, 1)]
    r5 = [*range(32, 40, 1)]
    r6 = [*range(40, 48, 1)]
    r7 = [*range(48, 56, 1)]
    r8 = [*range(56, 64, 1)]

    # for a bug with bishops and queens going off diagonal
    global green_squares
    global white_squares
    green_squares = [1, 3, 5, 7, 8, 10, 12, 14, 17, 19, 21, 23, 24, 26, 28, 30, 33, 35, 37, 39, 40, 42, 44, 46, 49, 51, 53, 55, 56, 58, 60, 62]
    white_squares = [2, 4, 6, 9, 11, 13, 15, 16, 18, 20, 22, 25, 27, 29, 31, 32, 34, 36, 38, 41, 43, 45, 47, 48, 50, 52, 54, 57, 59, 61, 63]

    # pawn move stuff, old but don't feel like refactoring
    row2 = [48, 49, 50, 51, 52, 53, 54, 55]
    row7 = [8, 9, 10, 11, 12, 13, 14, 15]

    # local variable to determine if a piece can legally move to chosen space
    can_move = False

    # White turn
    if white_turn is True:
        # First button press - selects the piece to be moved
        if button_pressed == 0:
            # If there is no piece, doesn't select
            if button["image"] is "":
                return
            # Only allowed if the piece is white
            elif button["image"] in white_pieces:
                button_pressed = 1
                # Stores the button that is pressed
                button_stored = button
                # Stores the index
                index_stored = index
                # Stores the row
                row_stored = row
        # Second button press - moves the piece
        elif button_pressed == 1:
            # prevents self destruct
            if button_stored is button:
                button_pressed = 0
                return
            # prevents friendly fire
            elif button["image"] in white_pieces:
                button_pressed = 0
                return
            # Checks legality of pawn moves
            if button_stored["image"] in white_p:
                if white_pawn_move(index, button, row2):
                    # check for promotion condition, then promotes
                    if check_pawn_promotion(index):
                        pawn_index = index
                        # pause game while white team selects the promotion piece
                        white_pawn_promotion_menu(button)
                    # if function deems the move legal and the pawn promotion menu isn't mapped, can_move is true
                    can_move = True
                else:
                    button_pressed = 0
            # Checks legality of rook moves
            elif button_stored["image"] in white_r_qs:
                if rook_move(index, row):
                    wh_queenside_rook_moved = True
                    can_move = True
                else:
                    button_pressed = 0
            elif button_stored["image"] in white_r_ks:
                if rook_move(index, row):
                    wh_kingside_rook_moved = True
                    can_move = True
                else:
                    button_pressed = 0
            elif button_stored["image"] in white_r:
                if rook_move(index, row):
                    can_move = True
                else:
                    button_pressed = 0
            # Checks legality of knight moves
            elif button_stored["image"] in white_kn:
                if knight_move(index, row):
                    can_move = True
                else:
                    button_pressed = 0
            # Checks legality of bishop moves
            elif button_stored["image"] in white_b:
                if bishop_move(index, row):
                    can_move = True
                else:
                    button_pressed = 0
            # Checks legality of queen moves
            elif button_stored["image"] in white_q:
                if queen_move(index, row):
                    can_move = True
                else:
                    button_pressed = 0
            # Checks legality of king moves
            elif button_stored["image"] in white_ki:
                if king_move(index, row):
                    wh_king_moved = True
                    can_move = True
                else:
                    button_pressed = 0
            # if move is legal, captures space
            if can_move is True:
                if button["image"] is "":
                    # empty space movement sound
                    playsound("movement.wav")
                elif button["image"] is not "":
                    # capture piece sound
                    playsound("capture.wav")
                button_pressed = 0
                # reverts if move places black into check
                revert1 = button_stored["image"]
                revert2 = button["image"]
                # Second button that is pressed becomes the new piece
                button.config(image=button_stored["image"])
                # Deletes the old piece
                button_stored.config(image="")
                # Does this move place your king into check? if so, reverts and gives you another turn
                if white_in_check():
                    button.config(image=revert2)
                    button_stored.config(image=revert1)
                    messagebox.showerror(title="Illegal!", message="That move would put your king into check! Try again")
                    button_pressed = 0
                    return
                # is black king in check?
                if black_in_check():
                    messagebox.showinfo(title="Check!", message="Black's king is now in check!")
                # Now it's blacks turn
                white_turn = False

    # Black turn
    elif white_turn is False:
        # First button press - selects the piece to be moved
        if button_pressed == 0:
            # If there is no piece, doesn't select
            if button["image"] is "":
                return
            # Only allowed if the piece is black
            elif button["image"] in black_pieces:
                button_pressed = 1
                # Stores the button that is pressed
                button_stored = button
                # Stores the index
                index_stored = index
                # Stores the row
                row_stored = row
        # Second button press - moves the piece
        elif button_pressed == 1:
            # prevents self destruct
            if button_stored is button:
                button_pressed = 0
                return
            # prevents friendly fire
            elif button["image"] in black_pieces:
                button_pressed = 0
                return
            # Checks legality of pawn moves
            if button_stored["image"] in black_p:
                if black_pawn_move(index, button, row7):
                    # check for promotion condition, then promotes
                    if check_pawn_promotion(index):
                        pawn_index = index
                        black_pawn_promotion_menu(button)
                    # if function deems the move legal, can_move is true
                    can_move = True
                else:
                    button_pressed = 0
            # Checks legality of rook moves
            elif button_stored["image"] in black_r_qs:
                if rook_move(index, row):
                    bl_queenside_rook_moved = True
                    can_move = True
                else:
                    button_pressed = 0
            elif button_stored["image"] in black_r_ks:
                if rook_move(index, row):
                    bl_kingside_rook_moved = True
                    can_move = True
                else:
                    button_pressed = 0
            elif button_stored["image"] in black_r:
                if rook_move(index, row):
                    can_move = True
                else:
                    button_pressed = 0
            # Checks legality of knight moves
            elif button_stored["image"] in black_kn:
                if knight_move(index, row):
                    can_move = True
                else:
                    button_pressed = 0
            # Calls check function for bishop moves
            elif button_stored["image"] in black_b:
                if bishop_move(index, row):
                    can_move = True
                else:
                    button_pressed = 0
            # Checks legality of queen moves
            elif button_stored["image"] in black_q:
                if queen_move(index, row):
                    can_move = True
            # Checks legality of king moves
            elif button_stored["image"] in black_ki:
                if king_move(index, row):
                    bl_king_moved = True
                    can_move = True
                else:
                    button_pressed = 0
            # if move is legal, captures space
            if can_move is True:
                if button["image"] is "":
                    # not capture sound
                    playsound("movement.wav")
                elif button["image"] is not "":
                    # capture sound
                    playsound("capture.wav")
                button_pressed = 0
                # reverts if move places black into check
                revert1 = button_stored["image"]
                revert2 = button["image"]
                # Second button that is pressed becomes the new piece
                button.config(image=button_stored["image"])
                # Deletes the old piece
                button_stored.config(image="")
                # Does this move put black in check? if so, revert
                if black_in_check():
                    button.config(image=revert2)
                    button_stored.config(image=revert1)
                    messagebox.showerror(title="Illegal!", message="That move would put your king into check! Try again")
                    button_pressed = 0
                    return
                # is black king in check?
                if white_in_check():
                    messagebox.showinfo(title="Check!", message="White's king is now in check!")
                # Now it's white's turn
                white_turn = True


# Constructs the board using a list of 64 buttons and some labels (helpful to the user).
def board():
    # white pieces variables,
    # 2 sets needed to calculate legal moves. 1st set of variables is assigned to unified set of images (for determining teams)`
    # 2nd set is assigned to individual images (for determining individual moves)
    global white_pawn
    global white_rook_qs
    global white_rook_ks
    global white_knight
    global white_queen
    global white_king
    global white_bishop

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
    # 2 sets needed to calculate legal moves. 1st set of variables is assigned to unified set of images (for determining teams)`
    # 2nd set is assigned to individual images (for determining individual moves)
    global black_pawn
    global black_rook_qs
    global black_rook_ks
    global black_knight
    global black_queen
    global black_king
    global black_bishop


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
    # Row 8
    buttons[0] = Button(root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", image=black_rook_qs, command=lambda: button_clicked(buttons[0], 0, 8))
    l8 = Label(text="8", font=("Arial", 22), fg="#7d945d", bg="#eeeed5")
    l8.place(x=5, y=0)
    buttons[0].place(x=0, y=0)
    buttons[1] = Button(root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", image=black_knight, command=lambda: button_clicked(buttons[1], 1, 8))
    buttons[1].place(x=112.5, y=0)
    buttons[2] = Button(root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", image=black_bishop, command=lambda: button_clicked(buttons[2], 2, 8))
    buttons[2].place(x=225, y=0)
    buttons[3] = Button(root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", image=black_queen, command=lambda: button_clicked(buttons[3], 3, 8))
    buttons[3].place(x=337.5, y=0)
    buttons[4] = Button(root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", image=black_king, command=lambda: button_clicked(buttons[4], 4, 8))
    buttons[4].place(x=450, y=0)
    buttons[5] = Button(root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", image=black_bishop, command=lambda: button_clicked(buttons[5], 5, 8))
    buttons[5].place(x=562.5, y=0)
    buttons[6] = Button(root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", image=black_knight, command=lambda: button_clicked(buttons[6], 6, 8))
    buttons[6].place(x=675, y=0)
    buttons[7] = Button(root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", image=black_rook_ks, command=lambda: button_clicked(buttons[7], 7, 8))
    buttons[7].place(x=787.5, y=0)

    # Row 7
    buttons[8] = Button(root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", image=black_pawn, command=lambda: button_clicked(buttons[8], 8, 7))
    buttons[8].place(x=0, y=112.5)
    l7 = Label(text="7", font=("Arial", 22), fg="#eeeed5", bg="#7d945d")
    l7.place(x=5, y=125)
    buttons[9] = Button(root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", image=black_pawn, command=lambda: button_clicked(buttons[9], 9, 7))
    buttons[9].place(x=112.5, y=112.5)
    buttons[10] = Button(root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", image=black_pawn, command=lambda: button_clicked(buttons[10], 10, 7))
    buttons[10].place(x=225, y=112.5)
    buttons[11] = Button(root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", image=black_pawn, command=lambda: button_clicked(buttons[11], 11, 7))
    buttons[11].place(x=337.5, y=112.5)

    buttons[12] = Button(root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", image=black_pawn, command=lambda: button_clicked(buttons[12], 12, 7))
    buttons[12].place(x=450, y=112.5)
    buttons[13] = Button(root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", image=black_pawn, command=lambda: button_clicked(buttons[13], 13, 7))
    buttons[13].place(x=562.5, y=112.5)
    buttons[14] = Button(root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", image=black_pawn, command=lambda: button_clicked(buttons[14], 14, 7))
    buttons[14].place(x=675, y=112.5)
    buttons[15] = Button(root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", image=black_pawn, command=lambda: button_clicked(buttons[15], 15, 7))
    buttons[15].place(x=787.5, y=112.5)

    # Row 6
    buttons[16] = Button(root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: button_clicked(buttons[16], 16, 6))
    buttons[16].place(x=0, y=225)
    l6 = Label(text="6", font=("Arial", 22), fg="#7d945d", bg="#eeeed5")
    l6.place(x=5, y=240)
    buttons[17] = Button(root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: button_clicked(buttons[17], 17, 6))
    buttons[17].place(x=112.5, y=225)
    buttons[18] = Button(root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: button_clicked(buttons[18], 18, 6))
    buttons[18].place(x=225, y=225)
    buttons[19] = Button(root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: button_clicked(buttons[19], 19, 6))
    buttons[19].place(x=337.5, y=225)
    buttons[20] = Button(root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: button_clicked(buttons[20], 20, 6))
    buttons[20].place(x=450, y=225)
    buttons[21] = Button(root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: button_clicked(buttons[21], 21, 6))
    buttons[21].place(x=562.5, y=225)
    buttons[22] = Button(root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: button_clicked(buttons[22], 22, 6))
    buttons[22].place(x=675, y=225)
    buttons[23] = Button(root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: button_clicked(buttons[23], 23, 6))
    buttons[23].place(x=787.5, y=225)

    # Row 5
    buttons[24] = Button(root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: button_clicked(buttons[24], 24, 5))
    buttons[24].place(x=0, y=337.5)
    l5 = Label(text="5", font=("Arial", 22), fg="#eeeed5", bg="#7d945d")
    l5.place(x=5, y=350)
    buttons[25] = Button(root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: button_clicked(buttons[25], 25, 5))
    buttons[25].place(x=112.5, y=337.5)
    buttons[26] = Button(root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: button_clicked(buttons[26], 26, 5))
    buttons[26].place(x=225, y=337.5)
    buttons[27] = Button(root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: button_clicked(buttons[27], 27, 5))
    buttons[27].place(x=337.5, y=337.5)
    buttons[28] = Button(root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: button_clicked(buttons[28], 28, 5))
    buttons[28].place(x=450, y=337.5)
    buttons[29] = Button(root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: button_clicked(buttons[29], 29, 5))
    buttons[29].place(x=562.5, y=337.5)
    buttons[30] = Button(root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: button_clicked(buttons[30], 30, 5))
    buttons[30].place(x=675, y=337.5)
    buttons[31] = Button(root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: button_clicked(buttons[31], 31, 5))
    buttons[31].place(x=787.5, y=337.5)

    # Row 4
    buttons[32] = Button(root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: button_clicked(buttons[32], 32, 4))
    buttons[32].place(x=0, y=450)
    l4 = Label(text="4", font=("Arial", 22), fg="#7d945d", bg="#eeeed5")
    l4.place(x=5, y=455)
    buttons[33] = Button(root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: button_clicked(buttons[33], 33, 4))
    buttons[33].place(x=112.5, y=450)
    buttons[34] = Button(root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: button_clicked(buttons[34], 34, 4))
    buttons[34].place(x=225, y=450)
    buttons[35] = Button(root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: button_clicked(buttons[35], 35, 4))
    buttons[35].place(x=337.5, y=450)
    buttons[36] = Button(root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: button_clicked(buttons[36], 36, 4))
    buttons[36].place(x=450, y=450)
    buttons[37] = Button(root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: button_clicked(buttons[37], 37, 4))
    buttons[37].place(x=562.5, y=450)
    buttons[38] = Button(root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: button_clicked(buttons[38], 38, 4))
    buttons[38].place(x=675, y=450)
    buttons[39] = Button(root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: button_clicked(buttons[39], 39, 4))
    buttons[39].place(x=787.5, y=450)

    # Row 3
    buttons[40] = Button(root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: button_clicked(buttons[40], 40, 3))
    buttons[40].place(x=0, y=562.5)
    l3 = Label(text="3", font=("Arial", 22), fg="#eeeed5", bg="#7d945d")
    l3.place(x=5, y=565)
    buttons[41] = Button(root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: button_clicked(buttons[41], 41, 3))
    buttons[41].place(x=112.5, y=562.5)
    buttons[42] = Button(root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: button_clicked(buttons[42], 42, 3))
    buttons[42].place(x=225, y=562.5)
    buttons[43] = Button(root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: button_clicked(buttons[43], 43, 3))
    buttons[43].place(x=337.5, y=562.5)
    buttons[44] = Button(root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: button_clicked(buttons[44], 44, 3))
    buttons[44].place(x=450, y=562.5)
    buttons[45] = Button(root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: button_clicked(buttons[45], 45, 3))
    buttons[45].place(x=562.5, y=562.5)
    buttons[46] = Button(root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: button_clicked(buttons[46], 46, 3))
    buttons[46].place(x=675, y=562.5)
    buttons[47] = Button(root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", command=lambda: button_clicked(buttons[47], 47, 3))
    buttons[47].place(x=787.5, y=562.5)

    # Row 2
    buttons[48] = Button(root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", image=white_pawn, command=lambda: button_clicked(buttons[48], 48, 2))
    buttons[48].place(x=0, y=675)
    l2 = Label(text="2", font=("Arial", 22), fg="#7d945d", bg="#eeeed5")
    l2.place(x=5, y=680)
    buttons[49] = Button(root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", image=white_pawn, command=lambda: button_clicked(buttons[49], 49, 2))
    buttons[49].place(x=112.5, y=675)
    buttons[50] = Button(root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", image=white_pawn, command=lambda: button_clicked(buttons[50], 50, 2))
    buttons[50].place(x=225, y=675)
    buttons[51] = Button(root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", image=white_pawn, command=lambda: button_clicked(buttons[51], 51, 2))
    buttons[51].place(x=337.5, y=675)
    buttons[52] = Button(root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", image=white_pawn, command=lambda: button_clicked(buttons[52], 52, 2))
    buttons[52].place(x=450, y=675)
    buttons[53] = Button(root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", image=white_pawn, command=lambda: button_clicked(buttons[53], 53, 2))
    buttons[53].place(x=562.5, y=675)
    buttons[54] = Button(root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", image=white_pawn, command=lambda: button_clicked(buttons[54], 54, 2))
    buttons[54].place(x=675, y=675)
    buttons[55] = Button(root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", image=white_pawn, command=lambda: button_clicked(buttons[55], 55, 2))
    buttons[55].place(x=787.5, y=675)

    # Row 1 has many more labels (for columns)
    buttons[56] = Button(root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", image=white_rook_qs, command=lambda: button_clicked(buttons[56], 56, 1))
    buttons[56].place(x=0, y=787.5)

    l1 = Label(text="1", font=("Arial", 25), fg="#eeeed5", bg="#7d945d")
    l1.place(x=5, y=790)

    la = Label(text="a", font=("Arial", 20), fg="#eeeed5", bg="#7d945d")
    la.place(x=95, y=850)

    buttons[57] = Button(root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", image=white_knight, command=lambda: button_clicked(buttons[57], 57, 1))
    buttons[57].place(x=112.5, y=787.5)

    lb = Label(text="b", font=("Arial", 20), fg="#7d945d", bg="#eeeed5")
    lb.place(x=205, y=850)

    buttons[58] = Button(root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", image=white_bishop, command=lambda: button_clicked(buttons[58], 58, 1))
    buttons[58].place(x=225, y=787.5)

    lc = Label(text="c", font=("Arial", 20), fg="#eeeed5", bg="#7d945d")
    lc.place(x=320, y=850)

    buttons[59] = Button(root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", image=white_queen, command=lambda: button_clicked(buttons[59], 59, 1))
    buttons[59].place(x=337, y=787.5)

    ld = Label(text="d", font=("Arial", 20), fg="#7d945d", bg="#eeeed5")
    ld.place(x=430, y=850)

    buttons[60] = Button(root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", image=white_king, command=lambda: button_clicked(buttons[60], 60, 1))
    buttons[60].place(x=450, y=787.5)

    le = Label(text="e", font=("Arial", 20), fg="#eeeed5", bg="#7d945d")
    le.place(x=545, y=850)

    buttons[61] = Button(root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", image=white_bishop, command=lambda: button_clicked(buttons[61], 61, 1))
    buttons[61].place(x=562.5, y=787.5)

    lf = Label(text="f", font=("Arial", 20), fg="#7d945d", bg="#eeeed5")
    lf.place(x=660, y=850)

    buttons[62] = Button(root, bg="#7d945d", padx=51.5, pady=44.5, activebackground="#B2E77C", image=white_knight, command=lambda: button_clicked(buttons[62], 62, 1))
    buttons[62].place(x=675, y=787.5)

    lg = Label(text="g", font=("Arial", 20), fg="#eeeed5", bg="#7d945d")
    lg.place(x=770, y=850)

    buttons[63] = Button(root, bg="#eeeed5", padx=51.5, pady=44.5, activebackground="#B2E77C", image=white_rook_ks, command=lambda: button_clicked(buttons[63], 63, 1))
    buttons[63].place(x=787.5, y=787.5)

    lh = Label(text="h", font=("Arial", 20), fg="#7d945d", bg="#eeeed5")
    lh.place(x=883, y=850)

    # pawn promotion global variable
    global promotion_buttons
    promotion_buttons = [*range(0, 9, 1)]
    # Pawn promotion buttons - White
    promotion_buttons[0] = Button(root, bg="white", padx=51.5, pady=44.5, activebackground="#B2E77C", image=white_queen, command=lambda: do_white_pawn_promotion(promotion_buttons[0]))
    promotion_buttons[1] = Button(root, bg="white", padx=51.5, pady=44.5, activebackground="#B2E77C", image=white_knight, command=lambda: do_white_pawn_promotion(promotion_buttons[1]))
    promotion_buttons[2] = Button(root, bg="white", padx=51.5, pady=44.5, activebackground="#B2E77C", image=white_rook, command=lambda: do_white_pawn_promotion(promotion_buttons[2]))
    promotion_buttons[3] = Button(root, bg="white", padx=51.5, pady=44.5, activebackground="#B2E77C", image=white_bishop, command=lambda: do_white_pawn_promotion(promotion_buttons[3]))

    # Pawn promotion buttons - black
    promotion_buttons[4] = Button(root, bg="white", padx=51.5, pady=44.5, activebackground="#B2E77C", image=black_queen, command=lambda: do_black_pawn_promotion(promotion_buttons[4]))
    promotion_buttons[5] = Button(root, bg="white", padx=51.5, pady=44.5, activebackground="#B2E77C", image=black_knight, command=lambda: do_black_pawn_promotion(promotion_buttons[5]))
    promotion_buttons[6] = Button(root, bg="white", padx=51.5, pady=44.5, activebackground="#B2E77C", image=black_rook, command=lambda: do_black_pawn_promotion(promotion_buttons[6]))
    promotion_buttons[7] = Button(root, bg="white", padx=51.5, pady=44.5, activebackground="#B2E77C", image=black_bishop, command=lambda: do_black_pawn_promotion(promotion_buttons[7]))

    # White pieces individual lists (based on buttons)
    # pawn
    white_pieces.append(buttons[48]["image"])
    white_p.append(buttons[48]["image"])
    # rook
    white_pieces.append(buttons[56]["image"])
    white_r_qs.append(buttons[56]["image"])
    white_r_ks.append(buttons[63]["image"])
    white_r.append(promotion_buttons[2]["image"])
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

    # Black pieces individual lists (based on buttons)
    # pawn
    black_pieces.append(buttons[8]["image"])
    black_p.append(buttons[8]["image"])
    # rook
    black_pieces.append(buttons[0]["image"])
    black_r_qs.append(buttons[0]["image"])
    black_r_ks.append(buttons[7]["image"])
    black_r.append(promotion_buttons[6]["image"])
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


# create board
board()
# start game sound
# playsound("start.mp3")
# run tkinter program
root.mainloop()
