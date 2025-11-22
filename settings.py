import pygame

from pygame.math import Vector2 as vector
from sys import exit as close_game
from os import system, name

# Variables
SCREEN_W, SCREEN_H = 1400, 750
GRAVITY = 2
MAX_FALLING_SPEED = 10

# Functions
def cc():
    system("cls" if name == "nt" else "clear")