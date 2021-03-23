import sys
import pygame
from pygame import mixer
from time import sleep

from bullet import Bullet
from alien import Alien


def check_events(ai_settings, screen, stats, sb, menu, ship, aliens, bullets):
    """ Respond to key presses and mouse events. """
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_menu(ai_settings, screen, stats, sb, menu, ship,
                       aliens, bullets, mouse_x, mouse_y)
        elif event.type == pygame.QUIT:
            save_and_quit(stats)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen,
                                 stats, sb, menu, ship, bullets, aliens)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_keydown_events(event, ai_settings, screen, stats, sb, menu, ship, bullets, aliens):
    """ Responds to keypresses. """
    if event.key == pygame.K_p:
        if not stats.game_active:
            start_new_game(ai_settings, screen, stats,
                           sb, ship, bullets, aliens)
        elif stats.game_active and not stats.game_paused:
            pause_game(stats, menu)
        elif stats.game_active and stats.game_paused:
            unpause_game(stats, menu)

    elif event.key == pygame.K_ESCAPE:
        if stats.game_paused:
            unpause_game(stats, menu)
        elif not stats.game_paused:
            pause_game(stats, menu)

    elif event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True

    elif event.key == pygame.K_SPACE and stats.game_active:
        fire_bullet(ai_settings, screen, ship, bullets)

    elif event.key == pygame.K_q:
        save_and_quit(stats)


def check_keyup_events(event, ship):
    """ Reponds to key releases. """
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_menu(ai_settings, screen, stats, sb, menu, ship, aliens,
               bullets, mouse_x, mouse_y):
    """Start a new game when the player clicks Play."""

    button_clicked = menu.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        start_new_game(ai_settings, screen, stats, sb, ship, bullets, aliens)


def start_new_game(ai_settings, screen, stats, sb, ship, bullets, aliens):
    """ Reset game and start new game. """

    play_bg_music(ai_settings)
    # Reset game speed metrics
    ai_settings.initialize_dynamic_settings()
    # Hide the mouse cursor
    pygame.mouse.set_visible(False)
    # Reset the game stats, scoreboard and ship images.
    stats.reset_stats()
    sb.prep_images()
    stats.game_active = True
    stats.game_ended = False
    aliens.empty()
    bullets.empty()
    # Create a new fleet and center the ship
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()


def play_bg_music(ai_settings):
    """ Play background music when game is running. """
    pygame.mixer.music.set_volume(ai_settings.med_volume)
    bg_music = pygame.mixer.music.load('./resources/sound/bg_music.mp3')
    pygame.mixer.music.play(-1)


def pause_game(stats, menu):
    """ Pauses the game. """
    stats.game_paused = True
    pygame.mixer.music.pause()


def unpause_game(stats, menu):
    """ Pauses the game. """
    stats.game_paused = False
    pygame.mixer.music.unpause()


def stop_bg_music():
    """ Stop background music when game ends. """
    pygame.mixer.music.stop()


def save_and_quit(stats):
    """ Save high score and the quit game. """
    game_data = './resources/data/high_score.txt'

    with open(game_data, 'w') as f_object:
        hs = int(stats.high_score)
        f_object.write(str(hs))

    sys.exit()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, menu):
    """ Uptades images on a the screen and flips to the new screen. """
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()

    # Redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():  # returns a list of all sprites in group
        bullet.draw_bullet()

    # Draw the play button if the game is inactive
    if not stats.game_active and not stats.game_paused and not stats.game_ended:
        menu.draw_menu(stats)
    if stats.game_paused and stats.game_active:
        menu.draw_menu(stats)
    if stats.game_ended:
        menu.draw_menu(stats)

    # Make the most recently drawn screen visible
    pygame.display.flip()


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in the row."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    alien.rect.x = alien.x
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    # Create an alien and find the number of aliens in a row
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)
    # Create the fleet of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,
                         row_number)


def update_aliens(ai_settings, stats, sb, menu, screen, ship, aliens, bullets):
    """ Check if the fleet is at an edge,
    and then update the postions of all aliens in the fleet. """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, sb, menu,
                 screen, ship, aliens, bullets)


def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def check_aliens_bottom(ai_settings, stats, sb, menu, screen, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit
            ship_hit(ai_settings, stats, sb, menu,
                     screen, ship, aliens, bullets)
            break


def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_bullets(ai_settings, screen, stats, sb, menu, ship, aliens, bullets):
    """ Update position of bullets and get rid of old bullets. """

    # Update bullet positon
    bullets.update()

    # Get rid of bullets that have dissapeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(
        ai_settings, screen, stats, sb, ship, aliens, bullets)
    # Look for aliens hitting the bottom of the screen
    check_aliens_bottom(ai_settings, stats, sb, menu,
                        screen, ship, aliens, bullets)


def fire_bullet(ai_settings, screen, ship, bullets):
    """ Fire a bullet if limit not reached yet. """
    fire_sfx = pygame.mixer.Sound('./resources/sound/shoot.wav')
    fire_sfx.set_volume(ai_settings.low_volume)

    # Create a new bullet and add it to the bullets group
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        pygame.mixer.Sound.play(fire_sfx)
        bullets.add(new_bullet)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for bullet in collisions:
            for alien in collisions[bullet]:
                stats.score += (alien.points *
                                ai_settings.alien_score_multiplier)
                sb.prep_score()
        check_high_scores(ai_settings, stats, sb)

    if len(aliens) == 0:
        # If the entire fleet is destroyed, start a new level.
        start_new_level(ai_settings, screen, stats, sb, ship, aliens, bullets)


def start_new_level(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """ Starts a new level. """
    next_level_sfx = pygame.mixer.Sound('./resources/sound/next_level.wav')
    next_level_sfx.set_volume(ai_settings.med_volume)

    bullets.empty()
    ai_settings.increase_speed()
    stats.level += 1
    sb.prep_level()
    pygame.mixer.Sound.play(next_level_sfx)
    create_fleet(ai_settings, screen, ship, aliens)


def check_high_scores(ai_settings, stats, sb):
    """ Check to see if there's anew high score. """

    new_hs_sfx = pygame.mixer.Sound('./resources/sound/high_score.wav')
    new_hs_sfx.set_volume(ai_settings.med_volume)
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        if stats.high_score_achieved:
            pass
        else:
            pygame.mixer.Sound.play(new_hs_sfx)
            stats.high_score_achieved = True
        sb.prep_high_score()


def ship_hit(ai_settings, stats, sb, menu, screen, ship, aliens, bullets):
    """Respond to ship being hit by alien."""

    ship_hit_sfx = pygame.mixer.Sound('./resources/sound/ship_hit.wav')
    game_over_sfx = pygame.mixer.Sound('./resources/sound/game_over.wav')
    game_over_sfx.set_volume(ai_settings.med_volume)
    ship_hit_sfx.set_volume(ai_settings.low_volume)
    # Play ship hit sfx
    pygame.mixer.Sound.play(ship_hit_sfx)

    if stats.ships_left > 0:
        # Decrement ships_left
        stats.ships_left -= 1
        sb.prep_ships()
        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()
        # Create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        sleep(0.5)
    else:
        stats.game_active = False
        stats.game_ended = True
        pygame.mouse.set_visible(True)
        stop_bg_music()
        pygame.mixer.Sound.play(game_over_sfx)
