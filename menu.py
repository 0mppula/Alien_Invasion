import pygame.font
from button import Button


class Menu():

    def __init__(self, ai_settings, screen, stats):
        """ Initialize menu attributes. """
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Size and color
        self.width = 600
        self.height = 400
        self.bg_color = (45, 53, 89)
        self.text_color = (226, 188, 0)
        self.font = pygame.font.SysFont(None, 48)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Prep message
        self.prep_msg(stats)

        # Create Play button
        self.play_button = Button(ai_settings, screen, stats)

    def prep_text(self, stats):
        """ Determine the apropriate menu messgae based on gamestate. """
        if not stats.game_active and not stats.game_paused and not stats.game_ended:
            self.msg = 'Alien Invasion'
        elif stats.game_active and stats.game_paused:
            self.msg = 'Paused'
        elif stats.game_ended:
            self.msg = 'Gameover'

    def prep_msg(self, stats):
        """ Turn the message into a rendered image. """
        self.prep_text(stats)
        self.msg_image = self.font.render(
            self.msg, True, self.text_color, self.bg_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.screen_rect.center
        self.msg_image_rect.y = self.rect.center[1] - \
            (110 if stats.game_ended else 70)

        if stats.game_ended:
            self.prep_score_msg(stats)

    def prep_score_msg(self, stats):
        """ Add score to menu screen. """
        rounded_score = int(round(stats.score, -1))
        score_str = str(f'{rounded_score:,}')
        self.score_msg = f'Your score: {score_str}'
        self.score_msg_image = self.font.render(
            self.score_msg, True, self.text_color, self.bg_color)
        self.score_msg_image_rect = self.score_msg_image.get_rect()
        self.score_msg_image_rect.center = self.rect.center
        self.score_msg_image_rect.y = (self.rect.center[1] - 60)

    def draw_menu(self, stats):
        """ Draw the menu on screen. """
        self.prep_msg(stats)
        self.screen.fill(self.bg_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

        if stats.game_ended:
            self.screen.blit(self.score_msg_image, self.score_msg_image_rect)

        self.play_button.draw_button(stats)
