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

        # Configure level
        self.paths = {"level_1": 'Other/Map.csv'}
        self.clock = pygame.time.Clock()

    def run(self):
        level = Level(self.paths["level_1"])
        while True:
            level.run()
            # Player input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.options()
                    if event.key == pygame.K_r:
                        pass # Restart level
            # End frame
            self.clock.tick(FPS)
            pygame.display.update()

    def level(self):
        pass

    def restart(self):
        pass

    def title_screen(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN:
                    pass
            self.screen.fill((20, 60, 60))
            self.text_blit('GOLF GAME', (WIDTH / 2, 200), 'White')
            pygame.display.update()

    def options(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
            self.screen.fill((20, 60, 60))
            self.text_blit('OPTIONS', (WIDTH/2, 200), 'White')
            pygame.display.update()

    @staticmethod
    def quit():
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Golf()
    game.run()
