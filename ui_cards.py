import pygame
import styles as st
from ui_helpers import draw_text

__card_cache = {}
def load_card_image(card):
    if card.file_name not in __card_cache:
        image = pygame.image.load(f"Images/{card.file_name}").convert_alpha()
        image = pygame.transform.scale(image, (st.CARD_WIDTH, st.CARD_HEIGHT))

        __card_cache[card.file_name] = image

    return __card_cache[card.file_name]

def draw_card_image (screen, card, x, y, font, width=None, height = None, selected_card = False):
    if width is None:
        width = st.CARD_WIDTH

    if height is None:
        height = st.CARD_HEIGHT

    image = load_card_image(card)

    image = pygame.transform.scale(image, (width, height))

    card_rect = image.get_rect(topleft=(x, y))

    screen.blit(image, card_rect)

    mask = pygame.mask.from_surface(image)

    if selected_card:
        outline = mask.outline()
        if len(outline) >= 2:    
            outline = [
                (point_x + card_rect.x, point_y + card_rect.y)
                for point_x, point_y in outline
            ]

            pygame.draw.lines(
                screen,
                st.YELLOW,
                True,
                outline,
                4
            )

    mouse_x, mouse_y = pygame.mouse.get_pos()

    if card_rect.collidepoint(mouse_x, mouse_y):
        local_x = mouse_x - card_rect.x
        local_y = mouse_y - card_rect.y

        if mask.get_at((local_x, local_y)):
            rank_text = get_rank_text(card)
            text_surface = font.render(rank_text, True, st.YELLOW)

            text_rect = text_surface.get_rect(
                midbottom=(card_rect.centerx, card_rect.top - 5)
            )

            screen.blit(text_surface, text_rect)

    return {
        "rect": card_rect,
        "mask": mask,
        "position": (x,y)
    }

def get_rank_text(card):
    if card.rank > 0:
        return f"+{card.rank}"
    else:
        return str(card.rank)

def draw_player_hand(screen, player, font, selected_card = None):
    clickable_cards = []

    card_spacing = st.CARD_WIDTH + 2
    hand_width = len(player.hand) * card_spacing - 10
    center_x = st.WIDTH // 2
    start_x = center_x - hand_width // 2
    y = st.HEIGHT - st.CARD_HEIGHT - 100

    for i, card in enumerate(player.hand):
        x = start_x + i * card_spacing
        is_selected = (i == selected_card)

        card_data = draw_card_image(screen, card, x, y, font, selected_card= is_selected)
        clickable_cards.append(card_data)
    return clickable_cards

def clicked_card(event,game):
    mouse_x, mouse_y = event.pos

    for index, card in enumerate(getattr(game, "clickable_cards", [])):
        rect = card["rect"]

        if rect.collidepoint(mouse_x, mouse_y):
            local_x = mouse_x - rect.x
            local_y = mouse_y - rect.y

            if card["mask"].get_at((local_x, local_y)):
                return index
    return None

_card_back = None
def load_card_back():
    global _card_back
    if _card_back is None:
        image = pygame.image.load("Images/backside.png")
        _card_back = pygame.transform.scale(image, (st.CARD_WIDTH, st.CARD_HEIGHT))
    return _card_back

def draw_draw_pile(screen, font):
    x,y = st.DRAW_PILE_POSITION

    draw_text(screen, "Draw Pile:", x, y-40, font)

    card_back = load_card_back()
    screen.blit(card_back, (x, y))

def get_draw_pile_rect():
    x,y = st.DRAW_PILE_POSITION
    return pygame.Rect(x, y, st.CARD_WIDTH, st.CARD_HEIGHT)

def draw_discard_pile(screen, discard_pile, font, selected=False):
    x,y = st.DISCARD_PILE_POSITION

    draw_text(screen, "Discard Pile:", x, y-40, font)
    

    if discard_pile:
        top_card = discard_pile[-1]
        draw_card_image(screen, top_card, x, y, font, selected_card=selected)

def get_discard_pile_rect():
    x,y = st.DISCARD_PILE_POSITION
    return pygame.Rect(x, y, st.CARD_WIDTH, st.CARD_HEIGHT)
