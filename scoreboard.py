import pygame.font
from pygame.sprite import Group

from ship import Ship


class Scoreboard():
    """ A class to report the scoring information. """

    def __init__(self, ai_settings, screen, stats):
        """ Initialize scorekeeping attributes. """

        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # Font settings for scoring information
        self.text_color = (226, 188, 0)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial score images
        self.prep_images()

    def prep_score(self):
        """ Turn the score into a rendered image. """
        rounded_score = int(round(self.stats.score, -1))
        score_str = str(f'{rounded_score:,}')
        self.score_image = self.font.render(
            score_str, True, self.text_color, self.ai_settings.bg_color)

        # Display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """ Turn the highscore into a rendered image. """
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = str(f'{high_score:,}')
        self.high_score_image = self.font.render(
            high_score_str, True, self.text_color, self.ai_settings.bg_color)

        # Center the high score at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """ Turn the level into a rendered image. """
        self.level_image = self.font.render(
            str(self.stats.level), True, self.text_color, self.ai_settings.bg_color)

        # Postition the level below the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """ Show how many ships are left. """
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + (ship_number * (ship.rect.width + 3))
            ship.rect.y = 10
            self.ships.add(ship)

    def prep_images(self):
        """ Turn score, high score, level and ships left into rendered images. """
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def show_score(self):
        """ Draw the scores and ships to the screen. """
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
