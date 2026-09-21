import pygame
import styles as st
import player_actions

from ui_cards import (
    clicked_card,
    get_draw_pile_rect,
    get_discard_pile_rect
)

class Button:
    def __init__(self, text, x, y, width, height, color, text_color):
        self.text = text
        self.base_color = color
        self.text_color = text_color
        self.rect = pygame.Rect(x, y, width, height)

    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def is_clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONUP and 
            self.rect.collidepoint(event.pos)
        )

    def draw(self, screen, font):
        color = self.base_color

        if self.is_hovered():
            color = (min(self.base_color[0] + 30, 255),
                     min(self.base_color[1] + 30, 255),
                     min(self.base_color[2] + 30, 255)
                     )
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(
            screen,
            st.WHITE,
            self.rect,
            2
        )
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)

        screen.blit(text_surface, text_rect)

draw_button = Button(
    "Draw",
    st.DRAW_BUTTON_POSITION[0],
    st.DRAW_BUTTON_POSITION[1],
    st.BUTTON_WIDTH,
    st.BUTTON_HEIGHT,
    st.LIGHT_BLUE,
    st.BLACK
)

swap_button = Button(
    "Swap",
    st.DISCARD_BUTTON_POSITION[0],
    st.DISCARD_BUTTON_POSITION[1],
    st.BUTTON_WIDTH,
    st.BUTTON_HEIGHT,
    st.LIGHT_BLUE,
    st.BLACK
)

stand_button = Button(
    "Stand",
    st.STAND_BUTTON_POSITION[0],
    st.STAND_BUTTON_POSITION[1],
    st.BUTTON_WIDTH,
    st.BUTTON_HEIGHT,
    st.LIGHT_BLUE,
    st.BLACK
)

fold_button = Button(
    "Junk",
    st.FOLD_BUTTON_POSITION[0],
    st.FOLD_BUTTON_POSITION[1],
    st.BUTTON_WIDTH,
    st.BUTTON_HEIGHT,
    st.LIGHT_BLUE,
    st.BLACK
)

menu_button = Button(
    "Menu",
    st.MENU_BUTTON_POSITION[0],
    st.MENU_BUTTON_POSITION[1],
    st.BUTTON_WIDTH,
    st.BUTTON_HEIGHT,
    st.LIGHT_BLUE,
    st.BLACK
)

resume_button = Button(
    "Resume",
    st.MENU_OPTIONS_POSITION,
    300,
    st.MENU_BUTTON_WIDTH,
    st.MENU_BUTTON_HEIGHT,
    st.LIGHT_BLUE,
    st.BLACK
)

settings_button = Button(
    "Settings",
    st.MENU_OPTIONS_POSITION,
    370,
    st.MENU_BUTTON_WIDTH,
    st.MENU_BUTTON_HEIGHT,
    st.LIGHT_BLUE,
    st.BLACK
)

quit_button = Button(
    "Quit Game",
    st.MENU_OPTIONS_POSITION,
    440,
    st.MENU_BUTTON_WIDTH,
    st.MENU_BUTTON_HEIGHT,
    st.RED,
    st.WHITE
)

continue_button = Button(
    "Continue",
    500, 600, 
    st.MENU_BUTTON_WIDTH,
    st.MENU_BUTTON_HEIGHT,
    st.DARK_BLUE,
    st.WHITE 
)

back_button = Button(
    "Back",
    225, 600, 
    st.MENU_BUTTON_WIDTH,
    st.MENU_BUTTON_HEIGHT,
    st.DARK_BLUE,
    st.WHITE 
)

new_game_button = Button(
    "New Game",
    350,
    400, 
    st.MENU_BUTTON_WIDTH,
    st.MENU_BUTTON_HEIGHT,
    st.DARK_BLUE,
    st.WHITE 
)

winner_back_button = Button(
    "Back",
    350,
    465, 
    st.MENU_BUTTON_WIDTH,
    st.MENU_BUTTON_HEIGHT,
    st.DARK_BLUE,
    st.WHITE 
)

winner_quit_button = Button(
    "Quit Game",
    350,
    530,
    st.MENU_BUTTON_WIDTH,
    st.MENU_BUTTON_HEIGHT,
    st.RED,
    st.WHITE
)

betting_check_button = Button(
    "Check",
    st.STAND_BUTTON_POSITION[0],
    st.STAND_BUTTON_POSITION[1],
    st.BUTTON_WIDTH,
    st.BUTTON_HEIGHT,
    st.LIGHT_BLUE,
    st.BLACK
)

betting_call_button = Button(
    "Call",
    st.STAND_BUTTON_POSITION[0],
    st.STAND_BUTTON_POSITION[1],
    st.BUTTON_WIDTH,
    st.BUTTON_HEIGHT,
    st.LIGHT_BLUE,
    st.BLACK
)

betting_raise_button = Button(
    "Raise",
    st.DRAW_BUTTON_POSITION[0],
    st.DRAW_BUTTON_POSITION[1],
    st.BUTTON_WIDTH,
    st.BUTTON_HEIGHT,
    st.LIGHT_BLUE,
    st.BLACK
)

betting_fold_button = Button(
    "Fold",
    st.FOLD_BUTTON_POSITION[0],
    st.FOLD_BUTTON_POSITION[1],
    st.BUTTON_WIDTH,
    st.BUTTON_HEIGHT,
    st.LIGHT_BLUE,
    st.BLACK
)

def handle_button_clicks(event, game):
    if event.type != pygame.MOUSEBUTTONUP:
        return None

    if game.menu_open:
        if resume_button.is_clicked(event):
            game.close_menu()
            return

        if settings_button.is_clicked(event):
            print("Settings Closed")
            return

        if quit_button.is_clicked(event):
            game.quit_game()

        return

    if menu_button.is_clicked(event):
        game.open_menu()
        return

    if game.phase == game.SHOWDOWN_PHASE:
        if continue_button.is_clicked(event):
            game.next_showdown_page()
        if back_button.is_clicked(event):
            game.previous_showdown_page()

    if game.phase == game.WINNER_PHASE:
        if new_game_button.is_clicked(event):
            game.start_new_game()
            return
        if winner_quit_button.is_clicked(event):
            game.quit_game()
            return
        if winner_back_button.is_clicked(event):
            game.phase = game.SHOWDOWN_PHASE
            return
        return
    
    if not game.human_can_act:
        return None
    
    draw_pile_rect = get_draw_pile_rect()
    discard_pile_rect = get_discard_pile_rect()

    card_index = clicked_card(event, game)
    if card_index is not None:
        if game.selected_card == card_index:
            game.selected_card = None
        else:
            game.selected_card = card_index
            try_swap(game)
        return
   
    
    if draw_button.is_clicked(event) or draw_pile_rect.collidepoint(event.pos):
        player_actions.draw_card(game)
        return
      
    if swap_button.is_clicked(event) or discard_pile_rect.collidepoint(event.pos):
        if game.selected_discard:
            game.selected_discard = False
        else:
            game.selected_discard = True
        try_swap(game)
        return
    if stand_button.is_clicked(event):
        player_actions.stand(game)
        return
    if fold_button.is_clicked(event):
        player_actions.fold(game)
        return
    return None

def try_swap(game):
    if game.selected_card is not None and game.selected_discard:
        player_actions.swap(game, game.selected_card)
        game.selected_card = None
        game.selected_discard = False
