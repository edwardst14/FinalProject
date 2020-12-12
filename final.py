#Python Final Project
#Start Date: 11/02/20
#End Date: 12/05/20

#MOST RECENT FILE
''' missing screen to display user scores - top 5 only
       missing error handling of user entering more than 2 names on multiplayer screen
       make input boxes disappear??? IS THAT ENOUGH '''

#IMPORTS
import pygame, sys, time
from pygame.locals import *
import minmax as ttt
import textBox as text
import sqlite3
import ticdb as ticdb
from ticdb import DBConnection
from player import Player

#GLOBAL VARIABLES -- Board Details
WIDTH = 800
HEIGHT = 600
board = [None]*3, [None]*3, [None]*3

#SINGLE PLAYER GAME DETAILS
user = None
board = ttt.initial_state()
ai_turn = False
winner = None

#MULTIPLAYER GAME DETAILS
play1 = None
play2 = None
save_player = False

#Define colors
BLUE = (106, 159, 181)
BLUE2 = (126, 179, 201)
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

db = DBConnection()

def text_objects(text, font):
    textSurface = font.render(text, True, DARKGRAY)
    if text == "TOP THREE SCORES":
        textSurface = font.render(text, True, WHITE)
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

    if msg == "Rules" or msg == "Top Scores":
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
    #print("single player screen")
    
    global user, board, ai_turn, winner, save_player

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
                title = "Playing as {} - {}".format(user, text.play1Name)
            else:
                title = "Computer thinking..."
            title = largeFont.render(title, True, GRAY)
            titleRect = title.get_rect()
            titleRect.center = ((WIDTH / 2), 30)
            screen.blit(title, titleRect)

            player, game_over, board, tiles = minimax(player, game_over, board, tiles)

            if game_over:
                button("Play Again", (WIDTH / 3), (HEIGHT - 65), (WIDTH / 3), 50, WHITE, GRAY, reset)

                db.updateUserScores(text.player1)

        pygame.display.update()

def reset():
    global user, board, ai_turn, play1, play2, winner

    print("Storing data into DB")
    if text.player1 and text.player1.character == winner:
        text.player1.wins+= 1
        if text.player2:
            text.player2.losses+=1

    elif text.player2 and text.player2.character == winner:
        text.player2.wins+= 1
        text.player1.losses+=1

    else:
        text.player1.losses+=1
        #In the case of a two player draw
        if text.player2:
            text.player2.losses+=1
    save_player = False

    time.sleep(0.5)
    user = None
    board = ttt.initial_state()
    ai_turn = False
    play1 = None
    play2 = None
    winner = None

def resetPlayers():
    global user, board, ai_turn, play1, play2, winner

    user = None
    board = ttt.initial_state()
    ai_turn = False
    play1 = None
    play2 = None
    winner = None
    text.play1Name = ''
    text.play2Name = ''
    
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
    text.player1.character = "O"

def single():
    global user

    input_box1 = text.InputBox((WIDTH / 8) * 3.1, (HEIGHT / 3), 125, 50)
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
        button("Return to Main", (WIDTH / 8) - 90, (HEIGHT / 4) * 2 + 265, 110, 25, BLUE, BLUE2, mainScreen)

        if text.play1Name == '':
            for box in input_boxes:
                box.draw(screen)

        #let user choose a player
        if user == None:
            #Draw selection screen and get user's name
            title = largeFont.render("Enter Name and Select a Letter", True, WHITE)
            titleRect = title.get_rect()
            titleRect.center = ((WIDTH / 2), 50)
            screen.blit(title, titleRect)

            button("Play as X", (WIDTH / 8), 3 * (HEIGHT / 4), (WIDTH / 4), 50, WHITE, GRAY, setUserX)
            button("Play as O", (WIDTH / 8) * 5, 3 * (HEIGHT / 4), (WIDTH / 4), 50, WHITE, GRAY, setUserO)
        else:
            singlePlay()

        #print(text.play1Name)
        pygame.display.update()

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

        line1 = largeFont.render("The rules of Tic-Tac-Toe are simple:", True, WHITE)
        line1Rect = line1.get_rect()
        line1Rect.center = ((WIDTH / 2), ((HEIGHT / 3) + (50/2)) )
        screen.blit(line1, line1Rect)

        line2 = largeFont.render("Simply place your letter wherever you wish", True, WHITE)
        line2Rect = line2.get_rect()
        line2Rect.center = ((WIDTH / 2), ((HEIGHT / 3) + (50/2) + 35) )
        screen.blit(line2, line2Rect)

        line3 = largeFont.render("Three in a row always wins!", True, WHITE)
        line3Rect = line3.get_rect()
        line3Rect.center = ((WIDTH / 2), ((HEIGHT / 3) + (50/2) + 65) )
        screen.blit(line3, line3Rect)

        line4 = largeFont.render("X always goes first, no matter what!", True, WHITE)
        line4Rect = line4.get_rect()
        line4Rect.center = ((WIDTH / 2), ((HEIGHT / 3) + (50/2) + 95) )
        screen.blit(line4, line4Rect)

        line4 = largeFont.render("A Draw is a loss for both!", True, WHITE)
        line4Rect = line4.get_rect()
        line4Rect.center = ((WIDTH / 2), ((HEIGHT / 3) + (50/2) + 125) )
        screen.blit(line4, line4Rect)
    
        pygame.display.flip()

