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
        if direction == "horizontal":
            if x + ship.length > self.size:
                return False
            for i in range(ship.length):
                if self.grid[y][x + i] != ' ':
                    return False
            for i in range(ship.length):
                self.grid[y][x + i] = 'S'
                ship.coordinates.append((x + i, y))
        elif direction == "vertical":
            if y + ship.length > self.size:
                return False
            for i in range(ship.length):
                if self.grid[y + i][x] != ' ':
                    return False
            for i in range(ship.length):
                self.grid[y + i][x] = 'S'
                ship.coordinates.append((x, y + i))
        return True

        pass

    def attack(self, x, y):
        if self.grid[y][x] == 'S':
            self.grid[y][x] = 'H'
            return True
        elif self.grid[y][x] == ' ':
            self.grid[y][x] = 'M'
            return False
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

        for y in range(self.size):
            for x in range(self.size):
                rect = pygame.Rect(offset_x + x * cell_size, offset_y + y * cell_size, cell_size, cell_size)

                if self.grid[y][x] == 'S':
                    pygame.draw.rect(screen, BLUE, rect)
                else:
                    pygame.draw.rect(screen, WHITE, rect)
                
                pygame.draw.rect(screen, BLACK, rect, 1)

                if self.grid[y][x] == 'H':
                    pygame.draw.circle(screen, RED, 
                                       (offset_x + x * cell_size + cell_size // 2, 
                                       offset_y + y * cell_size + cell_size // 2),
                                       cell_size // 4) 

                elif self.grid[y][x] == 'M':
                    cx = offset_x + x * cell_size
                    cy = offset_y + y * cell_size
                    pygame.draw.line(screen, (150, 150, 150), (cx, cy), (cx + cell_size, cy + cell_size), 2)
                    pygame.draw.line(screen, (150, 150, 150), (cx + cell_size, cy), (cx, cy + cell_size), 2)


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
        self.placing_ship_index = 0
        self.ship_lengths = [4, 3, 3, 2, 2, 1, 1, 1, 1]
        self.placing_direction = "horizontal"
        self.ships = []

    def place_ships(self):
        ship1 = Ship(3)
        placed = self.board.placeShip(ship1, 0, 0, "vertical")
        if placed:
            self.ships.append(ship1)
        else:
            print("Placing error")
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

""" FUNCTIONS """
def getCellUnderMouse(pos, board_offset_x, board_offset_y, cell_size = 40):
    mx, my = pos
    x = (mx - board_offset_x) // cell_size
    y = (my - board_offset_y) // cell_size

    if 0 <= x < 10 and 0 <= y < 10:
        return x, y
    return None

def draw_enemy_board(board):
    cell_size = 40
    offset_x = 550  # правая доска
    offset_y = 50

    for y in range(board.size):
        for x in range(board.size):
            rect = pygame.Rect(offset_x + x * cell_size, offset_y + y * cell_size, cell_size, cell_size)

            if board.grid[y][x] == 'H':
                pygame.draw.rect(screen, WHITE, rect)
                pygame.draw.circle(screen, RED, rect.center, cell_size // 4)
            elif board.grid[y][x] == 'M':
                pygame.draw.rect(screen, WHITE, rect)
                pygame.draw.line(screen, (150,150,150), rect.topleft, rect.bottomright, 2)
                pygame.draw.line(screen, (150,150,150), rect.topright, rect.bottomleft, 2)
            else:
                pygame.draw.rect(screen, WHITE, rect)

            pygame.draw.rect(screen, BLACK, rect, 1)


player1 = Player("first")
player2 = Player("second")

player1.place_ships()

game = Game(player1, player2)

player2.board.grid[1][1] = 'S'
player2.board.grid[2][2] = 'S'


size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Naval Battle")

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            cell = getCellUnderMouse(pos, 550, 50)

            if cell:
                x, y = cell
                print(f"Attack to ({x}, {y})")
                hit = player2.board.attack(x,y)
                if hit is True:
                    print("Hit")
                elif hit is False:
                    print("Miss")
                else:
                    print("Already attacked")
    
    screen.fill(WHITE)

    player1.board.display()
    draw_enemy_board(player2.board)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()