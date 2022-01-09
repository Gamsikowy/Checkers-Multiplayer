import pygame
from checkers.network import Network
from checkers.game import Game
from checkers.constants import width, height, field
from checkers.constants import black, white

width = 600
height = 600
rows = 8
columns = 8
field = width // columns
crown_width = 44
crown_height = 25
fps = 60

window = pygame.display.set_mode((width, height))

pygame.display.set_caption('Computer Networks Project')

def mouse_to_field(position):
    x, y = position
    row = y // field
    column = x // field
    return row, column

def main():
    running = True
    result = None
    clock = pygame.time.Clock()
    game = Game(window)
    network = Network()

    if network.id == 'BBBB':
        game.player = black
    else:
        game.player = white

    while running:
        clock.tick(fps)

        if game.board.get_winner() != None:
            result = game.board.get_winner()
            if result == "#ffffff":
                print("The white player is the winner")
            else:
                print("The black player is the winner")

            # running = False
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
                opponent_move = network.receive(4)
                print(opponent_move)

                if opponent_move == 'LOST':
                    if network.id == 'BBBB':
                        game.board.white_quantity = 0
                    else:
                        game.board.black_quantity = 0
                    break
                else:
                    print("Moves", opponent_move[0:1], opponent_move[1:2], opponent_move[2:3], opponent_move[3:4])

                    game.choose(int(opponent_move[0:1]), int(opponent_move[1:2]), network)
                    game.choose(int(opponent_move[2:3]), int(opponent_move[3:4]), network)

        game.update()

    pygame.quit()

main()