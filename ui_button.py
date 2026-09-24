import pygame
import styles as st
import player_actions
import settings as stt
from ui_cards import (
    clicked_card,
    get_draw_pile_rect,
    get_discard_pile_rect
)
import showdown as show

class Button:
    def __init__(self, text, x, y, width, height, color, text_color):
        self.text = text
        self.base_color = color
        self.text_color = text_color
        self.rect = pygame.Rect(x, y, width, height)
        self.disabled = False

    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def is_clicked(self, event):
        if self.disabled:
            return False
        return (
            event.type == pygame.MOUSEBUTTONUP and 
            self.rect.collidepoint(event.pos)
        )

    def draw(self, screen, font):
        if self.disabled:
            color = st.GRAY
        else:
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
#In Game Buttons
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

#Menu Buttons
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
#Winner Buttons
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

#Betting_buttons
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

raise_1_button = Button("Raise +1",
        0, 0, st.BUTTON_WIDTH,
        st.BUTTON_HEIGHT, 
        st.LIGHT_BLUE, st.BLACK)
raise_5_button = Button("Raise +5",
        0, 0, st.BUTTON_WIDTH,
        st.BUTTON_HEIGHT,
        st.LIGHT_BLUE,
        st.BLACK)
raise_10_button = Button("Raise +10",
        0, 0, st.BUTTON_WIDTH,
        st.BUTTON_HEIGHT,
        st.LIGHT_BLUE,
        st.BLACK)
raise_reset_button = Button("Reset",
        0, 0, 
        120, 40,
        st.GRAY,
        st.WHITE)
raise_confirm_button = Button("Confirm",
        0, 0,
        120, 40,
        st.GREEN,
        st.WHITE)
raise_cancel_button = Button("Cancel",
        0, 0,
        120, 40,
        st.RED,
        st.WHITE)
raise_allin_button =  Button("All In",
        0, 0,
        120, 80,
        st.RED,
        st.WHITE)


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
    if game.raise_panel_open:
        current_bet = game.betting.current_bet
        player = game.current_player
        player_contribution = game.betting.player_bets[player]

        call_amount = current_bet - player_contribution
        max_raise_by_credits = player.credits - call_amount

        active_players = len([p for p in game.players if not p.folded])

        if active_players > 2:
            if game.betting.current_bet == 0:
                max_raise_by_rule = 10
            else:
                max_raise_by_rule = game.betting.current_bet * 2
        else:
            max_raise_by_rule = max_raise_by_credits

        max_raise = min(max_raise_by_credits, max_raise_by_rule)

        if raise_1_button.is_clicked(event):
            if game.pending_raise_amount + 1 <= max_raise:
                game.pending_raise_amount +=1
            else:
                game.pending_raise_amount = max_raise 
            return
        
        if raise_5_button.is_clicked(event):
            if game.pending_raise_amount + 5 <= max_raise:
                game.pending_raise_amount +=5
            else:
                game.pending_raise_amount = max_raise
            return

        if raise_10_button.is_clicked(event):
            if game.pending_raise_amount + 10 <= max_raise:
                game.pending_raise_amount +=10
            else:
                game.pending_raise_amount = max_raise                
            return

        if raise_reset_button.is_clicked(event):
            game.pending_raise_amount = 0
            return

        if raise_allin_button.is_clicked(event):
            amount_to_call = game.betting.current_bet - game.betting.player_bets[game.current_player]
            game.pending_raise_amount = game.current_player.credits - amount_to_call
            return
                
        if raise_confirm_button.is_clicked(event):
            if game.pending_raise_amount < stt.MINIMUM_RAISE:
                game.pending_raise_amount = stt.MINIMUM_RAISE

            if game.pending_raise_amount > max_raise:
                game.pending_raise_amount = max_raise
            

            final_amount = current_bet + game.pending_raise_amount

            print("Attempting raise to: ", final_amount)

            success = game.player_raise(final_amount)
            print("Raise success: ", success)

            
            if success:
                game.betting.next_betting_turn()
                game.raise_error_message = ""
                game.raise_panel_open = False
            else:
                game.raise_error_message = "Invalid Raise Value. Please Try Again"

            return
    
        if raise_cancel_button.is_clicked(event):
            game.raise_panel_open = False
            game.pending_raise_amount = 0
            game.raise_error_message = ""
            return

    if game.phase == game.SHOWDOWN_PHASE:
        if continue_button.is_clicked(event):
            show.next_showdown_page(game)
        if back_button.is_clicked(event):
            show.previous_showdown_page(game)

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

    if game.phase == game.BETTING_PHASE:
        if not game.human_can_act:
            return None
        
        if game.betting.current_bet == 0:
            if betting_check_button.is_clicked(event):
                game.player_check()
                return
        else:
            if betting_call_button.is_clicked(event):
                game.player_call()
                return

        if betting_raise_button.is_clicked(event):
            game.raise_panel_open = True
            game.pending_raise_amount = 0
            game.raise_error_message = ""
            return

        if betting_fold_button.is_clicked(event):
            game.player_fold()
            return

        return
    
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
        if game.selected_card is not None:
            player_actions.swap(game, game.selected_card, source="draw")
            game.selected_card = None
            return
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

def handle_clicks(self):
    if self.disabled:
        return False