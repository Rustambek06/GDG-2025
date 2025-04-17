import pygame
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
WIDTH = 800
HEIGHT = 600

pygame.init()
pygame.font.init()

class Ball:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.radius = 10
        self.dx = 4
        self.dy = 0  # начальное направление по Y — ноль

    def isBallOut(self):
        if 5 > self.x or self.x > 795:
            self.x = WIDTH // 2
            self.y = HEIGHT // 2
            return True
        return False

    def move(self, direction):
        self.x += self.dx * direction
        self.y += self.dy

        if self.y - self.radius <= 0 or self.y + self.radius >= HEIGHT:
            self.dy *= -1

    def bounceFromPaddle(self, paddle):
        offset = (self.y - paddle.rect.centery) / (paddle.height / 2)
        max_speed = 5
        self.dy = offset * max_speed
        self.dx *= -1

    def getRect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def display(self):
        pygame.draw.circle(screen, RED, (self.x, self.y), self.radius)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 100
        self.speed = 1

        self.rect = pygame.Rect(self.x, abs(self.y - self.height), self.width, self.height)

        pass

    def moveUp(self):
        if self.y > 100:
            self.y -= 10

        pass

    def moveDown(self):
        if self.y < 600:
            self.y += 10

        pass

    def display(self):
        self.rect = pygame.Rect(self.x, abs(self.y - self.height), self.width, self.height)

        pygame.draw.rect(screen, BLACK, self.rect)

class Game:
    def __init__(self):

        pass

    def display(self):

        pass
 
isGameStarted = False
ballDirection = 1
playerTurn = 0

player1 = Player(40, HEIGHT // 2)
player2 = Player(WIDTH - 60, HEIGHT // 2)

ball = Ball()

# Set the width and height of the screen [width, height]
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("Ping-pong")
 
# Loop until the user clicks the close button.
running = True
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# -------- Main Program Loop -----------
while running:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                isGameStarted = True
        
    # --- Game logic should go here
 
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        player2.moveUp()
    if keys[pygame.K_DOWN]:
        player2.moveDown()
    if keys[pygame.K_w]:
        player1.moveUp()
    if keys[pygame.K_s]:
        player1.moveDown()
 
    if player1.rect.colliderect(ball.getRect()):
        ball.bounceFromPaddle(player1)
    if player2.rect.colliderect(ball.getRect()):
        ball.bounceFromPaddle(player2)

    if ball.isBallOut():
        isGameStarted = False
        playerTurn += 1
        if playerTurn == 2:
            playerTurn = 0
            ballDirection *= -1
    else:
        if isGameStarted:
            ball.move(ballDirection)

    # --- Screen-clearing code goes here
 
    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
 
    # If you want a background image, replace this clear with blit'ing the
    # background image.
    screen.fill(WHITE)
 
    # --- Drawing code should go here

    player1.display()
    player2.display()

    ball.display()

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()