def scores():
    #display top 5 scores in DB
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

        #print("showing scores")
        msg = "TOP THREE SCORES"
        textSurf, textRect = text_objects(msg, largeFont)
        textRect.center = (((WIDTH / 8) * 3 + 100), HEIGHT - 550)
        screen.blit(textSurf, textRect)

        #get scores from DB
        score = db.displayScores()

        name1 = largeFont.render(str(score[0][0]), True, WHITE)
        name1Rect = name1.get_rect()
        name1Rect.center = (((WIDTH / 8) * 3), HEIGHT - 450)
        screen.blit(name1, name1Rect)

        name1 = largeFont.render(str(score[0][1]), True, WHITE)
        name1Rect = name1.get_rect()
        name1Rect.center = (((WIDTH / 8) * 3 + 250), HEIGHT - 450)
        screen.blit(name1, name1Rect)

        name2 = largeFont.render(str(score[1][0]), True, WHITE)
        name2Rect = name2.get_rect()
        name2Rect.center = (((WIDTH / 8) * 3), HEIGHT - 350)
        screen.blit(name2, name2Rect)

        name2 = largeFont.render(str(score[1][1]), True, WHITE)
        name2Rect = name2.get_rect()
        name2Rect.center = (((WIDTH / 8) * 3 + 250), HEIGHT - 350)
        screen.blit(name2, name2Rect)

        name3 = largeFont.render(str(score[2][0]), True, WHITE)
        name3Rect = name3.get_rect()
        name3Rect.center = (((WIDTH / 8) * 3), HEIGHT - 250)
        screen.blit(name3, name3Rect)

        name3 = largeFont.render(str(score[2][1]), True, WHITE)
        name3Rect = name3.get_rect()
        name3Rect.center = (((WIDTH / 8) * 3 + 250), HEIGHT - 250)
        screen.blit(name3, name3Rect)

        pygame.display.flip()

def multiPlay():
    #print("multiplayer screen")
    global board, winner

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
        text.player1.character = "X"
        play2 = ttt.O
        text.player2.character = "O"

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
            title = "Playing as {} - {}".format(play1, text.play1Name)
        else:
            title = "Playing as {} - {}".format(play2, text.play2Name)
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

            db.updateUserScores(text.player1)
            db.updateUserScores(text.player2)
        pygame.display.update()

def multi():
    #print("going to different screen")
    global play1Name, play2Name

    input_box1 = text.InputBox((WIDTH / 8) * 1.55, (HEIGHT / 3) + 60, 125, 50)
    input_box2 = text.InputBox((WIDTH / 8) * 4.65, (HEIGHT / 3) + 60, 125, 50)
    input_boxes = [input_box1, input_box2]

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
        button("Return to Main", (WIDTH / 8) - 90, (HEIGHT / 4) * 2 + 265, 110, 25, BLUE, BLUE2, mainScreen)

        if text.play1Name == '':
            for box in input_boxes:
                box.draw(screen)
        elif text.play1Name != '' and text.play2Name == '':
            for box in input_boxes:
                box.draw(screen)

        char1 = mediumFont.render("Player X", True, WHITE)
        charRect1 = char1.get_rect()
        charRect1.center = ((WIDTH / 3) - 10, (HEIGHT / 4) * 1.5)
        screen.blit(char1, charRect1)

        char2 = mediumFont.render("Player O", True, WHITE)
        charRect2 = char2.get_rect()
        charRect2.center = ((WIDTH / 3) * 2 + 20, (HEIGHT / 4) * 1.5)
        screen.blit(char2, charRect2)

        title2 = largeFont.render("Enter Names:", True, WHITE)
        titleRect = title2.get_rect()
        titleRect.center = ((WIDTH / 2), 175)
        screen.blit(title2, titleRect)

        note = mediumFont.render("Remember: X always goes first!", True, WHITE)
        noteRect = note.get_rect()
        noteRect.center = ((WIDTH / 8) * 4, (HEIGHT / 3) * 2)
        screen.blit(note, noteRect)

        button("Let's Play!", (WIDTH / 8) * 3.5, (HEIGHT / 3) * 2.5 + 30, 125, 50, WHITE, GRAY, multiPlay)

        #print(text.play1Name, text.play2Name)
        pygame.display.flip()

def end():
    db.conn.close() #NEW FROM GULA
    pygame.quit()
    sys.exit()

def mainScreen():

    resetPlayers()
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
        button("One Player", (WIDTH / 8), (HEIGHT / 4) * 2, 125, 50, WHITE, GRAY, single)
        button("Two Player", (WIDTH / 8) * 6, (HEIGHT / 4) * 2, 125, 50, WHITE, GRAY, multi)
        button("QUIT", (WIDTH / 8) * 3.5, (HEIGHT / 3) * 2, 125, 50, WHITE, GRAY, end)

        button("Rules", (WIDTH / 8) * 7 + 20, HEIGHT - 585, 55, 25, BLUE, BLUE2, rules)
        button("Top Scores", (WIDTH / 8) - 95, HEIGHT - 585, 100, 25, BLUE, BLUE2, scores)
        pygame.display.flip() #can also use update here

#------------------------------------------------------------------------------------
mainScreen()