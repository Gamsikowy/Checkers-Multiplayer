import pygame
from .constants import  black, brown, beige, rows, field, columns, white
from .pawn import Pawn

class Board:
    def __init__(self):
        self.board = []
        self.black_quantity = self.white_quantity = 12
        self.black_kings = self.white_kings = 0

        self.plan_board()
    
    # rysowanie planszy składajacej się z brązowych i beżowych pól
    def draw_squares(self, window):
        window.fill(brown)
        for row in range(rows):
            for column in range(row % 2, columns, 2):
                pygame.draw.rect(window, beige, (row * field, column * field, field, field))

    # zmiana pozycji na planszy
    def move(self, pawn, row, column):
        self.board[pawn.row][pawn.column], self.board[row][column] = self.board[row][column], self.board[pawn.row][pawn.column]
        pawn.move(row, column)

        # sprawdzenie czy pionek jest królem
        if row == rows - 1 or row == 0:
            pawn.is_king = True

            if pawn.color == black:
                self.black_kings += 1
            else:
                self.white_kings += 1 

    def get_pawn(self, row, column):
        return self.board[row][column]

    # logiczne rozmieszczenie pionków na planszy
    def plan_board(self):
        for row in range(rows):
            self.board.append([])

            for column in range(columns):
                if column % 2 == ((row +  1) % 2):
                    if row <= 2:
                        # umieszczenie białych pionków na górze planszy
                        self.board[row].append(Pawn(row, column, white))
                    elif row >= 5:
                        # umieszczenie czarnych pionków na dole planszy
                        self.board[row].append(Pawn(row, column, black))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
        
    # rysowanie rozmieszczonych pionków
    def draw(self, window):
        self.draw_squares(window)

        for row in range(rows):
            for column in range(columns):
                pawn = self.board[row][column]

                if pawn != 0:
                    pawn.draw(window)

    # rekacja na zbicie pionka
    def remove(self, pawns):
        for pawn in pawns:
            #self.board[pawn.row][pawn.column] = 0

            if pawn != 0:
                self.board[pawn.row][pawn.column] = 0
                if pawn.color == black:
                    self.black_quantity -= 1
                else:
                    self.white_quantity -= 1
    
    def get_winner(self):
        if self.white_quantity <= 0:
            return black
        elif self.black_quantity <= 0:
            return white
        
        return None 
    
    # pobranie zbioru poprawnych ruchów
    def get_valid_moves(self, pawn):
        moves = {}
        row = pawn.row

        # wybór pierwszej kolumny podczas, gdy przesuwamy się w prawą stronę
        start_column_right = pawn.column + 1
        # wybór pierwszej kolumny podczas, gdy przesuwamy się w lewą stronę
        start_column_left = pawn.column - 1

        if pawn.is_king or pawn.color == black:
            start_row = row - 1
            end_row = max(row - 3, -1)
            step = -1

            # aktualizacja słownika zawierającego poprawne ruchy
            moves.update(self._left_analyze(start_row, end_row, step, pawn.color, start_column_left))
            moves.update(self._right_analyze(start_row, end_row, step, pawn.color, start_column_right))

        if pawn.is_king or pawn.color == white:
            start_row = row + 1
            end_row = min(row + 3, rows)
            step = 1

            # aktualizacja słownika zawierającego poprawne ruchy
            moves.update(self._left_analyze(start_row, end_row, step, pawn.color, start_column_left))
            moves.update(self._right_analyze(start_row, end_row, step, pawn.color, start_column_right))
    
        return moves

    # utworzenie zbioru poprawnych ruchów
    def _left_analyze(self, start_row, end_row, step, pawn_color, start_column, jumped_over = []):
        # pole, na które zostanie przesunięty pinek po biciu
        next_field = []
        correct_moves = {}

        for i in range(start_row, end_row, step):
            if start_column < 0:
                # wyjście poza planszę
                break
            
            current_pawn = self.board[i][start_column]

            if current_pawn == 0:
                if jumped_over and not next_field:
                    # brak możliwości bicia, ze względu na niepuste pole, na którym pionek powinien wylądować
                    break
                elif jumped_over:
                    # podwójne bicie
                    correct_moves[(i, start_column)] = next_field + jumped_over
                else:
                    # pojedyńcze bicie
                    correct_moves[(i, start_column)] = next_field
                
                # sprawdzenie czy możliwe jest ponowne przeskoczenie
                if next_field:
                    if step == -1:
                        row = max(i - 3, 0)
                    else:
                        row = min(i + 3, rows)

                    correct_moves.update(self._left_analyze(i + step, row, step, pawn_color, start_column - 1, jumped_over = next_field))
                    correct_moves.update(self._right_analyze(i + step, row, step, pawn_color, start_column + 1, jumped_over = next_field))
                break
            elif current_pawn.color == pawn_color:
                break
            else:
                # jesli na sprawdzanym polu znajduje się pionek przeciwnika istnieje szansa zbicia go,
                # przesuwając się na następne pole
                next_field = [current_pawn]

            start_column -= 1

        return correct_moves

    def _right_analyze(self, start, stop, step, color, start_column, jumped_over = []):
        # pole, na które zostanie przesunięty pinek po biciu
        next_field = []
        correct_moves = {}
        
        for i in range(start, stop, step):
            if start_column >= columns:
                # wyjście poza planszę
                break
            
            current_pawn = self.board[i][start_column]
            if current_pawn == 0:
                if jumped_over and not next_field:
                    # brak możliwości bicia, ze względu na niepuste pole, na którym pionek powinien wylądować
                    break
                elif jumped_over:
                    # podwójne bicie
                    correct_moves[(i, start_column)] = next_field + jumped_over
                else:
                    # pojedyńcze bicie
                    correct_moves[(i, start_column)] = next_field
                
                # sprawdzenie czy możliwe jest ponowne przeskoczenie
                if next_field:
                    if step == -1:
                        row = max(i - 3, 0)
                    else:
                        row = min(i + 3, rows)

                    correct_moves.update(self._left_analyze(i + step, row, step, color, start_column - 1, jumped_over = next_field))
                    correct_moves.update(self._right_analyze(i + step, row, step, color, start_column + 1, jumped_over = next_field))
                break
            elif current_pawn.color == color:
                break
            else:
                # jesli na sprawdzanym polu znajduje się pionek przeciwnika istnieje szansa zbicia go,
                # przesuwając się na następne pole
                next_field = [current_pawn]

            start_column += 1
        
        return correct_moves