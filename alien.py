import pygame
from pygame.sprite import Sprite
from random import randint


class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_settings, screen):
        """ Initialize the alien and set its starting position. """
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load(self.get_color())
        self.rect = self.image.get_rect()
        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # Store the alien's exact position.
        self.x = float(self.rect.x)

    def update(self):
        """Move the alien right or left."""
        self.x += (self.ai_settings.alien_speed_factor *
                   self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True

        elif self.rect.left <= 0:
            return True

    def get_color(self):
        """ Set color random color for alien. """
        colors = ['./resources/images/alien_blue.bmp',
                  './resources/images/alien_red.bmp', './resources/images/alien_green.bmp']
        random_index = randint(0, len(colors)-1)
        alien_color = colors[random_index]
        self.set_alien_points(alien_color)
        return alien_color

    def set_alien_points(self, color):
        """ Determines score of alien based on alien color. """
        if color == './resources/images/alien_green.bmp':
            self.points = 100
        elif color == './resources/images/alien_blue.bmp':
            self.points = 150
        elif color == './resources/images/alien_red.bmp':
            self.points = 200

    def blitme(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.image, self.rect)
