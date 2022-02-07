import math


def distance(from_pos: tuple, to_pos: tuple):
    return ((from_pos[0]-to_pos[0])**2 + (from_pos[1]-to_pos[1])**2)**(1/2)


def vector_decomposition(from_pos: tuple, to_pos: tuple):
    return to_pos[0] - from_pos[0], to_pos[1] - from_pos[1]


def dot_product(v1, v2):
    return sum((a*b) for a, b in zip(v1, v2))


def length(v):
    return math.sqrt(dot_product(v, v))


# angle in radians
def angle(v1, v2):
    if v1[1] != 0:
        return math.acos(dot_product(v1, v2) / (length(v1) * length(v2)))
    else:
        return 0


# Depending on the vector, returns the angle quarter -1
def vector_quarter(v):
    if v[0] > 0 and v[1] > 0:
        return 0
    elif v[1] > 0 > v[0]:
        return 1
    elif v[0] > 0 > v[1]:
        return 3
    else:
        return 2
