import sys, pygame
from settings import *
from objects import *


class Golf:

    def __init__(self):
        # Setup
        pygame.init()
        pygame.display.set_caption("Golf minigame")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.images = {"hole": 'Images/hole (2).png',
                       "background": 'Images/background_sky.png',
                       "golf_ball" : 'Images/golfball.png'}
        self.font = pygame.font.Font('pixelart.ttf', 60)
        self.background = pygame.image.load('Images/background_sky.png').convert()

        # Instances
        self.player = Ball((200, 400), self.images["golf_ball"])
        self.hole = Object((0, 400), self.images["hole"])

        # Variables
        self.score = 0
        self.clock = pygame.time.Clock()

    def text_blit(self, text, destination: tuple):
        text_surface = self.font.render(text, False, 'black')
        self.screen.blit(text_surface, destination)

    def run(self):
        while True:

            # Static images
            self.screen.fill('Black')
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.hole.get_image(), self.hole.get_rect())

            # Player input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        print('restart')
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.player.mouse_pos_1:
                    vectors = Ball.eucl_dist_and_vectors(event.pos, self.player.mouse_pos_1)
                    self.player.vector[0] = vectors[1]
                    self.player.vector[1] = vectors[2]
                    self.player.mouse_pos_1 = None
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.player.mouse_pos_1 = event.pos

            # Ball movement
            if self.player.get_rect().midleft[0] < 0 or self.player.get_rect().midright[0] >= WIDTH:
                pass
            if self.player.get_rect().midbottom[1] <= 0 or self.player.get_rect().midtop[1] >= HEIGHT:
                pass
            if self.player.mouse_pos_1:
                pygame.draw.line(self.screen, 'Black', self.player.get_rect().center, pygame.mouse.get_pos(), 2)

            # Collision handling
            if self.hole.get_rect().colliderect(self.player.get_rect()):
                pass

            # Window
            self.player.move()
            self.screen.blit(self.player.get_image(), self.player.get_rect())

            # End frame
            self.text_blit(str(self.score), (20,20))
            self.clock.tick(FPS)
            pygame.display.update()


if __name__ == "__main__":
    game = Golf()
    game.run()
