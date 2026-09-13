import math
import pygame
import styles as st
import ui_helpers as uh

def get_seat_postions(players):
    positions = []
    center_x, center_y = st.TABLE_CENTER
    radius = st.TABLE_RADIUS

    num_players = len(players)

    start_angle = math.pi/2

    angle_step= (2*math.pi) / num_players

    for i, player in enumerate(players):
        angle = start_angle + i * angle_step

        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)

        if y >= 450  and player.is_ai == True:
            y -= 75
            if x >= (st.WIDTH//2):
                x += 100

            if x <= (st.WIDTH//2):
                x -= 100

            

        positions.append((
            int(x - st.PLAYER_BOX_WIDTH / 2),
            int(y - st.PLAYER_BOX_HEIGHT / 2)
        ))
    return positions

def draw_dealer_marker(screen,x,y):
    pygame.draw.circle(screen,st.YELLOW,(x,y), 10)

    dealer_font = pygame.font.Font(None, 16)
    dealer_text = dealer_font.render("D", True, st.BLACK)
    dealer_rect = dealer_text.get_rect(center = (x,y))

    screen.blit(dealer_text, dealer_rect)

def draw_player_names(screen, name, x, y, font):
    name_font = font
    while name_font.size(name)[0] > st.PLAYER_BOX_WIDTH-30:
        current_size = name_font.get_height()
        name_font = pygame.font.Font(None, current_size - 1)

    uh.draw_text(screen, name, x, y, name_font)

def draw_player_panel (screen, player, x, y, font, game):
    width = st.PLAYER_BOX_WIDTH
    height = st.PLAYER_BOX_HEIGHT

    panel = pygame.Rect(x, y, width, height)


    if player == game.current_player:
        panel_color = st.LIGHT_BLUE
        border_color = st.YELLOW
    else:
        panel_color = st.DARK_BLUE
        border_color = st.WHITE

    pygame.draw.rect(screen, panel_color, panel)
    
    pygame.draw.rect(screen, border_color, panel, 2)

    draw_player_names(screen, player.name, x + 10, y + 10, font) 
    uh.draw_text(screen, f"Credits: {player.credits}", x + 10, y + 35, font)
    if player.folded:
        uh.draw_text(
        screen,
        "Folded",
        x + 10, y + 60,
        font,
        color = st.RED
    )
    else:
        uh.draw_text(screen, f"Cards: {len(player.hand)}", x + 10, y + 60, font, color=st.WHITE)

    if player == game.dealer:
        draw_dealer_marker(screen, x + width -20, y + 43)
