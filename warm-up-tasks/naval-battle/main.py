import pygame

""" CONSTANTS """
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

WIDTH = 1000
HEIGHT = 800

""" OBJECTS """
class Board:
    def __init__(self, size):
        self.size = size
        self.grid = [[' ' for _ in range(size)] for _ in range(size)]

    def placeShip(self, ship, x, y, direction):

        pass

    def attack(self, x, y):

        pass

    def display(self):
        cell_size = 40  # Размер одной клетки
        offset_x = 50   # Смещение от левого края
        offset_y = 50   # Смещение от верхнего края

        # Вертикальные линии
        for i in range(self.size + 1):
            x = offset_x + i * cell_size
            pygame.draw.line(screen, BLACK, (x, offset_y), (x, offset_y + self.size * cell_size))

        # Горизонтальные линии
        for j in range(self.size + 1):
            y = offset_y + j * cell_size
            pygame.draw.line(screen, BLACK, (offset_x, y), (offset_x + self.size * cell_size, y))


class Ship:
    def __init__(self, length):
        self.length = length
        self.coordinates = []

    def place(self):

        pass

    def hit(self, x, y):

        pass

    def isSunk(self):

        pass

class Player:
    def __init__(self, name):
        self.name = name
        self.board = Board(10)
        self.ships = []

    def place_ships(self):

        pass

    def makeMove(self, x, y):
        
        pass


class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.currentPlayer = player1

        self.board = Board(10)

    def switchTurn(self):
        if self.currentPlayer == self.player1:
            self.currentPlayer = self.player2
        else:
            self.currentPlayer = self.player1
    
    def play(self):
        self.board.display()
        pass

player1 = Player("first")
player2 = Player("second")
    
game = Game(player1, player2)
    

size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Naval Battle")

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(WHITE)

    game.board.display()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()