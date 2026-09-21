import pygame

import styles as st
import ui_button as ub
import ui_helpers as uh


def draw_betting_phase(screen, game, font):
    pot_x, pot_y = st.WIDTH // 2 -150, 150
    panel_rect = pygame.Rect(pot_x,pot_y, 300, 100)

    pygame.draw.rect(screen, st.DARK_BLUE, panel_rect)
    pygame.draw.rect(screen, st.WHITE, panel_rect, 2)

    uh.draw_text(screen, f"General Pot: {game.general_pot}", pot_x + 20, pot_y + 15, font)
    uh.draw_text(screen, f"Current Bet: {game.betting.current_bet}", pot_x + 20, pot_y + 40, font)
    uh.draw_text(screen, f"Sabacc Pot: {game.sabaac_pot}", pot_x + 20, pot_y + 65, font)

    if game.betting.current_bet == 0:
        ub.betting_check_button.draw(screen, font)
    else:
        ub.betting_call_button.draw(screen, font)


    ub.betting_raise_button.draw(screen, font)
    ub.betting_fold_button.draw(screen, font)