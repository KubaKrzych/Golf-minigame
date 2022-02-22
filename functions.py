import math
import sys
from settings import *


# euclidean distance
def distance(from_pos: tuple, to_pos: tuple):
    return ((from_pos[0]-to_pos[0])**2 + (from_pos[1]-to_pos[1])**2)**(1/2)


def vector_decomposition(from_pos: tuple, to_pos: tuple):
    return to_pos[0] - from_pos[0], to_pos[1] - from_pos[1]


# dot product of two vectors
def dot_product(v1, v2):
    return sum((a*b) for a, b in zip(v1, v2))


# length of a vector
def length(v):
    return math.sqrt(dot_product(v, v))


# angle in radians between two vectors
def angle(v1, v2):
    if v1[1] != 0:
        return math.acos(dot_product(v1, v2) / (length(v1) * length(v2)))
    else:
        return 0


# Angle between vectors in pygame framework
def inverted_angle(v1, v2):
    quarter = vector_quarter(v1)
    result = angle(v1, v2)
    if quarter > 2:
        return math.radians(360) - result
    return result


# Depending on the vector, returns the angle quarter -1
def vector_quarter(v):
    if v[0] > 0 and v[1] > 0:
        return 1
    elif v[0] < 0 < v[1]:
        return 2
    elif v[0] < 0:
        return 3
    else:
        return 4


# blit text on display using FONT from settings
def text_blit(text, x, y, color='Black'):
    display = pygame.display.get_surface()
    text = FONT.render(text, False, color)
    text_rect = text.get_rect(center=(x, y))
    display.blit(text, text_rect)
    return text_rect


def quit_all():
    pygame.quit()
    sys.exit()

