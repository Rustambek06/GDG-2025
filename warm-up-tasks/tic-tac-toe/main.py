import pygame

# Constants
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pygame.init()

screen = pygame.display.set_mode((900, 900))
pygame.display.set_caption("Tic Tac Toe")

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    pygame.draw.line(screen, RED, (300, 100), (300, 900), 5)
    pygame.draw.line(screen, RED, (600, 100), (600, 900), 5)

    pygame.draw.line(screen, RED, (0, 367), (900, 367), 5)
    pygame.draw.line(screen, RED, (0, 634), (900, 634), 5)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()