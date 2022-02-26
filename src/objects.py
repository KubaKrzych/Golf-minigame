from math import cos, sin, radians

import pygame.mixer_music

from src.misc.functions import *
from Data.settings import *
from os import path, getcwd


class Player(pygame.sprite.Sprite):

    def __init__(self, position: tuple):
        """

        :param position:
        """
        super().__init__()

        # Images and sounds
        frame_1 = pygame.image.load(getcwd() + '/Images/Ball/ball_1.png')
        frame_2 = pygame.image.load(getcwd() + '/Images/Ball/ball_2.png')
        frame_3 = pygame.image.load(getcwd() + '/Images/Ball/ball_3.png')
        pygame.mixer.set_num_channels(10)
        self.image_index = 0
        self.screen = pygame.display.get_surface()
        self.frames = [frame_1, frame_2, frame_3]
        self.image = frame_1
        self.sounds = {"strong_hit": pygame.mixer.Sound(getcwd() + '/Audio/strong_hit.wav'),
                       "light_hit": pygame.mixer.Sound(getcwd() + '/Audio/light_hit.wav'),
                       "hard_bounce": pygame.mixer.Sound(getcwd() + '/Audio/hard_bounce.wav'),
                       "mid_bounce":  pygame.mixer.Sound(getcwd() + '/Audio/mid_bounce.wav'),
                       "light_bounce": pygame.mixer.Sound(getcwd() + '/Audio/light_bounce.wav'),
                       "ball_roll": pygame.mixer.Sound(getcwd() + '/Audio/ball_roll.wav')
                       }
        pygame.mixer.Channel(0).set_volume(0.3)

        # Instances
        self.rect = self.image.get_rect(topleft=position)
        self.vector = [0, 0]
        self.click_pos = None
        self.iterations = 10
        self.hit_count = 0
        self.rest_x = 0
        self.rest_y = 0
        self.rolls = False

        # States
        self.in_air = True
        self.in_move = True
        self.in_collision = False

    def user_input(self, mouse_buttons):
        if mouse_buttons[0] and not self.in_move and self.in_collision and not self.click_pos:
            self.click_pos = pygame.mouse.get_pos()
        if self.click_pos and not mouse_buttons[0]:
            self.hit(pygame.mouse.get_pos())

    def gravity(self):
        if self.in_air and length(self.vector) < MAX_SPEED:
            self.vector[1] += GRAVITY

    def current_angle_of_move(self):
        result = angle(self.vector, [1, 0])  # [1, 0] for x-axis normal vector
        quarter = vector_quarter(self.vector)
        if quarter > 2:
            result = radians(360) - result
        return result

    def move(self, delta_time):
        t = delta_time * FPS
        if self.in_move:
            pygame.time.delay(1)  # The movement is not as fast when delayed by 1ms

            if self.in_air:
                self.rect.y += self.vector[1] * t / self.iterations

                # Code below makes vertical movement much more smooth
                self.rest_y += self.vector[1] * t / self.iterations % 1
                self.rect.y += self.rest_y // 1
                self.rest_y = self.rest_y - self.rest_y // 1

            else:
                self.rest_y = 0
                if self.rolls is False:
                    pygame.mixer.Channel(0).play(self.sounds["ball_roll"])
                    self.rolls = True

            self.rect.x += self.vector[0] * t / self.iterations
            # Code below makes horizontal movement much more smooth
            self.rest_x += self.vector[0] * t / self.iterations % 1
            self.rect.x += self.rest_x // 1
            self.rest_x = self.rest_x - self.rest_x // 1

        else:
            self.rest_x = 0
            self.rolls = False

    def update(self, obstacle_group, player_group, delta_time, mouse_buttons, end):
        self.user_input(mouse_buttons)
        self.draw_vector()
        self.check_movement()
        if self.in_move:
            self.gravity()
            for i in range(self.iterations):
                self.move(delta_time)
                self.collide(obstacle_group, player_group)
                self.check_movement()
                self.animation()

    def animation(self):
        if self.in_move:
            self.image_index += 0.1
            if self.image_index >= len(self.frames):
                self.image_index = 0
            self.image = self.frames[int(self.image_index)]

    def collide(self, obstacle_group, player_group):
        player = player_group.sprite
        obstacles = pygame.sprite.spritecollide(player, obstacle_group, False)

        # No collision
        if len(obstacles) == 0:
            self.in_collision = False
            return

        # If the ball touches the ground it decelerates
        if not self.in_air and self.in_move:
            self.vector[0] /= MOVE_QUANTITY
        print(obstacles)
        for obstacle in obstacles:
            obstacle_rect = obstacle.rect

            # Ball hits the block from the top
            if Block.get_top(obstacle_rect, 16, 8).colliderect(Block.get_bottom(self.rect, 22, 12)) and self.vector[1] > 0:
                self.vector[1] = self.vector[1] // Y_QUANTITY * (-1)
                self.vector[0] /= QUANTITY
                self.rect.y = obstacle_rect.y - TILE + 1
                self.in_collision = True  # The ball is on the ground
                self.bounce_sound(False)

            # Ball hits the block from the bottom
            if Block.get_bottom(obstacle_rect, 16, 8).colliderect(Block.get_top(self.rect, 22, 12)) and self.vector[1] < 0:
                self.vector[1] = self.vector[1] // Y_QUANTITY * (-1)
                self.vector[0] /= QUANTITY
                self.rect.y = obstacle_rect.y + TILE + 1
                self.bounce_sound(False)

            # Ball hits the block from the left
            if Block.get_left(obstacle_rect, 16, 8).colliderect(Block.get_right(self.rect, 22, 12)) and self.vector[0] > 0:
                self.vector[0] = self.vector[0] // X_QUANTITY * (-1)
                self.vector[1] /= QUANTITY
                self.rect.x = obstacle_rect.x - TILE - 6
                self.bounce_sound(True)

            # Ball hits the block from the right
            if Block.get_right(obstacle_rect, 16, 8).colliderect(Block.get_left(self.rect, 22, 12)) and self.vector[0] < 0:
                self.vector[0] = self.vector[0] // X_QUANTITY * (-1)
                self.vector[1] /= QUANTITY
                self.rect.x = obstacle_rect.x + TILE + 6
                self.bounce_sound(True)
            # TODO Obczaic rogi i wtedy odbic zmienic kierunek obu wektorow

    def draw_vector(self):
        # The statement below is up for a make-over
        if self.click_pos is not None and \
                distance(self.click_pos, pygame.mouse.get_pos()) > HIT_QUANTITY * MIN_VECTOR_LENGTH:
            mouse_pos = pygame.mouse.get_pos()

            # TODO mam funkcje po to co ponizej
            vector = (self.click_pos[0] - mouse_pos[0], self.click_pos[1] - mouse_pos[1])

            if length(vector) >= MAX_VECTOR_LENGTH * HIT_QUANTITY:
                vector_angle = inverted_angle(vector, [1, 0])
                end_pos = (self.rect.centerx - cos(vector_angle) * MAX_VECTOR_LENGTH * HIT_QUANTITY,
                           self.rect.centery - sin(vector_angle) * MAX_VECTOR_LENGTH * HIT_QUANTITY)
                pygame.draw.line(self.screen, 'Red', self.rect.center,
                                 end_pos, 3)
            else:
                end_pos = (self.rect.centerx - vector[0], self.rect.centery - vector[1])
                pygame.draw.line(self.screen, (10 + length(vector)//10, 255 - length(vector)//3, 10), self.rect.center,
                                 end_pos, 3)

    def check_movement(self):
        if not self.in_collision:
            self.in_air = True
            pygame.mixer.Channel(0).stop()

        elif self.in_collision and abs(self.vector[1]) <= self.iterations:
            self.vector[1] = 0
            self.in_air = False

        if not self.in_air and self.in_collision and abs(self.vector[0]) <= self.iterations / 2:
            self.vector[0] = 0
            self.in_move = False
            pygame.mixer.Channel(0).stop()

        elif not self.in_air and not self.in_collision:
            self.in_move = True

    def bounce_sound(self, side_collision: bool):
        # Played sounds depend on current state, side_collision is True if ball hits a block from the left or right
        if self.in_air:
            if length(self.vector) >= HARD_BOUNCE_VECTOR_LEN:
                pygame.mixer.Channel(3).play(self.sounds["hard_bounce"])
            elif length(self.vector) >= MID_BOUNCE_VECTOR_LEN:
                pygame.mixer.Channel(3).play(self.sounds["mid_bounce"])
            else:
                pygame.mixer.Channel(3).play(self.sounds["light_bounce"])
        else:
            if side_collision:
                if length(self.vector) >= HARD_BOUNCE_VECTOR_LEN:
                    pygame.mixer.Channel(3).play(self.sounds["hard_bounce"])
                elif length(self.vector) >= MID_BOUNCE_VECTOR_LEN:
                    pygame.mixer.Channel(3).play(self.sounds["mid_bounce"])
                else:
                    pygame.mixer.Channel(3).play(self.sounds["light_bounce"])

    def hit(self, lmb_release_pos):
        v = vector_decomposition(lmb_release_pos, self.click_pos)
        self.vector[0] = v[0] // HIT_QUANTITY
        self.vector[1] = v[1] // HIT_QUANTITY

        # Length of the vector between self.click_pos and mouse_pos is too small
        if length(self.vector) < MIN_VECTOR_LENGTH:
            self.click_pos = None
            self.vector = [0, 0]
            return

        # Maximum length of the vector
        elif length(self.vector) >= MAX_VECTOR_LENGTH:
            # Pure math, don't bother if trigonometry is hell to you
            self.vector[0] = cos(self.current_angle_of_move()) * MAX_VECTOR_LENGTH
            self.vector[1] = sin(self.current_angle_of_move()) * MAX_VECTOR_LENGTH
        if length(self.vector) >= STRONG_HIT_VECTOR_LEN:
            pygame.mixer.Channel(1).play(self.sounds["strong_hit"])
        else:
            pygame.mixer.find_channel(1).play(self.sounds["light_hit"])

        self.hit_count += 1
        self.click_pos = None
        self.in_air = True
        self.in_move = True


class Block(pygame.sprite.Sprite):
    def __init__(self, type_of_block, position: tuple, num: int):
        super().__init__()
        if type_of_block == 'B':
            self.image = pygame.image.load('Images/Blocks/block_{}.png'.format(num))
        elif type_of_block == 'W':
            self.image = pygame.image.load('Images/Blocks/wall_{}.png'.format(num))
        elif type_of_block == 'G':
            self.image = pygame.image.load('Images/Blocks/ground_{}.png'.format(num))
        else:
            self.image = None
        self.rect = self.image.get_rect(topleft=position)

    def get_rect(self):
        return self.rect

    # The functions below let you take a slice of block from a specific side

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
    def __init__(self, position: tuple):
        super().__init__()
        self.image = pygame.image.load(getcwd() + '/Images/Hole/hole.png')
        self.rect = self.image.get_rect(topleft=position)


class Cosmetic(pygame.sprite.Sprite):
    def __init__(self, position: tuple, img):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect(topleft=position)


class Coin(pygame.sprite.Sprite):
    def __init__(self, position: tuple):
        super().__init__()
        frame_1 = pygame.image.load(getcwd() + '/Images/Coin/coin_1.png')
        self.frames = [frame_1]
        i = 2
        while path.exists('Images/Coin/coin_{}.png'.format(i)):
            self.frames.append(pygame.image.load('Images/Coin/coin_{}.png'.format(i)).convert_alpha())
            i += 1

        self.image = frame_1
        self.rect = self.image.get_rect(topleft=position)
        self.picked = False
        self.animation_index = 0

    def animation(self):
        self.animation_index += 0.25
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
            self.image = self.frames[0]
        else:
            self.image = self.frames[int(self.animation_index)]

    def update(self, player_group):
        if not self.picked:
            self.animation()
        else:
            del self


class Flag(pygame.sprite.Sprite):
    def __init__(self, num, midtop_hole_pos):
        super().__init__()
        frame_1 = pygame.image.load(getcwd() + '\Images\Flags\level_{}_flag_1.png'.format(num)).convert_alpha()
        self.frames = [frame_1]
        i = 2
        while path.exists(getcwd() + '\Images\Flags\level_{}_flag_{}.png'.format(num, i)):
            self.frames.append(pygame.image.load(getcwd() + '\Images\Flags\level_{}_flag_{}.png'.format(num, i)).convert_alpha())
            i += 1

        self.image = frame_1
        self.rect = self.image.get_rect(midbottom=midtop_hole_pos)
        self.animation_index = 0

    def animation(self):
        self.animation_index += 0.05
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation()
