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

font = pygame.font.SysFont('Arial', 40)

class Ball:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.radius = 10
        self.dx = 4
        self.dy = 0  # начальное направление по Y — ноль

    def isBallOut(self):
        if 5 > self.x or self.x > 795:
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

    def moveUp(self):
        if self.y > 100:
            self.y -= 10

    def moveDown(self):
        if self.y < 600:
            self.y += 10

    def display(self):
        self.rect = pygame.Rect(self.x, abs(self.y - self.height), self.width, self.height)
        pygame.draw.rect(screen, BLACK, self.rect)

# ИНИЦИАЛИЗАЦИЯ
isGameStarted = False
ballDirection = 1
playerTurn = 0
gameOver = False

score1 = 0
score2 = 0

player1 = Player(40, HEIGHT // 2)
player2 = Player(WIDTH - 60, HEIGHT // 2)
ball = Ball()

size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Ping-pong")
clock = pygame.time.Clock()

# -------- Main Program Loop -----------
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if not gameOver:
                if event.key == pygame.K_SPACE:
                    isGameStarted = True
            else:
                if event.key == pygame.K_r:
                    # Сброс игры
                    gameOver = False
                    score1 = 0
                    score2 = 0
                    ballDirection = 1
                    playerTurn = 0
                    isGameStarted = False
                    ball.x = WIDTH // 2
                    ball.y = HEIGHT // 2

    keys = pygame.key.get_pressed()

    if not gameOver:
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
            if ballDirection < 0:
                ballDirection -= 0.1
            else:
                ballDirection += 0.1

        if player2.rect.colliderect(ball.getRect()):
            ball.bounceFromPaddle(player2)
            if ballDirection < 0:
                ballDirection -= 0.1
            else:
                ballDirection += 0.1

        if ball.isBallOut():
            if ball.x < WIDTH // 2:
                score2 += 1
            else:
                score1 += 1

            ball.x = WIDTH // 2
            ball.y = HEIGHT // 2

            if ballDirection < 0:
                ballDirection = -1
            else:
                ballDirection = 1


            isGameStarted = False
            playerTurn += 1
            if playerTurn == 2:
                playerTurn = 0
                ballDirection *= -1

            if score1 == 5 or score2 == 5:
                gameOver = True
        else:
            if isGameStarted:
                ball.move(ballDirection)

    screen.fill(WHITE)

    if not gameOver:
        player1.display()
        player2.display()
        ball.display()

        # Отображение счета
        score_text = font.render(f"{score1} : {score2}", True, BLACK)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))
    else:
        # Сцена Game Over
        if score1 == 5:
            winner_text = font.render("Player 1 wins!", True, GREEN)
        else:
            winner_text = font.render("Player 2 wins!", True, GREEN)
        screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - 50))

        restart_text = font.render("Press 'R' to Restart", True, BLACK)
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
