import pygame
from pygame.locals import *
from enum import IntEnum

# color rgb codes
BLACK = (0,0,0)
DODGER_BLUE = (57, 137, 249)
BLUE_ZODIAC = (14, 34, 77)
WHITE = (255,255,255)

# screen dimensions
WIDTH = 800
HEIGHT = 600
BORDER_THICKNESS = 10

# font selection
FONT = 'futura'
FONT_SIZE = 80

# frames per second
FPS = 24

"""
X-direction enumerators
"""
class XDirection(IntEnum):
    NONE = 0
    FORWARD = 1
    BACKWARD = -1

"""
Y-direction enumerators
"""
class YDirection(IntEnum):
    NONE = 0
    UPWARD = -1
    DOWNWARD = 1

"""
Paddle class
"""
class Paddle:
    def __init__(self, screen, x, y, width, height, velocity, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height 
        self.velocity = velocity 
        self.color = color
        self.score = 0
        self.paddle_obj = Rect(x, y, width, height)
        self.paddle_drawing = pygame.draw.rect(screen, self.color, self.paddle_obj)

    def display(self, screen):
        self.paddle_drawing = pygame.draw.rect(screen, self.color, self.paddle_obj)

    def move(self, dir):
        # move the paddle in the desired direction
        # dir = 0: no movement
        # dir = 1: move down
        # dir = -1: move up
        self.y += self.velocity * dir

        # handle out of bounds situations
        # 1/ hitting the bottom border
        if self.y <= BORDER_THICKNESS: 
            self.y = BORDER_THICKNESS
        # 2/ hitting the top border
        if self.y + self.height > HEIGHT + BORDER_THICKNESS:
            self.y = HEIGHT + BORDER_THICKNESS - self.height

        # update the paddle position
        self.paddle_obj = Rect(self.x, self.y, self.width, self.height)

    def display_score(self, screen, x, y, score, font_color):
        self.score = score
        myfont = pygame.font.SysFont(FONT, FONT_SIZE)
        score_txt = myfont.render("{:02d}".format(score), 1, font_color)
        screen.blit(score_txt, (x,y))

    def get_score(self):
        return self.score
    
    def get_paddle(self):
        return self.paddle_obj

"""
Ball class
"""
class Ball:
    def __init__(self, screen, x, y, radius, velocity, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.velocity = velocity
        self.color = color 
        self.xDir = int(XDirection['FORWARD'])
        self.yDir = int(YDirection['DOWNWARD'])
        self.score_goal = 0
        self.center = (x, y)
        self.ball = pygame.draw.circle(screen, self.color, self.center, self.radius)

    def display(self, screen):
        self.ball = pygame.draw.circle(screen, self.color, self.center, self.radius)

    def move(self):
        # move the ball in the desired direction
        self.x += self.velocity * self.xDir
        self.y += self.velocity * self.yDir

        # handle out of bounds situations
        # note: x and y are the center of the ball but they don't hit the borders
        # therefore, we must account for the radius of the ball
        # 1/ hitting the bottom border
        if self.y - self.radius <= BORDER_THICKNESS: 
            self.y = BORDER_THICKNESS + self.radius
        # 2/ hitting the top border
        if self.y + self.radius >= HEIGHT + BORDER_THICKNESS:
            self.y = HEIGHT + BORDER_THICKNESS - self.radius

        # make sure to update the center of the ball
        # otherwise, it will stay at the center of the screen
        self.center = (self.x, self.y)

        # simulate bounce by inverting the ball's direction 
        # when it hits the bottom or top walls
        if self.y <= BORDER_THICKNESS + self.radius or self.y >= HEIGHT + BORDER_THICKNESS - self.radius:
            self.yDir *= -1

    def get_score(self):
        # if player 1 scores, return -1
        if self.x <= BORDER_THICKNESS + self.radius and not self.score_goal:
            self.score_goal = 1
            return -1
        # if player 2 scores, return 1
        elif self.x >= WIDTH + 2*BORDER_THICKNESS - self.radius and not self.score_goal:
            self.score_goal = 1
            return 1
        # if no one scores, return 0
        else:
            return 0

    def reset(self):
        self.x = WIDTH//2 + BORDER_THICKNESS
        self.y = HEIGHT//2 + BORDER_THICKNESS
        self.xDir *= -1
        self.score_goal = 0

    def collide(self):
        self.xDir *= -1

    def get_ball(self):
        return self.ball

"""
Helper functions
"""
def handle_key_down_movement(event_key, yDir1, yDir2):
    if event_key == pygame.K_UP:
        yDir2 = int(YDirection['UPWARD'])
    if event_key == pygame.K_DOWN:
        yDir2 = int(YDirection['DOWNWARD'])
    if event_key == pygame.K_w:
        yDir1 = int(YDirection['UPWARD'])
    if event_key == pygame.K_s:
        yDir1 = int(YDirection['DOWNWARD'])
    return yDir1, yDir2

def handle_key_up_movement(event_key, yDir1, yDir2):
    if event_key == pygame.K_UP or event_key == pygame.K_DOWN:
        yDir2 = int(YDirection['NONE'])
    if event_key == pygame.K_w or event_key == pygame.K_s:
        yDir1 = int(YDirection['NONE'])
    return yDir1, yDir2

def handle_score_logic(ball, player1, player2):
    winner_score = ball.get_score()
    if winner_score != 0:
        if winner_score == -1:
            player2.score += 1
        elif winner_score == 1:
            player1.score += 1
        ball.reset()

def display_center_dashed_line(screen):
    for i in range(BORDER_THICKNESS + 10, HEIGHT + BORDER_THICKNESS, 20):
        pygame.draw.rect(screen, WHITE, Rect(WIDTH//2 + BORDER_THICKNESS, i, 8, 8))

"""
Game engine
"""

def play_pong():
    # timer
    clock = pygame.time.Clock()
    game_over = False

    pygame.init()
    screen = pygame.display.set_mode((WIDTH + 2*BORDER_THICKNESS, HEIGHT + 2*BORDER_THICKNESS))
    arena = Rect(10, 10, WIDTH, HEIGHT)
    border = Rect(0, 0, BORDER_THICKNESS, BORDER_THICKNESS)
    pygame.draw.rect(screen, BLACK, border, 1)
    pygame.display.set_caption("PONG")

    player1 = Paddle(screen, 
                     x = 30, 
                     y = HEIGHT//2 - 25, 
                     width = 10, 
                     height = 90, 
                     velocity = 15, 
                     color = WHITE)
    
    player2 = Paddle(screen, 
                     x = WIDTH + 2*BORDER_THICKNESS - 30 - 10, 
                     y = HEIGHT//2 - 25, 
                     width = 10, 
                     height = 90, 
                     velocity = 15, 
                     color = WHITE)
    
    ball = Ball(screen,
                x = WIDTH//2 + BORDER_THICKNESS,
                y = HEIGHT//2 + BORDER_THICKNESS,
                radius = 8,
                velocity = 11,
                color = WHITE)

    yDir1, yDir2 = 0, 0
    
    while not game_over:
        # fill the borders then the arena inside
        screen.fill(BLACK)
        screen.fill(DODGER_BLUE, arena)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                game_over = True
            # handle key presses
            if e.type == pygame.KEYDOWN:
                yDir1, yDir2 = handle_key_down_movement(e.key, yDir1, yDir2)
            elif e.type == pygame.KEYUP:
                yDir1, yDir2 = handle_key_up_movement(e.key, yDir1, yDir2)
            
        # collision detection
        for paddle in [player1, player2]:
            if ball.get_ball().colliderect(paddle.get_paddle()):
                ball.collide()

        # move the paddles
        player1.move(yDir1)
        player2.move(yDir2)
        # move the ball
        ball.move()
        handle_score_logic(ball, player1, player2)

        # display the ball and the paddles
        player1.display(screen)
        player2.display(screen)
        ball.display(screen)

        # display the scores for each player
        player1.display_score(screen, 
                                x = WIDTH//2 - 110, 
                                y = 15, 
                                score = player1.get_score(),
                                font_color= WHITE)
        player2.display_score(screen,
                                x = WIDTH//2 + 40,
                                y = 15,
                                score = player2.get_score(),
                                font_color = WHITE)
        
        # display the center dashed line
        display_center_dashed_line(screen)

        pygame.display.update()
        clock.tick(FPS)

play_pong()
