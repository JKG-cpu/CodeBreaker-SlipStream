import pygame

from pygame.math import Vector2 as vector
from pytmx.util_pygame import load_pygame
from sys import exit as close_game
from os import system, name
from os.path import join

# Variables
SCREEN_W, SCREEN_H = 1400, 750
TILE_SIZE = 32

# Functions
def cc():
    system("cls" if name == "nt" else "clear")