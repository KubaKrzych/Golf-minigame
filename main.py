import sys
import pygame
from settings import *
from objects import *
from level import Level


class Golf:

    def __init__(self):

        # Setup
        pygame.init()
        pygame.display.set_caption("Golf minigame")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.font = pygame.font.Font('Other/pixelart.ttf', 60)
        self.background = pygame.image.load('Images/title_screen.png').convert_alpha()
        # Variables
        self.running = True
        self.level = None
        self.level_n = None

        # Configure level
        self.paths = {
                      "level_1_banner": 'Images/level_1_banner.png',
                      "level_2_banner": 'Images/level_2_banner.png',
                      "level_3_banner": 'Images/level_3_banner.png',
                      }
        self.clock = pygame.time.Clock()

    def run(self):
        while self.running:

            if self.level_n:
                self.running = self.level.run()
            else:
                self.title_screen()

            # Player input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_all()

            # End frame
            self.clock.tick(FPS)
            pygame.event.pump()
            pygame.display.update()

    def title_screen(self):
        # Level 1
        level_1 = FONT.render("LEVEL 1", False, 'Black')
        rect_1 = level_1.get_rect(center=(WIDTH / 2, 450))
        level_1_banner = pygame.image.load(self.paths["level_1_banner"]).convert_alpha()

        # Level 2
        level_2 = FONT.render("LEVEL 2", False, 'White')
        rect_2 = level_2.get_rect(center=(WIDTH/2, 550))
        level_2_banner = pygame.image.load(self.paths["level_2_banner"]).convert_alpha()

        # Level 3
        level_3 = FONT.render("LEVEL 3", False, 'White')
        rect_3 = level_3.get_rect(center=(WIDTH/2, 650))
        level_3_banner = pygame.image.load(self.paths["level_3_banner"]).convert_alpha()

        rectangle_width, rectangle_height = rect_1.width + 5, rect_1.height + 15

        # Title
        title = TITLE.render("GOLF GAME", False, 'White')
        title_surf = title.get_rect(center=(WIDTH/2, 200))

        while True:
            self.screen.blit(self.background, (0, 0))
            dark = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()
            dark.fill((0, 0, 0, 100))
            self.screen.blit(dark, dark.get_rect())  # Darkens the image
            self.screen.blit(title, title_surf)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_all()
                if event.type == pygame.KEYDOWN:
                    pass

            # First level
            level_background = pygame.rect.Rect(rect_1.x - 5, rect_1.y - 5, rectangle_width, rectangle_height)
            self.screen.blit(pygame.transform.scale(level_1_banner, (rectangle_width, rectangle_height)),
                             level_background)
            self.screen.blit(level_1, rect_1)
            if rect_1.collidepoint(pygame.mouse.get_pos()):
                # Mouse collides with rect
                level_1 = FONT.render("LEVEL 1", False, (225,90,120))
                rect_1 = level_1.get_rect(center=(WIDTH/2, 450))
                pygame.draw.rect(self.screen, (225,90,120), level_background, 4)
                if pygame.mouse.get_pressed()[0]:
                    self.running = True
                    self.level_n = 1
                    self.level = Level(self.level_n)
                    self.run()
            else:
                # Mouse doesn't collide with rect
                level_1 = FONT.render("LEVEL 1", False, (175,50,60))
                self.screen.blit(level_1, rect_1)
                pygame.draw.rect(self.screen, (175,50,60), level_background, 4)

            # Second level
            level_background = pygame.rect.Rect(rect_2.x - 5, rect_2.y - 5, rectangle_width, rectangle_height)
            self.screen.blit(pygame.transform.scale(level_2_banner, (rectangle_width, rectangle_height)),
                             level_background)
            self.screen.blit(level_2, rect_2)
            if rect_2.collidepoint(pygame.mouse.get_pos()):
                # Mouse collides with rect
                level_2 = FONT.render("LEVEL 2", False, (15, 150, 255))
                rect_2 = level_2.get_rect(center=(WIDTH / 2, 550))
                pygame.draw.rect(self.screen, (15, 150, 255), level_background, 4)
                if pygame.mouse.get_pressed()[0]:
                    self.running = True
                    self.level_n = 2
                    self.level = Level(self.level_n)
                    self.run()
            else:
                # Mouse doesn't collide with rect
                level_2 = FONT.render("LEVEL 2", False, (25, 75, 130))
                self.screen.blit(level_2, rect_2)
                pygame.draw.rect(self.screen, (25, 75, 130), level_background, 4)

            # Third level
            level_background = pygame.rect.Rect(rect_3.x - 5, rect_3.y - 5, rectangle_width, rectangle_height)
            self.screen.blit(pygame.transform.scale(level_3_banner, (rectangle_width, rectangle_height)),
                             level_background)
            self.screen.blit(level_3, rect_3)
            if rect_3.collidepoint(pygame.mouse.get_pos()):
                # Mouse collides with rect
                level_3 = FONT.render("LEVEL 3", False, (55, 255, 90))
                rect_3 = level_3.get_rect(center=(WIDTH / 2, 650))
                pygame.draw.rect(self.screen, (55, 255, 90), level_background, 4)
                if pygame.mouse.get_pressed()[0]:
                    self.running = True
                    self.level_n = 3
                    self.level = Level(self.level_n)
                    self.run()
            else:
                # Mouse doesn't collide with rect
                level_3 = FONT.render("LEVEL 3", False, (20, 200, 80))
                self.screen.blit(level_3, rect_3)
                pygame.draw.rect(self.screen, (20, 200, 80), level_background, 4)

            pygame.display.update()


if __name__ == "__main__":
    game = Golf()
    game.run()
