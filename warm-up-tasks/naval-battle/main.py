import pygame

pygame.init()
pygame.font.init()

""" CONSTANTS """
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)

WIDTH = 1000
HEIGHT = 800
CELL_SIZE = 40

# Шрифты для координат и текста
COORD_FONT = pygame.font.SysFont(None, 24)
TEXT_FONT = pygame.font.SysFont(None, 36)

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

    # Отрисовка собственной доски с кораблями и координатными подписями
    def display(self, offset_x, offset_y):
        # Отрисовка клеток и линий
        for i in range(self.size + 1):
            x = offset_x + i * CELL_SIZE
            pygame.draw.line(screen, BLACK, (x, offset_y), (x, offset_y + self.size * CELL_SIZE))
        for j in range(self.size + 1):
            y = offset_y + j * CELL_SIZE
            pygame.draw.line(screen, BLACK, (offset_x, y), (offset_x + self.size * CELL_SIZE, y))
            
        # Отрисовка клеток с содержимым
        for y in range(self.size):
            for x in range(self.size):
                rect = pygame.Rect(offset_x + x * CELL_SIZE, offset_y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if self.grid[y][x] == 'S':
                    pygame.draw.rect(screen, BLUE, rect)
                else:
                    pygame.draw.rect(screen, WHITE, rect)
                pygame.draw.rect(screen, BLACK, rect, 1)

                if self.grid[y][x] == 'H':
                    pygame.draw.circle(screen, RED, rect.center, CELL_SIZE // 4)
                elif self.grid[y][x] == 'M':
                    pygame.draw.line(screen, (150,150,150), rect.topleft, rect.bottomright, 2)
                    pygame.draw.line(screen, (150,150,150), rect.topright, rect.bottomleft, 2)

        # Отрисовка координат: числа слева и буквы сверху
        for i in range(self.size):
            # Числа (номера строк)
            num_text = COORD_FONT.render(str(i+1), True, BLACK)
            screen.blit(num_text, (offset_x - 25, offset_y + i * CELL_SIZE + CELL_SIZE//3))
            # Буквы (номера столбцов)
            letter = chr(65 + i)  # 65 - ASCII код буквы A
            letter_text = COORD_FONT.render(letter, True, BLACK)
            screen.blit(letter_text, (offset_x + i * CELL_SIZE + CELL_SIZE//3, offset_y - 25))

    # Отрисовка вражеской доски без отображения кораблей, с координатами
    def display_enemy(self, offset_x, offset_y):
        for i in range(self.size + 1):
            x = offset_x + i * CELL_SIZE
            pygame.draw.line(screen, BLACK, (x, offset_y), (x, offset_y + self.size * CELL_SIZE))
        for j in range(self.size + 1):
            y = offset_y + j * CELL_SIZE
            pygame.draw.line(screen, BLACK, (offset_x, y), (offset_x + self.size * CELL_SIZE, y))
            
        for y in range(self.size):
            for x in range(self.size):
                rect = pygame.Rect(offset_x + x * CELL_SIZE, offset_y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if self.grid[y][x] == 'H':
                    pygame.draw.rect(screen, WHITE, rect)
                    pygame.draw.circle(screen, RED, rect.center, CELL_SIZE // 4)
                elif self.grid[y][x] == 'M':
                    pygame.draw.rect(screen, WHITE, rect)
                    pygame.draw.line(screen, (150,150,150), rect.topleft, rect.bottomright, 2)
                    pygame.draw.line(screen, (150,150,150), rect.topright, rect.bottomleft, 2)
                else:
                    pygame.draw.rect(screen, WHITE, rect)
                pygame.draw.rect(screen, BLACK, rect, 1)
                
        # Отрисовка координат
        for i in range(self.size):
            num_text = COORD_FONT.render(str(i+1), True, BLACK)
            screen.blit(num_text, (offset_x - 25, offset_y + i * CELL_SIZE + CELL_SIZE//3))
            letter = chr(65 + i)
            letter_text = COORD_FONT.render(letter, True, BLACK)
            screen.blit(letter_text, (offset_x + i * CELL_SIZE + CELL_SIZE//3, offset_y - 25))

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
        self.board = Board(10)      # Левая (оборонительная) доска
        self.placing_ship_index = 0 # Индекс текущего корабля для размещения
        self.ship_lengths = [4, 3, 3, 2, 2, 2]
        self.placing_direction = "horizontal"
        self.ships = []

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
def getCellUnderMouse(pos, board_offset_x, board_offset_y, cell_size = CELL_SIZE):
    mx, my = pos
    x = (mx - board_offset_x) // cell_size
    y = (my - board_offset_y) // cell_size
    if 0 <= x < 10 and 0 <= y < 10:
        return x, y
    return None

# Отрисовка пустой доски (только линии и координаты) для фазы размещения правой части
def draw_blank_board(offset_x, offset_y):
    for i in range(11):
        x = offset_x + i * CELL_SIZE
        pygame.draw.line(screen, BLACK, (x, offset_y), (x, offset_y + 10 * CELL_SIZE))
    for j in range(11):
        y = offset_y + j * CELL_SIZE
        pygame.draw.line(screen, BLACK, (offset_x, y), (offset_x + 10 * CELL_SIZE, y))
    # Добавляем координаты
    for i in range(10):
        num_text = COORD_FONT.render(str(i+1), True, BLACK)
        screen.blit(num_text, (offset_x - 25, offset_y + i * CELL_SIZE + CELL_SIZE//3))
        letter = chr(65 + i)
        letter_text = COORD_FONT.render(letter, True, BLACK)
        screen.blit(letter_text, (offset_x + i * CELL_SIZE + CELL_SIZE//3, offset_y - 25))

def draw_turn_queue(game):
    queue = game.getTurnQueue()
    base_x = 800
    base_y = 100
    spacing = 60

    title = TEXT_FONT.render("Ход:", True, BLACK)
    screen.blit(title, (base_x, base_y - 40))

    for i, name in enumerate(queue):
        color = GREEN if i == 0 else (150, 150, 150)
        pygame.draw.circle(screen, color, (base_x, base_y + i * spacing + 10), 10)
        text = TEXT_FONT.render(name, True, BLACK)
        screen.blit(text, (base_x + 25, base_y + i * spacing))

""" MAIN CODE """
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Naval Battle Two-Player")

# Создание двух игроков
player1 = Player("Игрок 1")
player2 = Player("Игрок 2")

# Фаза размещения кораблей
phase = "placement"    # Возможные фазы: "placement", "battle"
currentPlacementPlayer = player1

# Создание объекта игры для фазы боя
game = Game(player1, player2)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if phase == "placement" and event.key == pygame.K_r:
                if currentPlacementPlayer.placing_direction == "horizontal":
                    currentPlacementPlayer.placing_direction = "vertical"
                else:
                    currentPlacementPlayer.placing_direction = "horizontal"

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if phase == "placement":
                cell = getCellUnderMouse(mouse_pos, 50, 50)
                if cell:
                    x, y = cell
                    if currentPlacementPlayer.placing_ship_index < len(currentPlacementPlayer.ship_lengths):
                        length = currentPlacementPlayer.ship_lengths[currentPlacementPlayer.placing_ship_index]
                        new_ship = Ship(length)
                        placed = currentPlacementPlayer.board.placeShip(new_ship, x, y, currentPlacementPlayer.placing_direction)
                        if placed:
                            currentPlacementPlayer.ships.append(new_ship)
                            currentPlacementPlayer.placing_ship_index += 1
                            if currentPlacementPlayer.placing_ship_index >= len(currentPlacementPlayer.ship_lengths):
                                if currentPlacementPlayer == player1:
                                    currentPlacementPlayer = player2
                                    print("Теперь очередь Игрока 2 на размещение кораблей")
                                else:
                                    phase = "battle"
                                    game.currentPlayer = player1
                                    game.otherPlayer = player2
                                    print("Все корабли размещены. Начинается фаза боя!")
                        else:
                            print("Невозможно разместить корабль здесь")
            elif phase == "battle":
                cell = getCellUnderMouse(mouse_pos, 550, 50)
                if cell:
                    x, y = cell
                    result = game.playTurn(x, y)
                    if result == "hit":
                        print(f"{game.currentPlayer.name}: Попадание!")
                    elif result == "miss":
                        print(f"{game.currentPlayer.name}: Мимо!")
                        game.switchTurn()
                    elif result == "already":
                        print("Уже стреляли в эту клетку")
                    if game.otherPlayer.allShipSunk():
                        print(f"{game.currentPlayer.name} победил!")
                        running = False

    screen.fill(WHITE)
    if phase == "placement":
        currentPlacementPlayer.board.display(50, 50)
        draw_blank_board(550, 50)
        if currentPlacementPlayer.placing_ship_index < len(currentPlacementPlayer.ship_lengths):
            current_length = currentPlacementPlayer.ship_lengths[currentPlacementPlayer.placing_ship_index]
            text = f"{currentPlacementPlayer.name}: разместите корабль длины {current_length} ({currentPlacementPlayer.placing_direction})"
        else:
            text = f"{currentPlacementPlayer.name}: все корабли размещены"
        txt_surface = TEXT_FONT.render(text, True, BLACK)
        screen.blit(txt_surface, (50, 470))
    elif phase == "battle":
        # Отрисовка собственной доски с координатами слева
        game.currentPlayer.board.display(50, 50)
        # Отрисовка вражеской доски с координатами справа
        game.otherPlayer.board.display_enemy(550, 50)
        text = f"{game.currentPlayer.name}: Выберите клетку на правой доске для атаки"
        txt_surface = TEXT_FONT.render(text, True, BLACK)
        screen.blit(txt_surface, (50, 470))
        draw_turn_queue(game)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
