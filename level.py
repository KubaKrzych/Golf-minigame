import csv
import time

from settings import *
import pygame
from objects import *


class Level:
    def __init__(self, num):
        # Setup
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.get_surface()
        file = self.level_setup('Other/Map_{}.csv'.format(num))

        # Images
        background = pygame.image.load('Images/level_{}_background.png'.format(num)).convert_alpha()

        # Instances
        self.prev_time = time.time()
        self.score = 0

        # Sprites
        self.player = pygame.sprite.GroupSingle()
        self.hole = pygame.sprite.GroupSingle()
        self.obstacles = pygame.sprite.Group()
        self.cosmetic = pygame.sprite.Group()

        self.cosmetic.add(Cosmetic((0, 0), background))
        for row in range(len(file)):
            for col in range(len(file[0])):
                if file[row][col] == 'P':
                    self.player.add(Player((col * TILE, row * TILE)))
                elif file[row][col] == 'B':
                    self.obstacles.add(Block('B', (col * TILE, row * TILE), num))
                elif file[row][col] == 'G':
                    self.obstacles.add(Block('G', (col * TILE, row * TILE), num))
                # `rect.hole` checks whether hole position was already given
                elif file[row][col] == 'H' and not self.hole:
                    self.hole.add(Hole((col * TILE, row * TILE)))
                elif row == col == 0:
                    self.obstacles.add(Block('W', (col * TILE, row * TILE), num))
                elif file[row][col] == 'W':
                    self.obstacles.add(Block('W', (col * TILE, row * TILE), num))
                else:
                    continue

    @staticmethod
    def level_setup(path):
        file = open(path)
        csvreader = csv.reader(file, delimiter=';')
        rows = []
        for row in csvreader:
            rows.append(row)
        return rows

    def run(self):
        mouse_buttons = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_all()
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_ESCAPE:
                    # Level.options()
                    pass

        # Delta time
        now = time.time()
        dt = now - self.prev_time
        self.prev_time = now

        # Drawing surfaces
        self.cosmetic.draw(self.screen)
        self.obstacles.draw(self.screen)
        self.hole.draw(self.screen)

        # Processes
        self.player.update(self.obstacles, self.player, dt, mouse_buttons)
        if self.player.sprite.rect.colliderect(self.hole.sprite.rect) and not self.player.sprite.in_move:
            print(123)
        self.clock.tick(FPS)


    @staticmethod
    def options():
        screen = pygame.display.get_surface()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_all()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
            screen.fill((20, 60, 60))
            text_blit('OPTIONS', WIDTH/2, 200, 'White')
            pygame.display.update()