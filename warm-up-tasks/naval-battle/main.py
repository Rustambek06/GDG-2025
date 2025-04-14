import pygame

pygame.init()
pygame.font.init()


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

    def attack(self, x, y):
        if self.grid[y][x] == 'H' or self.grid[y][x] == 'M':
            return "already"
        if self.grid[y][x] == 'S':
            self.grid[y][x] = 'H'
            return "hit"
        elif self.grid[y][x] == ' ':
            self.grid[y][x] = 'M'
            return "miss"

    def display(self):
        cell_size = 40
        offset_x = 50
        offset_y = 50

        for i in range(self.size + 1):
            x = offset_x + i * cell_size
            pygame.draw.line(screen, BLACK, (x, offset_y), (x, offset_y + self.size * cell_size))

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

    def hit(self, x, y):
        if (x, y) in self.coordinates:
            self.coordinates.remove((x, y))
            return True
        return False

    def isSunk(self):
        return len(self.coordinates) == 0

class Player:
    def __init__(self, name):
        self.name = name
        self.board = Board(10)
        self.placing_ship_index = 0
        self.ship_lengths = [4, 3, 3, 2, 2, 2]
        self.placing_direction = "horizontal"
        self.ships = []

    def place_ships(self):
        ship1 = Ship(3)
        placed = self.board.placeShip(ship1, 0, 0, "vertical")
        if placed:
            self.ships.append(ship1)
        else:
            print("Placing error")

    def allShipSunk(self):
        for ship in self.ships:
            if not ship.isSunk():
                return False
        return True

    def makeMove(self, opponent, x, y):
        result = opponent.board.attack(x, y)
        if result == "hit":
            for ship in opponent.ships:
                if ship.hit(x, y):
                    if ship.isSunk():
                        print("Корабль потоплен!")
                    return "hit"
        return result

class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.currentPlayer = player1
        self.otherPlayer = player2

    def switchTurn(self):
        self.currentPlayer, self.otherPlayer = self.otherPlayer, self.currentPlayer

    def playTurn(self, x, y):
        return self.currentPlayer.makeMove(self.otherPlayer, x, y)
    
    def getTurnQueue(self):
        return [self.currentPlayer.name, self.otherPlayer.name]

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
    offset_x = 550
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

def draw_turn_queue(game):
    queue = game.getTurnQueue()
    base_x = 800
    base_y = 100
    spacing = 60

    font = pygame.font.SysFont(None, 32)
    title = font.render("Ход:", True, BLACK)
    screen.blit(title, (base_x, base_y - 40))

    for i, name in enumerate(queue):
        color = GREEN if i == 0 else (150, 150, 150)
        pygame.draw.circle(screen, color, (base_x, base_y + i * spacing + 10), 10)
        text = font.render(name, True, BLACK)
        screen.blit(text, (base_x + 25, base_y + i * spacing))

""" MAIN CODE """
player1 = Player("first")
player2 = Player("second")

player1.place_ships()
player2.place_ships()

game = Game(player1, player2)

size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Naval Battle")

placing_ships = True
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                if player1.placing_direction == "horizontal":
                    player1.placing_direction = "vertical"
                else:
                    player1.placing_direction = "horizontal"

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()

            if placing_ships:
                cell = getCellUnderMouse(mouse_pos, 50, 50)
                if cell:
                    x, y = cell
                    length = player1.ship_lengths[player1.placing_ship_index]
                    new_ship = Ship(length)
                    placed = player1.board.placeShip(new_ship, x, y, player1.placing_direction)
                    if placed:
                        player1.ships.append(new_ship)
                        player1.placing_ship_index += 1
                        if player1.placing_ship_index >= len(player1.ship_lengths):
                            placing_ships = False
                    else:
                        print("Невозможно разместить корабль здесь")

            else:
                cell = getCellUnderMouse(mouse_pos, 550, 50)
                if cell:
                    x, y = cell
                    result = game.playTurn(x, y)
                    if result == "hit":
                        print("Попадание!")
                    elif result == "miss":
                        print("Мимо")
                        game.switchTurn()
                    elif result == "already":
                        print("Уже стреляли")
                    
                    if game.otherPlayer.allShipSunk():
                        print(f"{game.currentPlayer.name} победил!")
                        running = False

    screen.fill(WHITE)
    player1.board.display()
    draw_enemy_board(player2.board)

    font = pygame.font.SysFont(None, 36)
    if placing_ships:
        current_length = player1.ship_lengths[player1.placing_ship_index]
        text = f"Place a ship with length {current_length} ({player1.placing_direction})"
    else:
        text = f"{game.currentPlayer.name}'s turn. Click to attack"
    txt_surface = font.render(text, True, BLACK)
    screen.blit(txt_surface, (50, 470))

    draw_turn_queue(game)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
