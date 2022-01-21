# Checkers-Multiplayer
## Table of contents
* [Goal of the projet](#goal-of-the-projet)
* [Technologies](#technologies)
* [Launching the application](#launching-the-application)
## Goal of the projet:
Application created as a project for a university that manages a database of a company dealing in the cultivation and sale of flowers and seeds. The data exchanged between the client and the server consists of 4 characters. In the case of movement information, the first two characters correspond to the position of the pawn, while the next two refer to the destination to which the user has moved the pawn. In case of disconnection of one of the players, the message "LOST" is sent to the opponent.

Client application:
After selecting the pawn that we plan to make a move, green markings symbolizing the available, correct moves are displayed on the board. We choose the target field on the board, but we can only move our pawns. After
When the move is made, the application waits for the opponent to move. The use of threads keeps the game window active while waiting. If any of the players wins, each of them is presented with information about the victory or defeat.

Server application:
After starting, the server waits for a connection. It connects players in pairs, creating a new thread and sends information about assigning users to the colors they will play. Later on, the server waits for data from one side, starting with the black player, and sends it to the opponent. After one of the players disconnects or wins, the program sends appropriate messages.
## Technologies:
* Python 3.9.1<br>
* pygame 2.0.1<br>
## Launching the application:
In order to start the client, go to the folder containing the main.py file and enter the line: python -u main.py in the terminal. The application uses the pygame library that was used to implement the graphical user interface. Another library thanks to which we can communicate with the server is socket. The server is implemented for the GNU / Linux system. Compile the server.c file:<br>
```
gcc server.c -lpthread -o server
```
and then run it:
```
./server
```
