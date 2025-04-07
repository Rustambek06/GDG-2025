import pygame

# Constants
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pygame.init()

screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Tic Tac Toe")

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()