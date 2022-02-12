import time

import pygame.mouse

from functions import *
from settings import *
from debug import debug


class Player(pygame.sprite.Sprite):

    def __init__(self, position: tuple):
        super().__init__()
        # Images and sounds
        self.screen = pygame.display.get_surface()
        frame_1 = pygame.image.load('Images/ball_1.png')
        frame_2 = pygame.image.load('Images/ball_2.png')
        frame_3 = pygame.image.load('Images/ball_3.png')
        self.image_index = 0
        self.radius = TILE
        self.frames = [frame_1, frame_2, frame_3]
        self.image = frame_1
        self.sounds = {"strong_hit": None,
                       "light_hit": None,
                       "swing": None,
                       }

        # Instances
        self.vector = [0, 0]
        self.rect = self.image.get_rect(topleft=position)
        self.click_pos = None
        self.collision_tolerance = 3
        self.iters = 10
        self.gravity_force = 4
        self.rest_x = 0
        self.rest_y = 0

        # States
        self.in_air = True
        self.in_move = True
        self.in_collision = False

    def user_input(self, delta_time, mouse_buttons):
        if mouse_buttons[0] and not self.in_move and self.in_collision and not self.click_pos:
            self.click_pos = pygame.mouse.get_pos()
        if self.click_pos and not mouse_buttons[0]:
            self.hit(pygame.mouse.get_pos(), delta_time)

    def find_angle_of_collision(self):
        pass

    def gravity(self, delta_time):
        if self.in_air:
            self.vector[1] += self.gravity_force

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

    def move(self, delta_time):
        t = delta_time * FPS
        if self.in_air:
            self.rect.y += self.vector[1] * t / self.iters
            # Code below makes vertical movement much more smooth
            self.rest_y += self.vector[1] * t / self.iters % 1
            self.rect.y += self.rest_y // 1
            self.rest_y = self.rest_y - self.rest_y // 1
        else:
            self.rest_y = 0
        if self.in_move:
            self.rect.x += self.vector[0] * t / self.iters
            # Code below makes horizontal movement much more smooth
            self.rest_x += self.vector[0] * t / self.iters % 1
            self.rest_x = self.rest_x - self.rest_x // 1
        else:
            self.rest_x = 0

    def update(self, obstacle_group, player_group, delta_time, mouse_buttons):
        self.user_input(delta_time, mouse_buttons)
        self.draw_vector()
        self.collide(obstacle_group, player_group)
        if self.in_move:
            self.gravity(delta_time)
            for i in range(self.iters):
                self.move(delta_time)
                self.collide(obstacle_group, player_group)
                self.check_movement()
                self.animation()
        player_group.draw(self.screen)

        debug(f"air:{self.in_air},   move:{self.in_move},   col:{self.in_collision}")
        debug(f"{self.vector},  {self.rect.x, self.rect.y}", 40)
        debug(f"{self.click_pos},  {pygame.mouse.get_pos()}", 70)
        debug(f"{pygame.mouse.get_pressed()}", 100)

    def animation(self):
        if self.in_move:
            self.image_index += 0.1
            if self.image_index >= len(self.frames):
                self.image_index = 0
            self.image = self.frames[int(self.image_index)]

    def collide(self, obstacle_group, player_group):
        # TODO Rozna zmniejszenia wektora w zaleznosci od bloku
        player = player_group.sprite
        obstacles = pygame.sprite.spritecollide(player, obstacle_group, False)

        if len(obstacles) == 0:
            self.in_collision = False
            return
        if not self.in_air and self.in_move:
            self.vector[0] /= MOVE_QUANTITY

        for obstacle in obstacles:
            rect = obstacle.get_rect()
            self.in_collision = True

            if Block.get_top(rect, 16, 8).colliderect(Block.get_bottom(self.rect, 24, 12)) and self.vector[1] > 0:
                self.vector[1] = self.vector[1] // Y_QUANTITY * (-1)
                self.vector[0] /= QUANTITY
                self.rect.y = rect.y - TILE + 1
            elif Block.get_bottom(rect, 16, 8).colliderect(Block.get_top(self.rect, 24, 12)) and self.vector[1] < 0:
                self.vector[1] = self.vector[1] // Y_QUANTITY * (-1)
                self.vector[0] /= QUANTITY
                self.rect.y = rect.y + TILE + 1
            elif Block.get_left(rect, 16, 8).colliderect(Block.get_right(self.rect, 24, 12)) and self.vector[0] > 0:
                self.vector[0] = self.vector[0] // X_QUANTITY * (-1)
                self.vector[1] /= QUANTITY
                self.rect.x = rect.x - TILE - 1
            elif Block.get_right(rect, 16, 8).colliderect(Block.get_left(self.rect, 24, 12)) and self.vector[0] < 0:
                self.vector[0] = self.vector[0] // X_QUANTITY * (-1)
                self.vector[1] /= QUANTITY
                self.rect.x = rect.x + TILE + 1
            # TODO Obczaic rogi i wtedy odbic zmienic kierunek obu wektorow

    def in_hole(self):
        pass

    def draw_vector(self):
        pass
        # if self.click_pos is not None:
        #     mouse_pos = pygame.mouse.get_pos()
        #     ball_pos = self.rect.center
        #     quarter = vector_quarter([mouse_pos[0]-ball_pos[0], mouse_pos[1]-ball_pos[0]])
        #     print(quarter)
        #     if quarter == 1:
        #         pygame.draw.line(self.screen, 'Black', ball_pos,
        #                          ball_pos[0] + mouse_pos[0] % 200, ball_pos[1] + mouse_pos[1] % 200)

    def check_movement(self):
        if not self.in_collision:
            self.in_air = True
        elif self.in_collision and abs(self.vector[1]) <= self.iters:
            self.vector[1] = 0
            self.in_air = False

        if not self.in_air and self.in_collision and abs(self.vector[0]) <= self.iters / 2:
            self.vector[0] = 0
            self.in_move = False

    def hit(self, lmp_release_pos, delta_time):
        v = vector_decomposition(lmp_release_pos, self.click_pos)
        self.vector[0] = v[0] // HIT_QUANTITY
        self.vector[1] = v[1] // HIT_QUANTITY
        self.click_pos = None
        self.in_air = True
        self.in_move = True


