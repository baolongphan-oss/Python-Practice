import numpy as np
import pygame
import sys
from enum import IntEnum
from pygame.locals import *

# kudos to: https://www.askpython.com/python/examples/connect-four-game
# color rgb codes
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

# global variables
ROWS = 6
COLS = 7
THREE_EXTRA = 3
SQ_SIZE = 100
PADDING = 5
DISC_RADIUS = (SQ_SIZE//2 - PADDING)
SCREEN_WIDTH = SQ_SIZE*COLS 
# create an additional row at the top to drop the discs
SCREEN_HEIGHT = SQ_SIZE*(ROWS+1)

# enumerator for player discs
class Disc(IntEnum):
    EMPTY = 0
    PLAYER_ONE = 1 # red color
    PLAYER_TWO = 2 # blue color

# board functions
def init_board():
    board = np.zeros((ROWS, COLS))
    return board

def drop_disc(board, r, c, player_code):
    board[r][c] = player_code

def can_drop_disc(board, c):
    return board[0][c] == 0

def get_next_empty_row(board, c):
    for r in range(ROWS-1,-1,-1):
        if board[r][c] == 0:
            return r

def horizontal_win(board, r, c, player_code):
    return (board[r][c] == player_code
        and board[r][c+1] == player_code
        and board[r][c+2] == player_code
        and board[r][c+3] == player_code)

def vertical_win(board, r, c, player_code):
    return (board[r][c] == player_code
        and board[r+1][c] == player_code
        and board[r+2][c] == player_code
        and board[r+3][c] == player_code)

def diagonal_nw_se_win(board, r, c, player_code):
    return (board[r][c] == player_code
        and board[r+1][c+1] == player_code
        and board[r+2][c+2] == player_code
        and board[r+3][c+3] == player_code)

def diagonal_sw_ne_win(board, r, c, player_code):
    return (board[r][c] == player_code
        and board[r-1][c+1] == player_code
        and board[r-2][c+2] == player_code
        and board[r-3][c+3] == player_code)

def check_winner(board, player_code):
    for r in range(ROWS):
        for c in range(COLS):
            # check for every rows except the bottom 3 
            if r < (ROWS-THREE_EXTRA):
                if vertical_win(board, r, c, player_code):
                    return True
                # check for every columns except the rightmost 3
                if c < (COLS-THREE_EXTRA):
                    if horizontal_win(board, r, c, player_code): 
                        return True
                    if diagonal_nw_se_win(board, r, c, player_code):
                        return True
            # check for the bottom 3 rows
            else:
                # check for every columns except the rightmost 3
                if c < (COLS-THREE_EXTRA):
                    if horizontal_win(board, r, c, player_code): 
                        return True
                    if diagonal_sw_ne_win(board, r, c, player_code):
                        return True
                    
    return False

def get_player_color(player_code):
    if player_code == int(Disc['PLAYER_ONE']):
        return RED 
    elif player_code == int(Disc['PLAYER_TWO']):
        return YELLOW 
    else:
        return BLACK

def draw_init_board(screen):
    rect = None
    center = None
    for r in range(ROWS):
        for c in range(COLS):
            # specify each rectangle's x-coordinates, y- coordinates, width, and height
            # note: for the y-coordinate, we add one extra square to account for 
            # the top row where the user can drop their discs.
            rect = Rect(SQ_SIZE*c, SQ_SIZE*(r+1), SQ_SIZE, SQ_SIZE)
            pygame.draw.rect(screen, BLUE, rect)
            center = (SQ_SIZE*(c+0.5), SQ_SIZE*(r+1.5))
            pygame.draw.circle(screen, BLACK, center, DISC_RADIUS)
    pygame.display.update()

def update_board(screen, r, c, player_code):
    color = get_player_color(player_code)
    # note: for the y-coordinate, we add one extra square to account for 
    # the top row where the user can drop their discs.
    center = (SQ_SIZE*(c+0.5),SQ_SIZE*(r+1.5))
    pygame.draw.circle(screen, color, center, DISC_RADIUS)
    pygame.display.update()

def play_connect_four():
    # initialize the game states
    board = init_board()
    game_over = False
    turn = 0

    # initialize pygame screen
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    draw_init_board(screen)
    myfont = pygame.font.SysFont('Comic Sans', 60)

    while not game_over:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: 
                sys.exit()

            # Turn is either 0 or 1.
            # If turn = 0 then player_code is 1. Otherwise, the player_code is 2.
            player_code = turn+1 

            if e.type == pygame.MOUSEMOTION:
                # specify the top row's x-coordinates, y- coordinates, width, and height
                rect = Rect(0, 0, SCREEN_WIDTH, SQ_SIZE)
                pygame.draw.rect(screen, BLACK, rect)

                # draw the circle that moves along the top row with the user's mouse movement
                center = (e.pos[0], SQ_SIZE//2) # x- and -y coordinates
                color = get_player_color(player_code)
                pygame.draw.circle(screen, color, center, DISC_RADIUS)

            pygame.display.update()

            if e.type == pygame.MOUSEBUTTONDOWN:
                # specify the top row's x-coordinates, y- coordinates, width, and height
                rect = Rect(0, 0, SCREEN_WIDTH, SQ_SIZE)
                pygame.draw.rect(screen, BLACK, rect)
                # get the exact column index from x-coordinates
                col = e.pos[0]//SQ_SIZE
                if can_drop_disc(board, col):
                    row = get_next_empty_row(board, col)
                    drop_disc(board, row, col, player_code)
                    update_board(screen, row, col, player_code)

                    if check_winner(board, player_code):
                        color = get_player_color(player_code)
                        label = myfont.render("Player {} wins!!!".format(player_code), 1, color)
                        screen.blit(label, (40,10))
                        game_over = True
                
                pygame.display.update()
                print(board)
                turn = (turn+1) % 2
                
                if game_over:
                    pygame.time.wait(2000)
  
play_connect_four()
