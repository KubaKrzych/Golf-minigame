import math
import pygame
from functions import *
from settings import *
from debug import debug


class Player(pygame.sprite.Sprite):

    def __init__(self, position: tuple):
        super().__init__()
        # Images and sounds
        frame_1 = pygame.image.load('Images/ball_1.png')
        frame_2 = pygame.image.load('Images/ball_2.png')
        frame_3 = pygame.image.load('Images/ball_3.png')
        self.image_index = 0
        self.radius = TILE
        self.frames = [frame_1, frame_2, frame_3]
        self.sounds = {"strong_hit": None,
                       "light_hit": None,
                       "swing": None,
                       }
        self.image = frame_1

        # Instances
        self.vector = [0, 0]
        self.rect = self.image.get_rect(center=position)
        self.click_pos = None

        # States
        self.in_air = True
        self.in_move = True

    def user_input(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: #  and self.in_move is False
                    self.click_pos = event.pos
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.hit(event.pos)
                    self.in_move = True
                    self.click_pos = None

    def find_angle_of_collision(self):
        pass

    def gravity(self):
        if self.in_air:
            self.vector[1] += 2

    # In radians
    #   [1, 0] for x-axis
    def current_angle(self):
        result = angle(self.vector, [1, 0])
        if self.vector[0] > 0 and self.vector[1] > 0: # 1st quarter
            pass
        elif self.vector[0] < 0 < self.vector[1]: # 2nd quarter
            result += math.radians(90)
        elif self.vector[0] > 0 > self.vector[1]: # 4th quarter
            result += 3 * math.radians(90)
        else: # 3rd quarter
            result += 2 * math.radians(90)
        return result

    # TODO this works awfully
    def move(self):
        if self.in_air:
            self.rect.y += self.vector[1]
            self.gravity()
        if self.in_move:
            if abs(self.vector[0]) < 2 and not self.in_air:
                self.in_move = False
            else:
                self.rect.x += self.vector[0]

    def update(self, obstacle_list):
        self.user_input()
        self.collide(obstacle_list)
        self.move()
        self.draw_vector()
        self.animation()

    def animation(self):
        if self.in_move:
            self.image_index += 0.1
            if self.image_index >= len(self.frames):
                self.image_index = 0
            self.image = self.frames[int(self.image_index)]

    # This function probably can be written much cleaner
    def collide(self, obstacle_list: bool):
        # for obstacle in obstacle_list:
        if not obstacle_list:
            return
        rect = obstacle_list.get_rect()

        # Rozna zmniejszenia wektora w zaleznosci od bloku
        # if self.rect.midright[0] >= obstacle_rect

        if rect.midtop[1] <= self.rect.midbottom[1] <= self.rect.bottomleft[1] <= self.rect.bottomright[1]:
            self.vector[1] = self.vector[1] // 2 * (-1)
            self.rect.y = rect.midtop[1] - TILE + 1
            self.check_air()
        elif rect.midbottom[1] >= self.rect.midtop[1] >= self.rect.topleft[1] >= self.rect.topright[1]:
            self.vector[1] = self.vector[1] // 2 * (-1)
            self.rect.y = rect.midtop[1] - TILE + 1
            self.check_air()
        elif rect.midleft[0] <= self.rect.midleft[0] <= self.rect.topleft[0] <= self.rect.bottomleft[0]:
            self.vector[0] *= -1
        elif rect.midright[0] >= self.rect.midright[0] >= self.rect.topright[0] >= self.rect.bottomright[0]:
            self.vector[0] *= -1
        else:
            print('error')

    def in_hole(self):
        pass

    def draw_vector(self):
        if self.click_pos:
            display = pygame.display.get_surface()
            mouse_pos = pygame.mouse.get_pos()
            pygame.draw.line(display, 'White', self.rect.center, (
                mouse_pos[0], mouse_pos[1]), 5)

    def check_air(self):
        if self.in_air and abs(self.vector[1]) < 3:
            self.in_air = False
            self.vector[1] = 0

    def hit(self, lmp_release_pos):
        v = vector_decomposition(self.click_pos, lmp_release_pos)
        self.vector[0] = v[0]
        self.vector[1] = v[1]
        self.check_air()

class Block(pygame.sprite.Sprite):
    def __init__(self, type_of_block, position: tuple):
        super().__init__()
        if type_of_block == 'B':
            self.image = pygame.image.load('Images/wood.png')
        elif type_of_block == 'W':
            self.image = pygame.image.load('Images/wall.png')
        elif type_of_block == 'G':
            self.image = pygame.image.load('Images/ground.png')
        else:
            self.image = None
        self.rect = self.image.get_rect(topleft=position)

    def get_rect(self):
        return self.rect


class Hole(pygame.sprite.Sprite):
    def __init__(self, position: tuple,):
        super().__init__()
        self.image = pygame.image.load('Images/hole.png')
        self.rect = self.image.get_rect(topleft=position)


class Cosmetic(pygame.sprite.Sprite):
    def __init__(self, position: tuple, img_path):
        super().__init__()
        self.image = pygame.image.load(img_path)
        self.rect = self.image.get_rect(topleft=position)
