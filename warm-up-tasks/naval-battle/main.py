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
    def __init(self, size):
        self.size = size
        self.grid = [[' ' for _ in range(size)] for _ in range(size)]
    
    def placeShip(self, ship, x, y, direction):

        pass

    def attack(self, x, y):

        pass

    def display(self):
        for row in self.grid:
            print(' '.join(row))


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

    def switchTurn(self):
        if self.currentPlayer == self.player1:
            self.currentPlayer = self.player2
        else:
            self.currentPlayer = self.player1
    
    def play(self):

        pass

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
    pygame.display.flip()

    clock.tick(60)

pygame.quit()