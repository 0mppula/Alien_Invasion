import os


class GameStats():
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_settings):
        """Initialize statistics."""
        self.ai_settings = ai_settings
        self.game_active = False
        self.game_paused = False
        self.game_ended = False

        self.high_score = self.get_high_score()
        self.reset_stats()

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.ai_settings.ship_limit
        self.level = 1
        self.high_score_achieved = False
        self.score = 0

    def get_high_score(self):
        """ Check if old high score data is present else high score is 0 """
        highscore_file = './resources/data/high_score.txt'

        try:
            with open(highscore_file) as f_object:
                if os.stat(highscore_file).st_size > 0:
                    high_score = f_object.read()
                    return int(high_score)

        except FileNotFoundError:
            high_score = 0
            return int(high_score)

        else:
            high_score = 0
            return int(high_score)
