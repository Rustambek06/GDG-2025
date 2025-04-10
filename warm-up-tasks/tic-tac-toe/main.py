import pygame

cells = [[None, None, None] for _ in range(9)]

def checkForWinner():
    
    wins = [
        [0, 1, 2],  # первая строка
        [3, 4, 5],  # вторая строка
        [6, 7, 8],  # третья строка
        [0, 3, 6],  # первый столбец
        [1, 4, 7],  # второй столбец
        [2, 5, 8],  # третий столбец
        [0, 4, 8],  # диагональ \
        [2, 4, 6]   # диагональ /
    ]
    
    for a, b, c in wins:
        if cells[a][0] != None and cells[b][0] != None and cells[c][0] != None:  # все заняты
            if cells[a][0] == cells[b][0] == cells[c][0]:
                print(cells[a][0])
                return cells[a][0]  
    
    return None 

def checkForDraw():
    draw = True
    for cell in cells:
        if cell[0] == None:
            draw = False
            return False

    if draw:
        return True

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
                if move is not None and cells[i + j * 3][0] is None:  # Проверка на допустимость движения
                    cells[i + j * 3][0] = move  # Записываем состояние ячейки
                else:
                    return False
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

def drawPlayAgain():
    pygame.draw.rect(screen, GREEN, (25, 25, 190, 50), 5)
    txtsurf = font.render("Play again", True, RED)
    screen.blit(txtsurf, (120 - txtsurf.get_width() // 2, 50 - txtsurf.get_height() // 2))

def playAgain():
    return [
    [[None, None, None] for _ in range(9)],
    True,
    None,
    False]

    pass
# Constants
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

player = True
isWinner = None
isGameOver = False


pygame.init()

screen = pygame.display.set_mode((900, 900))
pygame.display.set_caption("Tic Tac Toe")

fontButton = pygame.font.SysFont(None, 16)
font = pygame.font.SysFont(None, 48)
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if isWinner == True:
            print("X is winner")
            isGameOver = True
        elif isWinner == False:
            print("O is winner")
            isGameOver = True
        else:
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                if pos[0] > 25 and pos[1] > 25 and pos[0] < 215 and pos[1] < 75:
                    cells, player, isWinner, isGameOver = playAgain()
                else:
                    valid = checkPosition(pos, player)
                    player = playerMove(player, valid)

    screen.fill(WHITE)

    drawGrid()
    drawPlayAgain()

    for cell in cells:
        if cell[0] == True:
            drawCross(cell[1], cell[2])
        elif cell[0] == False:
            drawCircle(cell[1], cell[2])

    if isGameOver:
        if isWinner:
            txtsurf = font.render("Crosses win!", True, RED)
            screen.blit(txtsurf,(450 - txtsurf.get_width() // 2, 50 - txtsurf.get_height() // 2))
        else:
            txtsurf = font.render("Noughts win!", True, RED)
            screen.blit(txtsurf,(450 - txtsurf.get_width() // 2, 50 - txtsurf.get_height() // 2))
    else:
        if checkForDraw():
            txtsurf = font.render("Draw!", True, RED)
            screen.blit(txtsurf,(450 - txtsurf.get_width() // 2, 50 - txtsurf.get_height() // 2))
        else:
            isWinner = checkForWinner()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()