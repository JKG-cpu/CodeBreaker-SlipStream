import pygame

from pygame.math import Vector2 as vector
from pytmx.util_pygame import load_pygame
from pytmx import TiledMap
from sys import exit as close_game
from os import system, name, listdir
from os.path import join, isdir, basename

# Variables
SCREEN_W, SCREEN_H = 1600, 960
TILE_SIZE = 32
PLAYER_SCALE = 2

# Functions
def cc():
    system("cls" if name == "nt" else "clear")

def load_and_crop(path, size=32):
    image = pygame.image.load(path).convert_alpha()
    
    x = (image.get_width() - size) // 2
    y = (image.get_height() - size) // 2

    cropped = image.subsurface(pygame.Rect(x, y, size, size)).copy()
    return cropped

def scale_and_crop(scale: int, path):
    image = load_and_crop(path, 32)
    return pygame.transform.scale(
        image,
        (image.get_width() * scale, image.get_height() * scale)
    )

def import_image(*path):
    image_path = join(*path)
    return pygame.image.load(image_path).convert_alpha()

def scale_image(scale: int, *path):
    image = import_image(*path)
    return pygame.transform.scale(
        image, (image.get_width() * scale, image.get_height() * scale)
    )

def import_images(*parent_folder):
    folder = join(*parent_folder)
    imgs = []

    for item in listdir(folder):
        new_path = join(folder, item)
        if not isdir(new_path):
            imgs.append(scale_and_crop(PLAYER_SCALE, new_path))

    return imgs

def import_character(*head_folder):
    top_folder = join(*head_folder)
    frames = {}

    for item in listdir(top_folder):
        new_path = join(top_folder, item)
        if isdir(new_path):
            frames[basename(new_path)] = import_images(new_path)
    
    return frames
