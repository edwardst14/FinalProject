#Python Final Project
#Start Date: 11/02/20

#IMPORTS
import pygame 
import pygame as pg
import sys 
import time 
from pygame.locals import *
import minmax as ttt
from tkinter import *
from tkinter import messagebox
import sqlite3

#GLOBAL VARIABLES
WIDTH = 800
HEIGHT = 600
board = [None]*3, [None]*3, [None]*3

#SINGLE PLAYER GAME DETAILS
user = None
board = ttt.initial_state()
ai_turn = False

#MULTIPLAYER GAME DETAILS
play1 = None
play2 = None

#define colors
BLUE = (106, 159, 181)
WHITE = (255, 255, 255)
GRAY = (211,211,211)
DARKGRAY = (128,128,128)
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dimgray')

#initialize pygame font and other functionalities
pygame.font.init()
pygame.init()
conn = sqlite3.connect("scores.sqlite") #creates the database if it doesn't already exist
cursor = conn.cursor() #provides are cursor to the above connection (the means of executing the SQL queries)
#cursor.execute("create table playerScores (name text, wins integer, losses integer)") #execute the create table query

fps = 30 #MAY DELETE
timer = pygame.time.Clock()
FONT = pg.font.Font(None, 32)
NAME = ""

#FONTS
mediumFont = pygame.font.SysFont("OpenSans-Regular.ttf", 28)
largeFont = pygame.font.SysFont("OpenSans-Regular.ttf", 40)
moveFont = pygame.font.SysFont("OpenSans-Regular.ttf", 60)

#add 100 pixels to display for game status space
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

#-----------------------------------------------------------------
class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text)
                    entry = cursor.execute("SELECT *        \
                            FROM playerScores               \
                                WHERE name = ?;", [self.text])

                    
                    data = entry.fetchall()
                    print(data)
                    if len(data) != 0:
                        print("Alreaady Exists")
                    else: 
                        cursor.execute("INSERT INTO    \
                            playerScores(name, wins, losses)    \
                            VALUES(?,?,?)", [self.text, 0, 0])

                    conn.commit()
                    NAME = self.text
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if event.unicode.isalpha():
                        self.text += event.unicode

                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)
#----------------------------------------------------------------------

def text_objects(text, font):
    textSurface = font.render(text, True, (DARKGRAY))
    return textSurface, textSurface.get_rect()

