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
        self.end = False
        self.ball_in_hole = False

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

    def run(self):
        # Check for ball in hole, if so, delete all objects
        if self.end:
            return self.end_level()

        # Input handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_all()
        mouse_buttons = pygame.mouse.get_pressed()

        # Delta time
        now = time.time()
        dt = now - self.prev_time
        self.prev_time = now

        # Drawing surfaces
        self.draw()

        # Processes
        if Block.get_bottom(self.hole.sprite.rect, 2*TILE, 10).colliderect(self.player.sprite.rect) \
                and not self.player.sprite.in_move:
            self.ball_in_hole = True
            self.end = True
        self.player.update(self.obstacles, self.player, dt, mouse_buttons, self.end)
        pygame.display.update()
        return True

    def draw(self):
        self.cosmetic.draw(self.screen)
        self.obstacles.draw(self.screen)
        self.hole.draw(self.screen)
        self.player.draw(self.screen)

    def options(self):
        menu_rect = text_blit('MAIN MENU', WIDTH/2, HEIGHT - 200, 'White')
        options_text = TITLE.render("OPTIONS", False, "White")
        options_rect = options_text.get_rect(center=(WIDTH/2, 200))
        while True:
            # Input handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_all()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

            self.screen.fill((20, 60, 60))
            self.screen.blit(options_text, options_rect)

            # Main menu button
            if menu_rect.collidepoint(pygame.mouse.get_pos()):
                text_blit('MAIN MENU', WIDTH/2, HEIGHT - 200, 'Cyan')
                if pygame.mouse.get_pressed()[0]:
                    self.end = True
                    break  # TODO Tutaj musi byc inne wyjscie, bez fade away
            else:
                text_blit('MAIN MENU', WIDTH / 2, HEIGHT - 200, 'White')

            pygame.display.update()

    # Screen fades away if the ball is in hole, but if the ball is not in hole
    # then the frame simply changes (user went back to main menu)
    def end_level(self):
        if self.ball_in_hole:
            fade = pygame.Surface((WIDTH, HEIGHT))
            fade.fill(('White'))
            for alpha in range(255):
                fade.set_alpha(alpha)
                self.draw()
                self.screen.blit(fade, (0, 0))
                pygame.display.update()
                pygame.time.delay(5)

        del self.player
        del self.obstacles
        del self.hole
        del self.cosmetic
        del self
        return False

    @staticmethod
    def level_setup(path):
        file = open(path)
        csvreader = csv.reader(file, delimiter=';')
        rows = []
        for row in csvreader:
            rows.append(row)
        return rows
