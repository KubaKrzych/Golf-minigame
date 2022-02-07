import csv
from settings import *
import pygame
from objects import *


class Level:
    def __init__(self, path):
        self.score = 0
        file = self.level_setup(path)
        # Sprites
        self.player = pygame.sprite.GroupSingle()
        self.hole = pygame.sprite.GroupSingle()
        self.obstacles = pygame.sprite.Group()
        self.cosmetic = pygame.sprite.Group()

        for row in range(len(file)):
            for col in range(len(file[0])):
                if file[row][col] == 'P':
                    self.player.add(Player((col * TILE, row * TILE)))
                elif file[row][col] == 'B':
                    self.obstacles.add(Block('B', (col * TILE, row * TILE)))
                elif file[row][col] == 'G':
                    self.obstacles.add(Block('G', (col * TILE, row * TILE)))
                # `self.hole` checks whether hole position was already given
                elif file[row][col] == 'H' and not self.hole:
                    self.hole.add(Hole((col * TILE, row * TILE)))
                elif row == col == 0:
                    self.obstacles.add(Block('W', (col * TILE, row * TILE)))
                elif file[row][col] == 'W':
                    self.obstacles.add(Block('W', (col * TILE, row * TILE)))
                else:
                    continue
        self.cosmetic.add(Cosmetic((0, 0), 'Images/background.png'))

    @staticmethod
    def level_setup(path):
        file = open(path)
        csvreader = csv.reader(file, delimiter=';')
        rows = []
        for row in csvreader:
            rows.append(row)
        return rows

    def run(self):
        screen = pygame.display.get_surface()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        # Drawing surfaces
        self.cosmetic.draw(screen)
        self.obstacles.draw(screen)
        self.hole.draw(screen)
        self.player.draw(screen)

        # Processes
        self.player.update(self.player_collision())

    # Potentially, can be removed so that player related stuff is handled inly in Player class
    def player_collision(self):
        return pygame.sprite.spritecollideany(self.player.sprite, self.obstacles)

