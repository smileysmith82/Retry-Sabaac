import random
import pygame
import showdown as show

def start_dice_roll(game):   
    game.die1 = random.randint(1,6)
    game.die2 = random.randint(1,6)

    game.dice_rolling = True
    game.dice_roll_start = pygame.time.get_ticks()
    game.dice_animation_last_change = game.dice_roll_start

    game.display_die1 = random.randint(1,6)
    game.display_die2 = random.randint(1,6)
    
def update_dice(game, current_time):
    if not game.dice_rolling:
        return

    elapsed = current_time - game.dice_roll_start

    if current_time - game.dice_animation_last_change >= 60:
        game.display_die1 = random.randint(1,6)
        game.display_die2 = random.randint(1,6)
        game.dice_animation_last_change = current_time

    if elapsed >= game.dice_roll_duration:
        game.dice_rolling = False
        game.display_die1 = game.die1
        game.display_die2 = game.die2
        finish_dice_roll(game)
    

def finish_dice_roll(game):
    game.dice_matched = (game.die1 == game.die2)
    game.phase = game.DICE_RESULT_PHASE
    game.dice_result_start = pygame.time.get_ticks()

def update_dice_result(game, current_time):

    if game.phase != game.DICE_RESULT_PHASE:
        return

    if current_time - game.dice_result_start < 1000:
        return

    game.rounds_played += 1

    if game.dice_matched:
        game.reset_hands()

    game.current_index = (game.dealer_index + 1) % len(game.players)

    
    if game.rounds_played >= game.rounds_per_game:
        show.start_showdown(game)

    else:
        game.phase = game.TURN_PHASE
        game.take_turn()