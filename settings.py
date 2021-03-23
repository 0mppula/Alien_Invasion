class Settings():
    """ A class to store all settings for 'Alien Invasion'. """

    def __init__(self):
        """ Initialize game's static settings. """
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (20, 20, 20)

        # Sound Settings
        self.high_volume = 1
        self.med_volume = 0.5
        self.low_volume = 0.25
        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = (250, 10, 10)
        self.bullets_allowed = 3

        # Alien settings
        self.fleet_drop_speed = 10

        # How quickly the game speeds up
        self.alien_speed_scale = 1.1
        self.ship_speed_scale = 1.05
        self.alien_score_multiplier = 1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """ Initialize game's dynamic settings. """
        self.ship_speed_factor = 1.10
        self.bullet_speed_factor = 1.55
        self.alien_speed_factor = 0.4
        # fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 0.4

    def increase_speed(self):
        """ Increment levels speed and scoring. """
        self.ship_speed_factor *= self.ship_speed_scale
        self.bullet_speed_factor *= self.ship_speed_scale
        self.alien_speed_factor *= self.alien_speed_scale
        self.alien_score_multiplier *= 1.5
