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
        return True
    if pos[0] > 267 and pos[0] < 534 and pos[1] > 100 and pos[1] < 367:
        return True
    if pos[0] > 534 and pos[0] < 900 and pos[1] > 100 and pos[1] < 367:
        return True
    
    if pos[0] > 0 and pos[0] < 267 and pos[1] > 367 and pos[1] < 634:
        return True
    if pos[0] > 267 and pos[0] < 534 and pos[1] > 367 and pos[1] < 634:
        return True
    if pos[0] > 534 and pos[0] < 900 and pos[1] > 367 and pos[1] < 634:
        return True

    if pos[0] > 0 and pos[0] < 267 and pos[1] > 634 and pos[1] < 900:
        return True
    if pos[0] > 267 and pos[0] < 534 and pos[1] > 634 and pos[1] < 900:
        return True
    if pos[0] > 534 and pos[0] < 900 and pos[1] > 634 and pos[1] < 900:
        return True   

def playerMove(move, isCorrect):
    if move and isCorrect:
        print("X")
    elif not move and isCorrect:
        print("O")
        
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

            playerMove(player, checkPosition(pos))
            player = not player

    screen.fill(WHITE)

    drawGrid()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()