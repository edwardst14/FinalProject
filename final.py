#Python Final Project
#Start Date: 11/02/20

import pygame as pg
import sys 
import time 
from pygame.locals import *

#GLOABAL VARIABLES
winner = ""
draw = ""

XO = "x"

#board detail variables
WIDTH = 750
HEIGHT = 600
board = [0]*3, [0]*3, [0]*3

gray = (230, 230, 230)
white = (250, 250, 250)
black = (0, 0, 0)

#initialize all pygame functionalities
pg.init()

game_display = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Tic-Tac-Toe")

#########################################################################################
#may delete if not functioning properly
def toggle_fullscreen(game_display):
    if toggle_fullscreen:
        game_display = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    else:
        game_display = pg.display.set_mode((WIDTH, HEIGHT))
##########################################################################################

def event_handler():
    for ev in pg.event.get():
        #print(ev)
        if ev.type == QUIT or (
            ev.type == KEYDOWN and (
                ev.key == K_ESCAPE or
                ev.key == K_q
            )):
            pg.quit()
            quit()

def draw_lines():
    pg.draw.line(game_display, white, [250,0], [250, 600], 2)
    pg.draw.line(game_display, white, [500,0], [500, 600], 2)
    pg.draw.line(game_display, white, [0,200], [750, 200], 2)
    pg.draw.line(game_display, white, [0,400], [750, 400], 2)

###########################################################################################
#main game loop
#toggle_fullscreen(game_display)

while True:
    #start = pg.time.get_ticks()

    event_handler()

    pg.display.update()

    draw_lines()

    #end = pg.time.get_ticks()

    #totalTime = end-start
