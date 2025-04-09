import pygame

grid = [None] * 9

def drawGrid():
    pygame.draw.line(screen, RED, (0, 100), (0, 900), 5)
    pygame.draw.line(screen, RED, (900, 100), (900, 900), 5)

    pygame.draw.line(screen, RED, (0, 100), (900, 100), 5)
    pygame.draw.line(screen, RED, (0, 900), (900, 900), 5)

    pygame.draw.line(screen, RED, (300, 100), (300, 900), 5)
    pygame.draw.line(screen, RED, (600, 100), (600, 900), 5)

    pygame.draw.line(screen, RED, (0, 367), (900, 367), 5)
    pygame.draw.line(screen, RED, (0, 634), (900, 634), 5)

def checkPosition(pos):
    if pos[0] > 0 and pos[0] < 267 and pos[1] > 100 and pos[1] < 367:
        return [True, 0, 100]
    if pos[0] > 267 and pos[0] < 534 and pos[1] > 100 and pos[1] < 367:
        return [True, 267, 100]
    if pos[0] > 534 and pos[0] < 900 and pos[1] > 100 and pos[1] < 367:
        return [True, 534, 100]
    
    if pos[0] > 0 and pos[0] < 267 and pos[1] > 367 and pos[1] < 634:
        return [True, 0, 367]
    if pos[0] > 267 and pos[0] < 534 and pos[1] > 367 and pos[1] < 634:
        return [True, 267, 367]
    if pos[0] > 534 and pos[0] < 900 and pos[1] > 367 and pos[1] < 634:
        return [True, 534, 367]

    if pos[0] > 0 and pos[0] < 267 and pos[1] > 634 and pos[1] < 900:
        return [True, 0, 534]
    if pos[0] > 267 and pos[0] < 534 and pos[1] > 634 and pos[1] < 900:
        return [True, 267, 534]
    if pos[0] > 534 and pos[0] < 900 and pos[1] > 634 and pos[1] < 900:
        return [True, 534,534]

    return [False, None, None]

def drawCross(pos_0, pos_1):
    pygame.draw.line(screen, RED, (pos_0 + 25, pos_1 + 25), (pos_0 + 242, pos_1 + 242), 10)
    pygame.draw.line(screen, RED, (pos_0 + 25, pos_1 + 242), (pos_0 + 242, pos_1 + 25), 10)

def drawCircle(pos_0, pos_1):
    pygame.draw.circle(screen, RED, (pos_0 + 133, pos_1 + 133), 50)

def playerMove(move, isValid):
    
    if move == True and isValid == True:
        print("X")
        return [False, True]
    elif move == False and isValid == True:
        print("O")
        return [True, False]
    else:
        return [move, None]
        
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

isCross = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()

            valid, pos_0, pos_1 = checkPosition(pos)
            player, isCross = playerMove(player, valid)

    screen.fill(WHITE)

    drawGrid()
    if isCross:
        drawCross(pos_0, pos_1)
    elif isCross == None:
        pass
    else:
        drawCircle(pos_0, pos_1)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()