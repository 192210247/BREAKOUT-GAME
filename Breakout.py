import pygame
import random
pygame.init()

WIDTH = 700
HEIGHT = 700
FPS = 60 


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🎮 BREAKOUT GAME 🎮")
clock = pygame.time.Clock()

class Paddle():
    def __init__(self):
        self.width = 120
        self.height = 20
        self.x = WIDTH//2 - self.width//2
        self.y = HEIGHT - 50  
        self.speed = 8
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self):
        pygame.draw.rect(win, WHITE, self.rect)
        pygame.draw.rect(win, BLUE, self.rect, 3) 
    
    def move(self):
        keys = pygame.key.get_pressed()
        # Move left
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        # Move right
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

class Ball():
    def __init__(self):
        self.radius = 12
        self.x = WIDTH // 2
        self.y = HEIGHT - 100  
        self.speed_x = random.choice([-5, 5])
        self.speed_y = -5 
    
    def draw(self):
        pygame.draw.circle(win, WHITE, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(win, RED, (int(self.x), int(self.y)), self.radius - 2)
    
    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        
    
        if self.x <= self.radius or self.x >= WIDTH - self.radius:
            self.speed_x = -self.speed_x
        

        if self.y <= self.radius:
            self.speed_y = -self.speed_y

class Brick():
    def __init__(self, x, y):
        self.width = 65
        self.height = 30
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.destroyed = False
    
    def draw(self):
        if not self.destroyed:

            pygame.draw.rect(win, ORANGE, self.rect)
            pygame.draw.rect(win, WHITE, self.rect, 2) 

def create_bricks():
    bricks = []
    rows = 5
    cols = 10
    
    for row in range(rows):
        for col in range(cols):
            x = col * 70 + 10
            y = row * 40 + 80
            brick = Brick(x, y)
            bricks.append(brick)
    
    return bricks

def check_ball_paddle_collision(ball, paddle):

    if (ball.y + ball.radius >= paddle.rect.y and 
        ball.x >= paddle.rect.x and 
        ball.x <= paddle.rect.x + paddle.rect.width and
        ball.speed_y > 0):  
        ball.speed_y = -ball.speed_y
        return True
    return False

def check_ball_brick_collision(ball, bricks):
    global score
    for brick in bricks:
        if not brick.destroyed:

            if (ball.x + ball.radius > brick.rect.left and 
                ball.x - ball.radius < brick.rect.right and
                ball.y + ball.radius > brick.rect.top and 
                ball.y - ball.radius < brick.rect.bottom):
                
                brick.destroyed = True
                ball.speed_y = -ball.speed_y
                score += 10
                break

def check_win(bricks):
    return all(brick.destroyed for brick in bricks)

def draw_game_over():
    font = pygame.font.Font(None, 72)
    text = font.render("GAME OVER!", True, RED)
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
    win.blit(text, text_rect)
    
    restart_text = font.render("Press SPACE to Restart", True, WHITE)
    restart_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
    win.blit(restart_text, restart_rect)

def draw_you_win():
    font = pygame.font.Font(None, 72)
    text = font.render("YOU WIN!", True, GREEN)
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
    win.blit(text, text_rect)
    
    restart_text = font.render("Press SPACE to Play Again", True, WHITE)
    restart_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
    win.blit(restart_text, restart_rect)

def reset_game():
    global paddle, ball, bricks, score, game_over, you_win
    paddle = Paddle()
    ball = Ball()
    bricks = create_bricks()
    score = 0
    game_over = False
    you_win = False

paddle = Paddle()
ball = Ball()
bricks = create_bricks()
score = 0
game_over = False
you_win = False

run = True
while run:
    clock.tick(FPS)
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and (game_over or you_win):
                reset_game()
    
    if not game_over and not you_win:
     
        paddle.move()
        
       
        ball.move()
        

        check_ball_paddle_collision(ball, paddle)
        

        check_ball_brick_collision(ball, bricks)
        

        if ball.y > HEIGHT:
            game_over = True

        if check_win(bricks):
            you_win = True
    
    win.fill(BLACK)
    
    if not game_over and not you_win:

        paddle.draw()
        ball.draw()
        
        for brick in bricks:
            brick.draw()
        
        font = pygame.font.Font(None, 48)
        score_text = font.render(f"SCORE: {score}", True, WHITE)
        win.blit(score_text, (20, 20))
        

        instruction_font = pygame.font.Font(None, 36)
        instruction_text = instruction_font.render("Use LEFT/RIGHT arrows to move paddle", True, YELLOW)
        win.blit(instruction_text, (WIDTH//2 - instruction_text.get_width()//2, HEIGHT - 25))
    
    elif game_over:
        draw_game_over()
    
    elif you_win:
        draw_you_win()
    
    pygame.display.update()

pygame.quit()