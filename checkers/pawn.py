from .constants import black, white, gold, field, border, padding
import pygame

class Pawn:
    def __init__(self, row, column, color):
        self.row = row
        self.column = column
        self.color = color
        self.is_king = False
        self.x = 0
        self.y = 0
        self.get_position()

    # funkcja rysująca rozmieszczone pionki
    def draw(self, window):
        radius = field // 2 - padding

        if self.color == white:
            pygame.draw.circle(window, black, (self.x, self.y), radius + border)
        else:
            pygame.draw.circle(window, white, (self.x, self.y), radius + border)

        pygame.draw.circle(window, self.color, (self.x, self.y), radius)

        # oznaczenie króla złotym konturem
        if self.is_king:
            pygame.draw.circle(window, gold, (self.x, self.y), radius + border)
            pygame.draw.circle(window, self.color, (self.x, self.y), radius)

    # obliczenie współrzędnych środka pionka
    def get_position(self):
        self.x = field * self.column + field // 2
        self.y = field * self.row + field // 2

    def move(self, row, column):
        self.row = row
        self.column = column
        self.get_position()