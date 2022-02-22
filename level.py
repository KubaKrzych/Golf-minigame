import csv
import time

from settings import *
import pygame
from objects import *


class Level:

    def __init__(self, num):
        """

        :param num:
        """
        # Setup
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.get_surface()
        file = self.read_csv('Other/Map_{}.csv'.format(num))

        # Images
        background = pygame.image.load('Images/level_{}_background.png'.format(num)).convert_alpha()
        self.options_img = pygame.image.load('Images/options_background.png').convert_alpha()

        # Instances
        self.prev_time = time.time()
        self.level_number = num
        self.hit_count = 0
        self.first_run = True
        self.hole_pos = None
        self.highscore = None
        self.end = False
        self.ball_in_hole = False
        self.coin_picked = False

        # Sprites
        self.player = pygame.sprite.GroupSingle()
        self.hole = pygame.sprite.GroupSingle()
        self.coin = pygame.sprite.GroupSingle()
        self.flag = pygame.sprite.GroupSingle()
        self.obstacles = pygame.sprite.Group()
        self.cosmetic = pygame.sprite.Group()
        self.cosmetic.add(Cosmetic((0, 0), background))

        for row in range(len(file)):
            for col in range(len(file[0])):
                if file[row][col] == 'P':
                    self.ball = Player((col * TILE, row * TILE))
                    self.player.add(self.ball)
                elif file[row][col] == 'B':
                    self.obstacles.add(Block('B', (col * TILE, row * TILE), num))
                elif file[row][col] == 'G':
                    self.obstacles.add(Block('G', (col * TILE, row * TILE), num))
                # `rect.hole` checks whether hole position was already given
                elif file[row][col] == 'H':
                    self.obstacles.add(Block('B', (col * TILE, row * TILE), num))
                    if not self.hole_pos:
                        self.hole_pos = (col * TILE, row * TILE)
                elif file[row][col] == 'C':
                    self.coin.add(Coin((col * TILE, row * TILE)))
                elif file[row][col] == 'W':
                    self.obstacles.add(Block('W', (col * TILE, row * TILE), num))
                elif row == col == 0:
                    self.obstacles.add(Block('W', (col * TILE, row * TILE), num))
                else:
                    continue
        self.get_highscore()
        self.flag.add(Flag(num, (self.hole_pos[0] + TILE, self.hole_pos[1])))

    def run(self):
        if self.first_run:
            self.start_level()
            self.first_run = False
            self.prev_time = time.time()  # Due to fade, removing this could lead to a bug

        # Check for ball in hole, if so, delete all objects and set highscore
        if self.end:
            return self.end_level()

        # Input handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_all()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.options()
                if event.key == pygame.K_r:
                    self.__init__(self.level_number)

        mouse_buttons = pygame.mouse.get_pressed()

        # Delta time
        now = time.time()
        dt = now - self.prev_time
        self.prev_time = now

        # Drawing surfaces
        self.draw()

        # Processes
        self.process_coin()
        self.update_all(self.obstacles, self.player, dt, mouse_buttons, self.end)
        pygame.event.pump()
        pygame.display.update()

        return True

    def process_coin(self):
        if not self.coin_picked:

            # Player picks up a coin
            if self.coin.sprite.rect.colliderect(self.player.sprite.rect):
                self.coin_picked = True
                self.coin.sprite.kill()

                # Kill blocks in hole position, create and open up a hole
                for obs in self.obstacles:  # Search for blocks at position of the hole
                    if obs.rect.topleft == self.hole_pos or \
                            obs.rect.topleft == (self.hole_pos[0] + TILE, self.hole_pos[1]):
                        obs.kill()
                self.hole.add(Hole(self.hole_pos))
        else:
            # If coin is picked and player is standing on the bottom edge of the hole block -> game ends
            if Block.get_bottom(self.hole.sprite.rect, 2 * TILE, 10).colliderect(self.player.sprite.rect) \
                    and not self.player.sprite.in_move:
                self.ball_in_hole = True
                self.end = True

    def draw(self):
        self.cosmetic.draw(self.screen)
        self.hole.draw(self.screen)
        self.obstacles.draw(self.screen)
        self.coin.draw(self.screen)
        self.flag.draw(self.screen)
        self.player.draw(self.screen)
        if self.level_number == 3:
            self.draw_panel((WIDTH - 250, 100), "{} hits".format(self.ball.hit_count))
        else:
            self.draw_panel((WIDTH / 2, 100), "{} hits".format(self.ball.hit_count))
        debug(length(self.ball.vector))

    def update_all(self, obstacle_group, player_group, delta_time, mouse_but, end):
        self.player.update(obstacle_group, player_group, delta_time, mouse_but, end)
        self.flag.update()
        self.coin.update(player_group)
        self.hole.update(self.coin_picked)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.__init__(self.level_number)
                if event.key == pygame.K_ESCAPE:
                    self.options()
            if event.type == pygame.QUIT:
                quit_all()

    def summary_screen(self):
        new_highscore = self.set_highscore()
        while True:
            self.screen.fill('Black')
            if new_highscore:
                self.draw_panel((WIDTH/2, HEIGHT/2 - 100),
                                "  New best score!  ")
                self.draw_panel((WIDTH/2, HEIGHT/2 + 100), " {} hits ".format(self.highscore))
            else:
                self.draw_panel((WIDTH/2, HEIGHT/2 - 100), " Highscore {} ".format(self.highscore))
                self.draw_panel((WIDTH/2, HEIGHT/2 + 100), " Your score {} ".format(self.ball.hit_count))

            text_blit("Press any key to continue...", WIDTH/2, HEIGHT - 100, 'White')
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    return
                if event.type == pygame.QUIT:
                    quit_all()
            pygame.display.update()

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

            self.screen.blit(self.options_img, (0,0))
            self.screen.blit(options_text, options_rect)

            # Main menu button
            if menu_rect.collidepoint(pygame.mouse.get_pos()):
                text_blit('MAIN MENU', WIDTH/2, HEIGHT - 200, 'Cyan')
                if pygame.mouse.get_pressed()[0]:
                    self.end = True  # User goes back to main menu
                    break
            else:
                text_blit('MAIN MENU', WIDTH / 2, HEIGHT - 200, 'White')

            pygame.display.update()

    # Screen fades away if the ball is in hole, but if the ball is not in hole
    # then the frame simply changes (user went back to main menu)
    def end_level(self):
        if self.ball_in_hole:
            # TODO stop theme music
            pygame.mixer.music.load('Other/hole_sound.wav')
            pygame.mixer.music.play(0)
            fade = pygame.Surface((WIDTH, HEIGHT))
            fade.fill(('Black'))
            for alpha in range(255):
                fade.set_alpha(alpha)
                self.draw()
                self.screen.blit(fade, (0, 0))
                pygame.display.update()

                # Prevents unnecessary waiting for screen to fully fade
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit_all()

                pygame.time.delay(5)
            self.summary_screen()
        self.delete_all()
        return False

    # Fade in
    def start_level(self):
        fade = pygame.Surface((WIDTH, HEIGHT))
        fade.fill(('Black'))
        for alpha in range(255, 0, -1):
            fade.set_alpha(alpha)
            self.draw()
            self.screen.blit(fade, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_all()
            pygame.display.update()

    def get_highscore(self):
        try:
            with open('Other/hs.txt', 'r') as file:
                lines = file.readlines()
                self.highscore = int(lines[self.level_number - 1].strip())

        # The file doesn't exist
        except IOError:
            with open('Other/hs.txt', 'w') as file:
                file.write("32000\n32000\n32000\n")
                self.highscore = 32000

    # If score is smaller than "highscore", then it writes to a file
    # Returns 1 if new best score, 0 if not
    def set_highscore(self):
        if self.ball.hit_count < self.highscore and self.ball_in_hole:
            self.highscore = self.ball.hit_count
            with open('Other/hs.txt', 'r') as file:
                score = file.readlines()
                file.close()
            score = [i.strip() for i in score]
            score[self.level_number - 1] = str(self.highscore)
            with open('Other/hs.txt', 'w') as file:
                for i in score:
                    file.write(str(i) + "\n")
                file.close()
            return 1
        return 0

    def draw_panel(self, position: tuple, text: str, color='White'):
        panel_background = pygame.image.load('Images/panel.png')
        text_surf = FONT.render(text, False, color)
        text_rect = text_surf.get_rect(center=position)
        # -5 and + 10 are given due to a border
        x, y = text_rect.x - 30, text_rect.y - 30
        width, height = text_rect.width + 60, text_rect.height + 60
        panel_background = pygame.transform.scale(panel_background, (width, height))
        self.screen.blit(panel_background, (x, y))
        self.screen.blit(text_surf, text_rect)

    # Read rows in csv file
    @staticmethod
    def read_csv(path):
        file = open(path)
        csvreader = csv.reader(file, delimiter=';')
        rows = []
        for row in csvreader:
            rows.append(row)
        return rows

    # Deletes all objects in level
    def delete_all(self):
        del self.player
        del self.obstacles
        del self.hole
        del self.cosmetic
        del self