class Block(pygame.sprite.Sprite):
    def __init__(self, type_of_block, position: tuple, num: int):
        super().__init__()
        if type_of_block == 'B':
            self.image = pygame.image.load('Images/block_{}.png'.format(num))
        elif type_of_block == 'W':
            self.image = pygame.image.load('Images/wall_{}.png'.format(num))
        elif type_of_block == 'G':
            self.image = pygame.image.load('Images/ground_{}.png'.format(num))
        else:
            self.image = None
        self.rect = self.image.get_rect(topleft=position)

    def get_rect(self):
        return self.rect

    @staticmethod
    def get_left(rect, width, height):
        return pygame.rect.Rect(rect.x, rect.y + TILE/2 - height/2, height, width)

    @staticmethod
    def get_right(rect, width, height):
        return pygame.rect.Rect(rect.x + TILE - width, rect.y + TILE/2 - height/2, height, width)

    @staticmethod
    def get_top(rect, width, height):
        return pygame.rect.Rect(rect.x + TILE/2 - width/2, rect.y, width, height)

    @staticmethod
    def get_bottom(rect, width, height):
        return pygame.rect.Rect(rect.x + TILE / 2 - width/2, rect.y + TILE, width, height)


class Hole(pygame.sprite.Sprite):
    def __init__(self, position: tuple,):
        super().__init__()
        self.image = pygame.image.load('Images/hole.png')
        self.rect = self.image.get_rect(topleft=position)


class Cosmetic(pygame.sprite.Sprite):
    def __init__(self, position: tuple, img):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect(topleft=position)
