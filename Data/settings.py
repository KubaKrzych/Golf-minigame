import math
import os

import pygame
pygame.init()

# Basic settings
WIDTH = 1280
HEIGHT = 800
FPS = 60
TARGET_FPS = 60
TILE = 32

# Game variables
HIT_QUANTITY = 8.5  # Hit strength is divided by this value
Y_QUANTITY = 2  # Whenever the ball hits a block from the top or bottom, it's Y vector is divided by this value
X_QUANTITY = 1.5  # Whenever the ball hits a block from the left or right, it's X vector is divided by this value
QUANTITY = 1.1  # Opposite to the above, if the ball hits a block from the right, it's Y vector is divided
MOVE_QUANTITY = 1.002  # If the ball moves on the ground, divide it's X vector by this value
MAX_VECTOR_LENGTH = 65  # Max length of move vector, 65 is the golden mean
MIN_VECTOR_LENGTH = 8
GRAVITY = 4  # Gravity force
STRONG_HIT_VECTOR_LEN = 40  # When the length of the vector is 40 or above, other sfx will play
LIGHT_BOUNCE_VECTOR_LEN = 50
MID_BOUNCE_VECTOR_LEN = 35
HARD_BOUNCE_VECTOR_LEN = 20
MAX_SPEED = 70

# Font
FONT = pygame.font.Font(os.getcwd() + '\Data\Fonts\pixelart.ttf', 60)
TITLE = pygame.font.Font(os.getcwd() + '\Data\Fonts\pixelart.ttf', 95)

# Colors

