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
width = 600
height = 600
board = [0]*3, [0]*3, [0]*3

grayColor = (230, 230, 230)
blackColor = (0, 0, 0)
