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

#board details
width = 800
height = 800
board = [0]*3, [0]*3, [0]*3

grayColor = (230, 230, 230)
blackColor = (0, 0, 0)

#initialize all pygame functionalities
pg.init()

game_display = pg.display.set_mode((width, height))
pg.display.update()