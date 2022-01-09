import pygame
from .constants import black, white, green, field
from checkers.board import Board

class Game:
    def __init__(self, window):
        self._init()
        self.window = window

    def _init(self):
        self.chosen = None
        self.board = Board()
        self.player = None
        self.turn = black
        self.from_row = None
        self.from_column = None
        self.valid_moves = {}
    
    def update(self):
        self.board.draw(self.window)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    # wybór pola
    # funkcja zwraca false jeśli wybierzemy puste pole lub pionek przeciwnika oraz true, gdy wybierzemy naszego pionka
    def choose(self, row, column, network):
        if self.chosen:
            is_valid = self._move_pawn(row, column, network)

            if not is_valid:
                self.chosen = None
                self.choose(row, column, network)

        pawn = self.board.get_pawn(row, column)

        if pawn != 0 and pawn.color == self.turn:
            self.chosen = pawn
            self.from_row = self.chosen.row
            self.from_column = self.chosen.column
            self.valid_moves = self.board.get_valid_moves(pawn)
            return True
       
        return False

    # funkcja przesuwa pionek lub zwraca false, gdy pożądany ruch jest niepoprawny
    def _move_pawn(self, row, column, network):
        pawn = self.board.get_pawn(row, column)

        if pawn == 0 and self.chosen and (row, column) in self.valid_moves:
            self.board.move(self.chosen, row, column)
            jumped_over = self.valid_moves[(row, column)]

            # wykrycie zbicia pionka
            if jumped_over:
                self.board.remove(jumped_over)
            
            # warunek zapobiegajacy ponownemu przeslaniu tej samej informacji o polozeniu pionka 
            if self.player == self.turn:
                # wyslanie informacji o ruchu
                print("ruch z", str(self.from_row), str(self.from_column))
                print("ruch na", str(row), str(column))
                network.send(str(self.from_row) + str(self.from_column) + str(row) + str(column))

            # zmiana tury
            if self.turn == black:
                self.turn = white
            else:
                self.turn = black

            self.valid_moves = {}
        else:
            return False

        return True

    # oznaczenie poprawnych ruchów zielonym kolorem
    def draw_valid_moves(self, moves):
        for move in moves:
            mark_radius = 8
            row, column = move
            pygame.draw.circle(self.window, green, (column * field + field // 2, row * field + field // 2), mark_radius)

    def get_winner_from_board(self):
        return self.board.get_winner()

    def reset(self):
        self._init()