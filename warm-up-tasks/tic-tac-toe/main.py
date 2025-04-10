import pygame

cells = [[None, None, None] for _ in range(9)]

def drawGrid():
    # Вертикальные линии
    pygame.draw.line(screen, RED, (300, 100), (300, 900), 5)
    pygame.draw.line(screen, RED, (600, 100), (600, 900), 5)

    # Горизонтальные линии

    pygame.draw.line(screen, RED, (0, 100), (900, 100), 5)
    pygame.draw.line(screen, RED, (0, 367), (900, 367), 5)
    pygame.draw.line(screen, RED, (0, 634), (900, 634), 5)

def checkPosition(pos, move):
    for i in range(3):
        for j in range(3):
            if (pos[0] > i * 300) and (pos[0] < (i + 1) * 300) and (pos[1] > 100 + j * 267) and (pos[1] < 100 + (j + 1) * 267):
                if move is not None:  # Проверка на допустимость движения
                    cells[i + j * 3][0] = move  # Записываем состояние ячейки
                cells[i + j * 3][1] = i * 300  # x координата
                cells[i + j * 3][2] = 100 + j * 267  # y координата
                return True
    return False


def drawCross(pos_0, pos_1):
    pygame.draw.line(screen, RED, (pos_0 + 25, pos_1 + 25), (pos_0 + 242, pos_1 + 242), 10)
    pygame.draw.line(screen, RED, (pos_0 + 25, pos_1 + 242), (pos_0 + 242, pos_1 + 25), 10)

def drawCircle(pos_0, pos_1):
    pygame.draw.circle(screen, RED, (pos_0 + 133, pos_1 + 133), 50)

def playerMove(move, isValid):
    
    if move == True and isValid == True:
        print("X")
        return False
    elif move == False and isValid == True:
        print("O")
        return True
    else:
        return move
        
# Constants
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

player = True

pygame.init()

screen = pygame.display.set_mode((900, 900))
pygame.display.set_caption("Tic Tac Toe")

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()

            valid = checkPosition(pos, player)
            player = playerMove(player, valid)

    screen.fill(WHITE)

    drawGrid()

    for cell in cells:
        if cell[0]:
            drawCross(cell[1], cell[2])
        elif cell[0] == False:
            drawCircle(cell[1], cell[2])

    pygame.display.flip()
    clock.tick(60)

pygame.quit()