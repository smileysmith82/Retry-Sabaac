import pygame
import styles as st
import winning_hands as wh
import ui_helpers as uh
import ui_button as ub
import ui_cards as uc
import ui_panels as up
import ui_betting as ut
import ui_raise as ur
import settings as stt

def draw_background(screen, background):
    screen.blit(background, (0, 0))

def draw_showdown(screen, game, font):

    players_per_page = st.SHOWDOWN_PLAYERS_PER_PAGE

    start = game.showdown_page * players_per_page
    end = start + players_per_page
    players_to_show = game.showdown_order[start:end]

    
    box_width = 800
    box_height = 500

    box_x = (st.WIDTH - box_width) // 2
    box_y = 100
    #Showdown Outline
    showdown_rect = pygame.Rect(
        box_x,
        box_y,
        box_width,
        box_height
    )

    pygame.draw.rect(
        screen,
        st.DARK_BLUE,
        showdown_rect
    )

    pygame.draw.rect(
        screen,
        st.WHITE,
        showdown_rect,
        3
    )
    #Title
    uh.draw_text(
        screen,
        "Showdown",
        box_x + 20,
        box_y + 20,
        font
    )
    for row, player_index in enumerate(players_to_show):
        player = game.players[player_index]
        if not player.is_ai:
            name_color = st.YELLOW
        else:
            name_color = st.WHITE

        uh.draw_text(
            screen,
            player.name,
            box_x + 20,
            box_y + 80 + row * 100,
            font,
            color=name_color
        )

        if player.folded:
            uh.draw_text(
            screen,
            "Folded",
            box_x + 250,
            box_y + 80 + row *100,
            font,
            color= st.RED
            ) 
            continue

        card_spacing = st.SHOWDOWN_CARD_WIDTH + 10

        for card_index, card in enumerate(player.hand):
            x = box_x + 250 + card_index * card_spacing
            y = box_y + 60 + row * 100

            uc.draw_card_image(
                screen,
                card,
                x, y, font,
                st.SHOWDOWN_CARD_WIDTH,
                st.SHOWDOWN_CARD_HEIGHT
            )

        score = game.total_of_hand(player.hand)
        score_x = box_x + 250 + len(player.hand) * card_spacing 
        score_y = y + (st.SHOWDOWN_CARD_HEIGHT // 2) - (font.get_height() //2)

        uh.draw_text(
            screen,
            f"Score: {score}",
            score_x, score_y,
            font
        )

def draw_winner_screen(screen, game, font):
    winner = game.winner
    winning_hand = wh.evaluate_hand(winner.hand)
    hand_name = wh.HAND_NAMES[winning_hand[0]]
    box_width = 800
    box_height = 500

    box_x = (st.WIDTH - box_width) // 2
    box_y = 100

    winner_rect = pygame.Rect(
        box_x,
        box_y,
        box_width,
        box_height
    )

    pygame.draw.rect(
        screen,
        st.DARK_BLUE,
        winner_rect
    )

    pygame.draw.rect(
        screen,
        st.WHITE,
        winner_rect,
        3
    )

    uh.draw_text(
        screen,
        f"Winner: {winner.name} with {hand_name}",
        350,
        175,
        font
    )
    uh.draw_text(
            screen,
            f"General Pot: {game.awarded_general_pot} credits",
            350,
            250,
            font
        )
    if game.total_of_hand(game.winner.hand) == 0:
        uh.draw_text(
            screen,
            f"Sabaac Pot: {game.awarded_sabaac_pot} credits",
            350,
            325,
            font
        )
    else:
            uh.draw_text(
            screen,
            f"Nobody had a Sabbac",
            350,
            325,
            font
        )
            uh.draw_text(
            screen,
            f"Credits in Sabaac Pot: {game.sabaac_pot} credits",
            350,
            360,
            font
        )

_dice_cache = {}
def load_dice_image(dice):
    if dice not in _dice_cache:
        image = pygame.image.load(f"Images/dice_{dice}.jpg").convert()
        image = pygame.transform.scale(
            image,
            (st.DICE_WIDTH, st.DICE_HEIGHT)
        )

        _dice_cache[dice] = image

    return _dice_cache[dice]

def draw_dice(screen, dice, x, y):
    dice_image = load_dice_image(dice)
    screen.blit(dice_image, (x,y))

def draw_menu(screen, font):
    overlay = pygame.Surface((st.WIDTH, st.HEIGHT), pygame.SRCALPHA)
    overlay.fill((23, 23, 23, 150))
    screen.blit(overlay, (0,0))

    menu_width = 400
    menu_height = 350

    menu_x = (st.WIDTH - menu_width) // 2
    menu_y = (st.HEIGHT - menu_height) // 2

    menu_rect = pygame.Rect(
        menu_x,
        menu_y,
        menu_width,
        menu_height
    )

    pygame.draw.rect(screen, st.DARK_BLUE, menu_rect)
    pygame.draw.rect(screen, st.WHITE, menu_rect, 3)
    uh.draw_text(
        screen,
        "Menu",
        menu_x + 150,
        menu_y + 30,
        font
    )

    ub.resume_button.rect.topleft = (menu_x + 50, menu_y + 100)
    ub.settings_button.rect.topleft = (menu_x + 50, menu_y + 170)
    ub.quit_button.rect.topleft = (menu_x + 50, menu_y + 240)

    ub.resume_button.draw(screen,font)
    ub.settings_button.draw(screen,font)
    ub.quit_button.draw(screen,font)

#What Shows Up on the Screen
def draw_game(screen, game, font):
    uc.draw_draw_pile(screen, font)
    uc.draw_discard_pile(screen, game.discard_pile, font, selected=game.selected_discard)
    display_round_info(screen,game,font)

    if game.display_die1 is not None:
        draw_dice(screen, game.display_die1, 400, 200)

    if game.display_die2 is not None:
        draw_dice(screen, game.display_die2, 500, 200)

    if game.phase == game.SHOWDOWN_PHASE:
        game.clickable_cards = []
        draw_showdown(screen, game, font)
        ub.continue_button.draw(screen, font)
        ub.back_button.draw(screen, font)

    elif game.phase == game.WINNER_PHASE:
        game.clickable_cards = []
        draw_winner_screen(screen, game, font)
        ub.new_game_button.draw(screen, font)
        ub.winner_back_button.draw(screen,font)
        ub.winner_quit_button.draw(screen, font)

    elif game.phase == game.BETTING_PHASE:
        ut.draw_betting_phase(screen, game, font)
        game.clickable_cards = uc.draw_player_hand(screen, game.current_human_player, font,game.selected_card)
        positions = up.get_seat_postions(game.players)
        for player, (x, y) in zip(game.players, positions):
            up.draw_player_panel(screen, player, x, y, font, game)
        if game.betting.current_bet == 0:
            ub.betting_check_button.draw(screen, font)
        else:
            ub.betting_call_button.draw(screen, font)

        player = game.current_player
        current_bet = game.betting.current_bet
        player_contribution = game.betting.player_bets[player]
        min_raise = stt.MINIMUM_RAISE
        new_bet = current_bet + min_raise
        raise_allowed = game.betting.can_raise(new_bet)

        ub.betting_raise_button.disabled = not raise_allowed

        if raise_allowed:
            ub.betting_raise_button.base_color = st.LIGHT_BLUE
            ub.betting_raise_button.text_color = st.BLACK

        else:
            ub.betting_raise_button.base_color = st.GRAY
            ub.betting_raise_button.text_color = st.WHITE

        ub.betting_raise_button.draw(screen, font)
        ub.betting_fold_button.draw(screen, font)
        if game.raise_panel_open:
            ur.draw_raise_panel(screen,game, font)

    else:
        game.clickable_cards = uc.draw_player_hand(screen, game.current_human_player, font,game.selected_card)

        positions = up.get_seat_postions(game.players)

        for player, (x, y) in zip(game.players, positions):
            up.draw_player_panel(screen, player, x, y, font, game)

        ub.draw_button.draw(screen, font)
        ub.swap_button.draw(screen, font)
        ub.stand_button.draw(screen, font)
        ub.fold_button.draw(screen, font)

    ub.menu_button.draw(screen, font)

    if game.phase == game.DICE_RESULT_PHASE:
        draw_dice(screen, game.display_die1, 400, 200)
        draw_dice(screen, game.display_die2, 500, 200)

        msg = "Dice Match!" if game.dice_matched else "Dice don't Match!"
        uh.draw_text(screen, msg, st.WIDTH//2-100, 150, font)
    

    if game.menu_open:
        draw_menu(screen, font)

    
    
def display_round_info(screen, game, font):
    x,y = st.GAME_INFO_POSITION

    if game.phase == game.SHOWDOWN_PHASE:
        round_number = game.rounds_per_game
    else:
        round_number = game.rounds_played + 1

    uh.draw_text(screen,
              f"Round: {round_number}/ {game.rounds_per_game}",
              x,
              y,
              font)

    uh.draw_text(screen,
              f"Current Phase: {game.phase}",
              x,
              y+20,
              font)

    uh.draw_text (screen,
               f"Current Player: {game.current_player.name}",
               x,
               y + 40,
               font)

