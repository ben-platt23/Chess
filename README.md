# Chess - Singleplayer or Online!
### Author: Ben Platt
### Contributors: Mark Ross, Raymond Johnson, Rhoda Asamoah
### *Updated 04/25/2023
### Fully functioning chess game made in python! GUI made using Tkinter. In this program you are able to play chess either singleplayer or online. Note: in order to play online, you must run and connect to Server.py, which is included in this repository.
### An important note: The GUI does not currently work as expected on Mac OS systems. The program has been fully tested and developed for windows machines.

## REQUIREMENTS TO RUN:
### Operating System --> Only works as expected on WINDOWS 10 MACHINES (no Windows 11, mac, linux, etc.)
### Extensions -->
#### GUI - Depending on python version, may not need to separately install tkinter:
#### --pip install tk
#### Sounds:
#### --pip install playsound
#### Images:
#### --pip install PIL
#### NOTE: PIL is a fork of the pillow library, if you cannot run the program correctly due to this import, try installing the pillow library.
#### --pip install pillow

## Online Specific Instructions
1). In order to enable online play, you need to run Server.py. For this program to run correctly, you need to change the server IP address to the IP address of the machine that is running Server.py. This change needs to be done on Server.py and CLient.py. See the below images for where this in the code this needs to be done. The variables are called "host" and "host_server"

![image](https://user-images.githubusercontent.com/86609189/234387116-b2bcdc6e-81fc-4309-8e4c-730e23a669d0.png)

![image](https://user-images.githubusercontent.com/86609189/234387176-728a499f-a59a-4440-8961-a2d0cd786f43.png)


2). Make sure that port 50000 is open on your device. If it is in use, the game will raise an error.

3). After running the program, enter an alias that can be viewed by other ciients in the server.

4). Simply follow the instructions that are printed in the console in order to be matched up with another client for a game.

5). After successfully matching with another client and choosing which color pieces, the GUI will launch and the game will begin. Time usage for white starts after both players have "Readied up"


## Singleplayer Specific Instructions
1). There is no need to run Server.py in order to play the game in singleplayer mode. Simply reply "N" when the program asks you if you would like to play online.

2). The GUI will launch itself after stating "N" in upper or lower case.


## General Game Instructions:
#### This game was created using an array of 64 buttons that were placed and labeled to look and feel exactly like a chess board.
#### -white pieces move first, then black
#### -press the button for the piece that you want to move, then press the button for the square that you want to move the piece to
#### -Turns are controlled automatically by the program, users should keep track of whose turn it is
#### -If the first button pressed is empty, nothing will happen and the user must select a piece to move. If the move is not defined as a legal move for the piece, nothing will happen and the user must select the piece and try again.
#### -If the move would place the current teams king into check, an error window will popup and the current team will have to input a move that doesn't put their king into check.
#### -If no legal move can be found, then the team currently in check has been mated and loses.


## Features not included (for simplicities sake):
#### -En passant move for pawns
#### -Stalemate match result 
#### -Checkmate (Although you should quickly figure out if you are in checkmate. The game won't let you proceed)
#### -Restart game (Since no end of game conditions are included)

## Game Demonstration
### Valid and Invalid Piece Movement
![ChessFirst](https://user-images.githubusercontent.com/86609189/172069907-03a3f007-5be7-43b2-9b41-8c40f10b4a44.gif)

### Putting the king into check. Cannot make illegal moves when in check.
![ChessSecond](https://user-images.githubusercontent.com/86609189/172070071-7ef07fe8-4303-40ea-877b-813624ee03d5.gif)