def button(msg, x, y, w, h, inactive, active, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, active,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(screen, inactive,(x,y,w,h))

    smallText = pygame.font.SysFont("OpenSans-Regular.ttf",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)

def singlePlay():
    print("single player screen")
    
    global user, board, ai_turn
    #print(user)

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT or (
                    ev.type == KEYDOWN and (
                        ev.key == K_ESCAPE or
                        ev.key == K_q
                    )):
                    end()
        screen.fill(BLUE)

        #let user choose a player
        if user == None:
            #Draw selection screen
            title = largeFont.render("Select a Letter", True, WHITE)
            titleRect = title.get_rect()
            titleRect.center = ((WIDTH / 2), 50)
            screen.blit(title, titleRect)

            button("Play as X", (WIDTH / 8), 3 * (HEIGHT / 4), (WIDTH / 4), 50, WHITE, GRAY, setUserX)
            button("Play as O", (WIDTH / 8) * 5, 3 * (HEIGHT / 4), (WIDTH / 4), 50, WHITE, GRAY, setUserO)

        else:
            #Draw game board

            tile_size = 115
            tile_origin = (WIDTH / 2 - (1.5 * tile_size),
                            HEIGHT / 2 - (1.5 * tile_size))
            tiles = []
            for i in range(3):
                row = []
                for j in range(3):
                    rect = pygame.Rect(
                        tile_origin[0] + j * tile_size,
                        tile_origin[1] + i * tile_size,
                        tile_size, tile_size
                    )
                    pygame.draw.rect(screen, DARKGRAY, rect, 3)

                    if board[i][j] != ttt.EMPTY:
                        move = moveFont.render(board[i][j], True, WHITE)
                        moveRect = move.get_rect()
                        moveRect.center = rect.center
                        screen.blit(move, moveRect)
                    row.append(rect)
                tiles.append(row)

            game_over = ttt.terminal(board)
            player = ttt.player(board)

            #show game title
            if game_over:
                winner = ttt.winner(board)
                if winner is None:
                    title = "Game Over: Draw!"
                else:
                    title = "Game Over: {} wins!".format(winner)
            elif user == player:
                title = "Playing as {}".format(user)
            else:
                title = "Computer thinking..."
            title = largeFont.render(title, True, GRAY)
            titleRect = title.get_rect()
            titleRect.center = ((WIDTH / 2), 30)
            screen.blit(title, titleRect)

            player, game_over, board, tiles = minimax(player, game_over, board, tiles)

            if game_over:
                button("Play Again", (WIDTH / 3), (HEIGHT - 65), (WIDTH / 3), 50, WHITE, GRAY, reset)

        pygame.display.update()

def reset():
    global user, board, ai_turn, play1, play2

    time.sleep(0.5)
    user = None
    board = ttt.initial_state()
    ai_turn = False

    play1 = None
    play2 = None
    
def minimax(player, game_over, board, tiles):
    # Check for AI move
    global ai_turn

    if user != player and not game_over:
        if ai_turn:
            time.sleep(0.5)
            move = ttt.minimax(board)
            board = ttt.result(board, move)
            ai_turn = False
        else:
            ai_turn = True

    # Check for a user move
    click, _, _ = pygame.mouse.get_pressed()
    if click == 1 and user == player and not game_over:
        mouse = pygame.mouse.get_pos()
        for i in range(3):
            for j in range(3):
                if (board[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(mouse)):
                    board = ttt.result(board, (i, j))

    return player, game_over, board, tiles

def setUserX():
    global user

    timer.tick(3)
    user = ttt.X
    print(user)
    print("works when X button is clicked")
    
def setUserO():
    global user

    timer.tick(3)
    user = ttt.O
    print(user)
    print("works when O button is clicked")

def single():
    print("going to diff screen")

    singlePlay()

def filler2():
    print("works fine")

def multiPlay():
    print("multiplayer screen")
    global board, NAME

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT or (
                    ev.type == KEYDOWN and (
                        ev.key == K_ESCAPE or
                        ev.key == K_q
                    )):
                    end()
        screen.fill(BLUE)
        play1 = ttt.X
        play2 = ttt.O

        #Draw game board
        tile_size = 115
        tile_origin = (WIDTH / 2 - (1.5 * tile_size),
                        HEIGHT / 2 - (1.5 * tile_size))
        tiles = []
        for i in range(3):
            row = []
            for j in range(3):
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size, tile_size
                )
                pygame.draw.rect(screen, DARKGRAY, rect, 3)

                if board[i][j] != ttt.EMPTY:
                    move = moveFont.render(board[i][j], True, WHITE)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                    screen.blit(move, moveRect)
                row.append(rect)
            tiles.append(row)

        game_over = ttt.terminal(board)
        player = ttt.player(board)

        if game_over:
            winner = ttt.winner(board)
            if winner is None:
                title = "Game Over: Draw!"
            else:
                title = "Game Over: {} wins!".format(winner)
        elif play1 == player:
            title = "Play as {}".format(play1)
        else:
            title = "Play as {}".format(play2)
        title = largeFont.render(title, True, WHITE)
        titleRect = title.get_rect()
        titleRect.center = ((WIDTH / 2), 30)
        screen.blit(title, titleRect)
        
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(3):
                for j in range(3):
                    if (board[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(mouse)):
                        board = ttt.result(board, (i, j))

        if game_over:
            button("Play Again", (WIDTH / 3), (HEIGHT - 65), (WIDTH / 3), 50, WHITE, GRAY, reset)

        pygame.display.update()

def multi():
    print("going to different screen")

    multiPlay()

def end():
    conn.close()
    pygame.quit()
    sys.exit()
#---------------------------------------------------------------------
def mainScreen():
    input_box1 = InputBox((WIDTH / 8) * 3.1, (HEIGHT / 3), 125, 50)
    #input_box2 = InputBox(100, 300, 140, 32)
    input_boxes = [input_box1]
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT or (
                    ev.type == KEYDOWN and (
                        ev.key == K_ESCAPE or
                        ev.key == K_q
                    )):
                    end()
            for box in input_boxes:
                box.handle_event(ev)

        for box in input_boxes:
            box.update()

        screen.fill(BLUE)
        #pygame.display.flip() #can also use update here
        for box in input_boxes:
            box.draw(screen)

        #Draw on main screen
        title = largeFont.render("Play Tic-Tac-Toe", True, WHITE)
        titleRect = title.get_rect()
        titleRect.center = ((WIDTH / 2), 50)
        screen.blit(title, titleRect)

        title2 = mediumFont.render("Enter Name:", True, WHITE)
        titleRect = title2.get_rect()
        titleRect.center = ((WIDTH / 2), 175)
        screen.blit(title2, titleRect)

        #Draw all three buttons on screen
        button("Single Player", (WIDTH / 8), (HEIGHT / 4) * 2, 125, 50, WHITE, GRAY, single)
        button("Two Player", (WIDTH / 8) * 6, (HEIGHT / 4) * 2, 125, 50, WHITE, GRAY, multi)
        button("QUIT", (WIDTH / 8) * 3.5, (HEIGHT / 3) * 2, 125, 50, WHITE, GRAY, end)
        pygame.display.flip() #can also use update here


#------------------------------------------------------------------------------------
mainScreen()