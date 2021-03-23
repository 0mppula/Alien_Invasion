import pygame
from pygame.sprite import Group


from settings import Settings
import game_functions as gf
from game_stats import GameStats
from scoreboard import Scoreboard
from menu import Menu
from ship import Ship


def run_game():
    # Initialize game and create a screen object
    pygame.init()

    ai_settings = Settings()
    stats = GameStats(ai_settings)
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')

    sb = Scoreboard(ai_settings, screen, stats)
    # Make the Play button
    menu = Menu(ai_settings, screen, stats)

    # Make a ship, a group of bullets, and a group of aliens
    ship = Ship(ai_settings, screen)
    aliens = Group()
    bullets = Group()

    # Create the fleet of aliens
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Start the main loop of the game
    while True:

        gf.check_events(ai_settings, screen, stats, sb,
                        menu, ship, aliens, bullets)

        if stats.game_active and not stats.game_paused:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, menu,
                              ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, sb, menu,
                             screen, ship, aliens, bullets)

        gf.update_screen(ai_settings, screen, stats, sb, ship,
                         aliens, bullets, menu)


run_game()
