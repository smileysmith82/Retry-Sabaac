import pygame
import styles as st
import ui_helpers as uh
import ui_button as ub

def draw_raise_panel(screen, game, font):
    panel_width = 300
    panel_height = 250

    x = (st.WIDTH - panel_width) // 2
    y = (st.HEIGHT - panel_height) // 2

    rect = pygame.Rect(x, y, panel_width, panel_height)
    pygame.draw.rect(screen, st.DARK_BLUE, rect)
    pygame.draw.rect(screen, st.WHITE, rect, 2)

    uh.draw_text(screen, "Raise Amount:", x + 40, y + 20, font)
    uh.draw_text(screen, f"{game.pending_raise_amount}", x + 40, y + 60, font)

    ub.raise_1_button.rect.topleft = (x + 30, y + 100)
    ub.raise_5_button.rect.topleft = (x + 160, y + 100)
    ub.raise_10_button.rect.topleft = (x + 30, y + 150)
    ub.raise_reset_button.rect.topleft = (x + 160, y + 150)
    ub.raise_confirm_button.rect.topleft = (x + 30, y + 210)
    ub.raise_cancel_button.rect.topleft = (x + 160, y + 210)
    

    ub.raise_1_button.draw(screen, font)
    ub.raise_5_button.draw(screen, font)
    ub.raise_10_button.draw(screen, font)
    ub.raise_reset_button.draw(screen, font) 
    ub.raise_confirm_button.draw(screen, font)
    ub.raise_cancel_button.draw(screen, font)

    if hasattr(game, "raise_error_message") and game.raise_error_message:
        uh.draw_text(screen, game.raise_error_message, x+40, y +180, font)