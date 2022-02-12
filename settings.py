import pygame
pygame.init()

# Basic settings
WIDTH = 1280
HEIGHT = 800
FPS = 60
TARGET_FPS = 60
TILE = 32

# Game variables
HIT_QUANTITY = 12.5  # Hit strength is divided by this value
Y_QUANTITY = 4  # Whenever the ball hits a block from the top or bottom, it's Y vector is divided by this value
X_QUANTITY = 2  # Whenever the ball hits a block from the left or right, it's X vector is divided by this value
QUANTITY = 1.1  # Opposite to the above, if the ball hits a block from the right, it's Y vector is divided
MOVE_QUANTITY = 1.0025  # If the ball moves on the ground, divide it's X vector by this value

# Font
FONT = pygame.font.Font('pixelart.ttf', 60)
TITLE = pygame.font.Font('pixelart.ttf', 95)

