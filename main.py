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
        self.font = pygame.font.Font('pixelart.ttf', 60)

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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and self.level:
                        self.level.options()
                    if event.key == pygame.K_r and self.level:
                        self.level = Level(self.level_n)
            # End frame
            self.clock.tick(FPS)
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
            self.screen.fill((20, 60, 60))
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
                level_1 = FONT.render("LEVEL 1", False, 'Cyan')
                rect_1 = level_1.get_rect(center=(WIDTH/2, 450))
                if pygame.mouse.get_pressed()[0]:
                    self.running = True
                    self.level_n = 1
                    self.level = Level(self.level_n)
                    self.run()
            else:
                level_1 = FONT.render("LEVEL 1", False, (0, 75, 160))
                self.screen.blit(level_1, rect_1)
                pygame.draw.rect(self.screen, (0, 75, 160), level_background, 4)

            # Second level
            self.screen.blit(level_2, rect_2)
            level_background = pygame.rect.Rect(rect_2.x - 5, rect_2.y - 5, rectangle_width, rectangle_height)
            self.screen.blit(pygame.transform.scale(level_2_banner, (rectangle_width, rectangle_height)),
                             level_background)
            if rect_2.collidepoint(pygame.mouse.get_pos()):
                level_2 = FONT.render("LEVEL 2", False, 'Cyan')
                rect_2 = level_2.get_rect(center=(WIDTH / 2, 550))
                if pygame.mouse.get_pressed()[0]:
                    self.running = True
                    self.level_n = 2
                    self.level = Level(self.level_n)
                    self.run()
            else:
                level_2 = FONT.render("LEVEL 2", False, 'White')
                self.screen.blit(level_2, rect_2)
                pygame.draw.rect(self.screen, (0, 75, 160), level_background, 4)

            # Third level
            self.screen.blit(level_3, rect_3)
            level_background = pygame.rect.Rect(rect_3.x - 5, rect_3.y - 5, rectangle_width, rectangle_height)
            self.screen.blit(pygame.transform.scale(level_3_banner, (rectangle_width, rectangle_height)),
                             level_background)
            if rect_3.collidepoint(pygame.mouse.get_pos()):
                level_3 = FONT.render("LEVEL 3", False, 'Cyan')
                rect_3 = level_3.get_rect(center=(WIDTH / 2, 650))
                if pygame.mouse.get_pressed()[0]:
                    self.running = True
                    self.level_n = 3
                    self.level = Level(self.level_n)
                    self.run()
            else:
                level_3 = FONT.render("LEVEL 3", False, 'White')
                self.screen.blit(level_3, rect_3)
                pygame.draw.rect(self.screen, (0, 75, 160), level_background, 4)

            pygame.display.update()


if __name__ == "__main__":
    game = Golf()
    game.run()
