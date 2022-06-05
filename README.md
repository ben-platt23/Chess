# Chess
### Author Ben Platt
### *Updated 12/23/2021
### Fully functioning chess game made in python! GUI made using Tkinter. Note that this project is not perfect by any means and may still include bugs (either weird visuals or pieces not moving like they should. Although I think i squashed most of them). But this was just meant as a fun winter break project so I could learn more python.

### Game Demonstration with piece movement and capture
![ChessFirst](https://user-images.githubusercontent.com/86609189/172069907-03a3f007-5be7-43b2-9b41-8c40f10b4a44.gif)

### Putting the king into check. Cannot make illegal moves when in check.
![ChessSecond](https://user-images.githubusercontent.com/86609189/172070071-7ef07fe8-4303-40ea-877b-813624ee03d5.gif)

&emsp;
#### Extensions required to run in python:
#### GUI:
#### --pip install tk
#### Sounds:
#### --pip install playsound
#### Images:
#### --pip install PIL

#### Instructions:
#### This game was created using an array of 64 buttons that were placed and labeled to look and feel exactly like a chess board.
#### -white pieces move first, then black
#### -press the button for the piece that you want to move, then press the button for the square that you want to move the piece to
#### -Turns are controlled automatically by the program, users should keep track of whose turn it is
#### -If the first button pressed is empty, nothing will happen and the user must select a piece to move. If the move is not defined as a legal move for the piece, nothing will happen and the user must select the piece and try again.
#### -If the move would place the current teams king into check, an error window will popup and the current team will have to input a move that doesn't put their king into check.
#### -If no legal move can be found, then the team currently in check has been mated and loses.

### Also all the code was written in the same file because tkinter is weird with having different files/classes. To compensate I tried to organize the sections better.
### Features not included (for simplicities sake):
#### -En passant move for pawns
#### -Stalemate match result 
#### -Checkmate (Although you should quickly figure out if you are in checkmate. The game won't let you proceed)
#### -Restart game (Since no end of game conditions are included)
