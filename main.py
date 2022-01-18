from threading import Thread
import pygame
from checkers.network import Network
from checkers.game import Game
from checkers.constants import width, height, field, black, white, fps

window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Computer Networks Project')
running = True

def mouse_to_field(position):
    x, y = position
    row = y // field
    column = x // field
    return row, column

def print_result(game):
    if game.board.get_winner() == white:
        print("The white player is the winner")
    else:
        print("The black player is the winner")

# odczytywanie informacji z serwera przez wątek
def answer_management(game, network):        
    try:
        opponent_move = network.receive(4)

        if opponent_move == 'LOST':
            if network.id == 'BBBB':
                game.board.white_quantity = 0
            else:
                game.board.black_quantity = 0

            global running
            running = False
            print_result(game)
            global user_informed
            user_informed = True
        else:
            #print("Moves", opponent_move[0:1], opponent_move[1:2], opponent_move[2:3], opponent_move[3:4])
            game.choose(int(opponent_move[0:1]), int(opponent_move[1:2]), network)
            game.choose(int(opponent_move[2:3]), int(opponent_move[3:4]), network)

    except:
        pass

def main():
    global running
    global user_informed
    clock = pygame.time.Clock()
    game = Game(window)
    game.update()
    network = Network()

    if network.id == 'BBBB':
        game.player = black
    else:
        game.player = white

    while running:
        clock.tick(fps)

        if game.board.get_winner() != None and not user_informed:
            print_result(game)
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if game.player == game.turn:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    row, column = mouse_to_field(position)
                    game.choose(row, column, network)
            else:
                try:
                    thread = Thread(target = answer_management, args = (game, network))
                    thread.daemon = True
                    thread.start()
                except:
                    pass

        game.update()

    pygame.quit()
    try:
        network.client.shutdown()
        network.client.close()
    except:
        pass

main()