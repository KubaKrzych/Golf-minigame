import pygame
from math import sqrt


class Object:

    def __init__(self, position: tuple, picture_path):
        self.position = position
        self.picture = pygame.image.load(picture_path).convert_alpha()
        self.rect = self.picture.get_rect(midleft=self.position)

    def get_image(self):
        return self.picture

    def get_rect(self):
        return self.rect


class Ball(Object):

    def __init__(self, position: tuple, picture_path):
        super().__init__(position, picture_path)
        self.vector = [0, 0]
        self.mouse_pos_1 = None
        self.air = True

    def move(self):
        if self.air:
            self.vector[1] += 1
        if self.vector[0] > 1 or self.vector[0]*(-1) > 1:
            self.get_rect().x += self.vector[0] // 25
            self.vector[0] /= 10
        else:
            self.vector[0] = 0
        if self.vector[1] >= 1 or self.vector[1]*(-1) >= 1:
            self.get_rect().y += self.vector[1] // 25
        else:
            self.vector[1] = 0

    @staticmethod
    def eucl_dist_and_vectors(from_pos: tuple, to_pos: tuple):
        return (sqrt(pow(from_pos[0]-to_pos[0], 2) + pow(from_pos[1] - to_pos[1],2)), to_pos[0] -
                from_pos[0], to_pos[1] - from_pos[1])

