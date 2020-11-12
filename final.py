#Python Final Project
#Start Date: 11/02/20

import pygame as pg
import sys 
import time 
from pygame.locals import *

#GLOABAL VARIABLES
winner = ""
XO = "x"
draw = False

timer = pg.time.Clock()

#board detail variables
WIDTH = 400
HEIGHT = 400
board = [None]*3, [None]*3, [None]*3

gray = (230, 230, 230)
white = (255, 255, 255)
black = (0, 0, 0)

#images 
x_img = pg.image.load("X2.png")
o_img = pg.image.load("O5.png")
TTT = pg.image.load("image2.jpeg")
#resize images
x_img = pg.transform.scale(x_img, (100, 100))
o_img = pg.transform.scale(o_img, (100, 100))
TTT = pg.transform.scale(TTT, (WIDTH, HEIGHT+100))
#########################################################################################

#initialize all pygame functionalities
pg.init()
fps = 30

#add 100 pixels to display for game status space
game_display = pg.display.set_mode((WIDTH, HEIGHT+100))
pg.display.set_caption("Tic-Tac-Toe")
#########################################################################################

#may delete if not functioning properly
'''def toggle_fullscreen(game_display):
    if toggle_fullscreen:
        game_display = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    else:
        game_display = pg.display.set_mode((WIDTH, HEIGHT))'''
##########################################################################################
def draw_lines():
    game_display.blit(TTT, (0,0))
    pg.display.update()
    time.sleep(3)
    game_display.fill(white)

    #vertical lines
    pg.draw.line(game_display, black, [WIDTH/3,0], [WIDTH/3, HEIGHT], 2)
    pg.draw.line(game_display, black, [WIDTH/3*2,0], [WIDTH/3*2, HEIGHT], 2)

    #horizontal lines
    pg.draw.line(game_display, black, [0,HEIGHT/3], [WIDTH, HEIGHT/3], 2)
    pg.draw.line(game_display, black, [0,HEIGHT/3*2], [WIDTH, HEIGHT/3*2], 2)
    display_status()
###############################################################################################
#needs to be fixed
def display_status():
    global draw

    if winner == "":
        message = XO.upper() + " 's Turn!"
    else:
        message = winner.upper() + " won!!!"
    if draw:
        message = "It's a Draw!"

    #font
    font = pg.font.Font(None, 30)
    text = font.render(message, 1, white)

    #display message
    game_display.fill(black, (0, 400, 500, 100))
    text_rect = text.get_rect(center = (WIDTH/2, 500-50))
    game_display.blit(text, text_rect)
    pg.display.update()
################################################################################################
def check_win():
    global board, winner,draw
    # check for winning rows
    for row in range (0,3):
        if ((board[row][0] == board[row][1] == board[row][2]) and (board[row][0] != None)):
            # this row won
            winner = board[row][0]
            #draw winning line 
            pg.draw.line(game_display, (50,168,74), (0, (row + 1)*HEIGHT/3 -HEIGHT/6),\
                              (WIDTH, (row + 1)*HEIGHT/3 - HEIGHT/6 ), 4)
            break
    # check for winning columns
    for col in range (0, 3):
        if (board[0][col] == board[1][col] == board[2][col]) and (board[0][col] != None):
            # this column won
            winner = board[0][col]
            #draw winning line
            pg.draw.line(game_display, (50,168,74),((col + 1)* WIDTH/3 - WIDTH/6, 0),\
                          ((col + 1)* WIDTH/3 - WIDTH/6, HEIGHT), 4)
            break
    # check for diagonal winners
    if (board[0][0] == board[1][1] == board[2][2]) and (board[0][0] != None):
        # game won diagonally left to right
        winner = board[0][0]
        pg.draw.line(game_display, (50,168,74), (50, 50), (350, 350), 4)

    # check 2nd diagonal winner
    if (board[0][2] == board[1][1] == board[2][0]) and (board[0][2] != None):
        # game won diagonally right to left
        winner = board[0][2]
        pg.draw.line (game_display, (50,168,74), (350, 50), (50, 350), 4)

    #DRAW DOESNT WORK
    if(all([all(row) for row in board]) and winner == None ):
        draw = True
    display_status()
############################################################################################################
def drawXO(row, col): 
    global board, XO 
    
    #first row
    if row == 1: 
        posx = 30 # was previously 50
          
    #second row    
    if row == 2: 
        posx = WIDTH / 3 + 30
          
    if row == 3: 
        posx = WIDTH / 3 * 2 + 30
   
    if col == 1: 
        posy = 30 #was previously 70
          
    if col == 2: 
        posy = HEIGHT / 3 + 30
      
    if col == 3: 
        posy = HEIGHT / 3 * 2 + 30
          
    # set up board  
    board[row-1][col-1] = XO 
    if(XO == 'x'): 
        #display x image in correct position
        game_display.blit(x_img, (posy, posx)) 
        XO = 'o'
    else: 
        #display o image in correct position
        game_display.blit(o_img, (posy, posx)) 
        XO = 'x'
    pg.display.update() 
############################################################################################################
def user_click(): 
    # get coordinates of mouse click 
    #pg.event.get() DIDNT HELP
    x, y = pg.mouse.get_pos() 
    #print(x,y)
    '''m1, m2, m3 = pg.mouse.get_pressed()
    if m1 == 1:
        x, y = pg.mouse.get_pos()
        #print(x, y)'''
   
    # get column of mouse click (1-3) 
    if (x < WIDTH / 3): 
        col = 1
    elif (x < WIDTH / 3 * 2): 
        col = 2
    elif(x < WIDTH): 
        col = 3
    else: 
        col = None
   
    # get row of mouse click (1-3) 
    if (y < HEIGHT / 3): 
        row = 1
    elif (y < HEIGHT / 3 * 2): 
        row = 2
    elif (y < HEIGHT): 
        row = 3 
    else: 
        row = None
    print(row,col)
        
    # place image in correct position
    if(row and col and board[row - 1][col - 1] == None): 
        global XO 
        drawXO(row, col) 
        check_win() 
################################################################################################################
def reset_game():
    #reset all gloabl variables
    global board, winner, XO, draw
    time.sleep(3)
    XO = 'x'
    draw = False
    draw_lines()
    winner = ""
    board = [[None]*3,[None]*3,[None]*3]
################################################################################################################
#handle all the ways of quitting
def event_handler():
    for ev in pg.event.get():
        if ev.type == QUIT or (
            ev.type == KEYDOWN and (
                ev.key == K_ESCAPE or
                ev.key == K_q
            )):
            pg.quit()
            quit()
        elif ev.type == MOUSEBUTTONDOWN:
            #activate user_click()
            user_click()
            if (winner or draw):
                reset_game()
    pg.display.update()
    timer.tick(fps)
###########################################################################################
#toggle_fullscreen(game_display)

draw_lines() #this doesnt work properly

#main game loop
while True:
    event_handler()

#Initial Game screen Doesnt Work  
#DRAW/TIE GAME DOESNT WORK YET
#GAME DOESNT RESET WHEN THERE'S A DRAW
#still need AI feature for one player option
    