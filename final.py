#Python Final Project
#Start Date: 11/02/20

import pygame 
import sys 
import time 
from pygame.locals import *


#GLOABAL VARIABLES
winner = ""
XO = "x"
draw = False

timer = pygame.time.Clock()

#board detail variables
WIDTH = 400
HEIGHT = 400
board = [None]*3, [None]*3, [None]*3

black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
orange = (255,127,0)
gray = (50,50,50)
bright_red = (255,0,0)
bright_green = (0,255,0)
bright_orange = (255,215,0)


#images 
x_img = pygame.image.load("X2.png")
o_img = pygame.image.load("O5.png")
TTT = pygame.image.load("image2.jpeg")
#resize images
x_img = pygame.transform.scale(x_img, (100, 100))
o_img = pygame.transform.scale(o_img, (100, 100))
TTT = pygame.transform.scale(TTT, (WIDTH, HEIGHT+100))
#########################################################################################

#initialize all pygame functionalities
pygame.init()
fps = 30

#add 100 pixels to display for game status space
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT+100))
pygame.display.set_caption("Tic-Tac-Toe")
##########################################################################################
def draw_lines():
    gameDisplay.blit(TTT, (0,0))
    pygame.display.update()
    time.sleep(3)
    gameDisplay.fill(white)

    #vertical lines
    pygame.draw.line(gameDisplay, black, [WIDTH/3,0], [WIDTH/3, HEIGHT], 2)
    pygame.draw.line(gameDisplay, black, [WIDTH/3*2,0], [WIDTH/3*2, HEIGHT], 2)

    #horizontal lines
    pygame.draw.line(gameDisplay, black, [0,HEIGHT/3], [WIDTH, HEIGHT/3], 2)
    pygame.draw.line(gameDisplay, black, [0,HEIGHT/3*2], [WIDTH, HEIGHT/3*2], 2)
    display_status()
###############################################################################################
def display_status():
    global draw

    if winner == "":
        message = XO.upper() + " 's Turn!"
    else:
        message = winner.upper() + " won!!!"
    if draw:
        message = "It's a Draw!"

    #font
    font = pygame.font.Font(None, 30)
    text = font.render(message, 1, white)

    #display message
    gameDisplay.fill(black, (0, 400, 500, 100))
    text_rect = text.get_rect(center = (WIDTH/2, 500-50))
    gameDisplay.blit(text, text_rect)
    pygame.display.update()
################################################################################################
def check_win():
    global board, winner,draw
    # check for winning rows
    for row in range (0,3):
        if ((board[row][0] == board[row][1] == board[row][2]) and (board[row][0] != None)):
            # this row won
            winner = board[row][0]
            #draw winning line 
            pygame.draw.line(gameDisplay, (50,168,74), (0, (row + 1)*HEIGHT/3 -HEIGHT/6),\
                              (WIDTH, (row + 1)*HEIGHT/3 - HEIGHT/6 ), 4)
            break
    # check for winning columns
    for col in range (0, 3):
        if (board[0][col] == board[1][col] == board[2][col]) and (board[0][col] != None):
            # this column won
            winner = board[0][col]
            #draw winning line
            pygame.draw.line(gameDisplay, (50,168,74),((col + 1)* WIDTH/3 - WIDTH/6, 0),\
                          ((col + 1)* WIDTH/3 - WIDTH/6, HEIGHT), 4)
            break
    # check for diagonal winners
    if (board[0][0] == board[1][1] == board[2][2]) and (board[0][0] != None):
        # game won diagonally left to right
        winner = board[0][0]
        pygame.draw.line(gameDisplay, (50,168,74), (50, 50), (350, 350), 4)

    # check 2nd diagonal winner
    if (board[0][2] == board[1][1] == board[2][0]) and (board[0][2] != None):
        # game won diagonally right to left
        winner = board[0][2]
        pygame.draw.line (gameDisplay, (50,168,74), (350, 50), (50, 350), 4)

    if(all([all(row) for row in board]) and winner == "" ):
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
        gameDisplay.blit(x_img, (posy, posx)) 
        XO = 'o'
    else: 
        #display o image in correct position
        gameDisplay.blit(o_img, (posy, posx)) 
        XO = 'x'
    pygame.display.update() 
############################################################################################################
def user_click(): 
    # get coordinates of mouse click 
    x, y = pygame.mouse.get_pos() 
   
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
    #print(row,col)
        
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
##########################################################################################################
def game_loop():
    draw_lines()
    while True:
        for ev in pygame.event.get():
            if ev.type == QUIT or (
                ev.type == KEYDOWN and (
                    ev.key == K_ESCAPE or
                    ev.key == K_q
                )):
                pygame.quit()
                quit()
            elif ev.type == MOUSEBUTTONDOWN:
                #activate user_click()
                user_click()
                if (winner != "" or draw == True):
                    reset_game()
                #print("got here!!")
        pygame.display.update()
        timer.tick(fps)

def quitgame():
    pygame.quit()

def text_objects(text, font):
    textSurface = font.render(text, True, (white))
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',75)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((WIDTH/2),(HEIGHT/2))
    game_display.blit(TextSurf, TextRect,)

def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)

        titleText = gameDisplay.blit(x_img, (170, 200))    # title is an image
        titleText.center = ((WIDTH / 2), (HEIGHT / 2))

        # button(msg, x, y, w, h, inactive, active, action=None)
        button("PLAY", 50, 350, 98, 40, green, bright_green, game_loop)
        button("Quit",275,350,98,40,red,bright_red,quitgame)

        pygame.display.update()
        timer.tick(15)
#you can call this menu above your game loop.


def button(msg, x, y, w, h, inactive, active, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, active,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(gameDisplay, inactive,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)



game_intro()
