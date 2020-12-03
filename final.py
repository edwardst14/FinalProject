#Python Final Project
#Start Date: 11/02/20
#End Date: 12/05/20

#IMPORTS
import pygame 
import sys 
import time 
from pygame.locals import *
import minmax as ttt

#GLOBAL VARIABLES -- Board Details
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

#Define colors
BLUE = (106, 159, 181)
BLUE2 = (126, 179, 201)
#WHITE = (255, 255, 255)
WHITE = (217,217,217)
GRAY = (211,211,211)
DARKGRAY = (128,128,128)

#initialize pygame font and other functionalities
pygame.font.init()
pygame.init()
timer = pygame.time.Clock()

#FONTS
mediumFont = pygame.font.SysFont("OpenSans-Regular.ttf", 28)
largeFont = pygame.font.SysFont("OpenSans-Regular.ttf", 40)
moveFont = pygame.font.SysFont("OpenSans-Regular.ttf", 60)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

def text_objects(text, font):
    textSurface = font.render(text, True, DARKGRAY)
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

    if msg == "Rules":
        smallFont = pygame.font.SysFont("OpenSans-Regular.ttf", 25)
        textSurf, textRect = text_objects(msg, smallFont)
        textSurf = textSurface = smallFont.render(msg, True, (WHITE))
    elif msg == "Return to Main":
        smallFont = pygame.font.SysFont("OpenSans-Regular.ttf", 22)
        textSurf, textRect = text_objects(msg, smallFont)
        textSurf = textSurface = smallFont.render(msg, True, (WHITE))
    else:
        #smallText = pygame.font.SysFont("OpenSans-Regular.ttf", 28)
        textSurf, textRect = text_objects(msg, mediumFont)

    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)

def singlePlay():
    print("single player screen")
    
    global user, board, ai_turn

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT or (
                    ev.type == KEYDOWN and (
                        ev.key == K_ESCAPE or
                        ev.key == K_q
                    )):
                    end()
        screen.fill(BLUE)
        button("Return to Main", (WIDTH / 8) - 90, (HEIGHT / 4) * 2 + 265, 110, 25, BLUE, BLUE2, mainScreen)

        #User chooses a player
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

    timer.tick(1)
    user = ttt.X
    print(user)
    #print("works when X button is clicked")
    
def setUserO():
    global user

    timer.tick(1)
    user = ttt.O
    print(user)
    print("works when O button is clicked")

def rules():
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT or (
                    ev.type == KEYDOWN and (
                        ev.key == K_ESCAPE or
                        ev.key == K_q
                    )):
                    end()

        screen.fill(BLUE)
        button("Return to Main", (WIDTH / 8) - 90, (HEIGHT / 4) * 2 + 265, 110, 25, BLUE, BLUE2, mainScreen)

        msg = "The rules of Tic-Tac-Toe are simple:"
        textSurf, textRect = text_objects(msg, largeFont)
        textRect.center = ( ((WIDTH / 8) * 3 + (125/2)), ((HEIGHT / 3) + (50/2)) )
        screen.blit(textSurf, textRect)

        msg = "Simply place your letter wherever you wish"
        textSurf, textRect = text_objects(msg, largeFont)
        textRect.center = ( ((WIDTH / 8) * 3 + (125/2)), ((HEIGHT / 3) + (50/2) + 35) )
        screen.blit(textSurf, textRect)

        msg = "Three in a row always wins!"
        textSurf, textRect = text_objects(msg, largeFont)
        textRect.center = ( ((WIDTH / 8) * 3 + (125/2)), ((HEIGHT / 3) + (50/2) + 65) )
        screen.blit(textSurf, textRect)

        msg = "And X always goes first, no matter what"
        textSurf, textRect = text_objects(msg, largeFont)
        textRect.center = ( ((WIDTH / 8) * 3 + (125/2)), ((HEIGHT / 3) + (50/2) + 95) )
        screen.blit(textSurf, textRect)
        
        pygame.display.flip()

def multiPlay():
    print("multiplayer screen")
    global board

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT or (
                    ev.type == KEYDOWN and (
                        ev.key == K_ESCAPE or
                        ev.key == K_q
                    )):
                    end()
        screen.fill(BLUE)
        button("Return to Main", (WIDTH / 8) - 90, (HEIGHT / 4) * 2 + 265, 110, 25, BLUE, BLUE2, mainScreen)

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

def end():
    pygame.quit()
    sys.exit()
#------------------------------------------------------------------------------------
def mainScreen():
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT or (
                    ev.type == KEYDOWN and (
                        ev.key == K_ESCAPE or
                        ev.key == K_q
                    )):
                    end()

        screen.fill(BLUE)

        #Draw on main screen
        title = largeFont.render("Play Tic-Tac-Toe", True, WHITE)
        titleRect = title.get_rect()
        titleRect.center = ((WIDTH / 2), 50)
        screen.blit(title, titleRect)

        #Draw all buttons on screen
        button("One Player", (WIDTH / 8), (HEIGHT / 4) * 2, 125, 50, WHITE, GRAY, singlePlay)
        button("Two Player", (WIDTH / 8) * 6, (HEIGHT / 4) * 2, 125, 50, WHITE, GRAY, multiPlay)
        button("QUIT", (WIDTH / 8) * 3.5, (HEIGHT / 3) * 2, 125, 50, WHITE, GRAY, end)

        button("Rules", (WIDTH / 8) * 7 + 20, HEIGHT - 585, 55, 25, BLUE, BLUE2, rules)
        pygame.display.flip() #can also use update here

#------------------------------------------------------------------------------------
mainScreen()