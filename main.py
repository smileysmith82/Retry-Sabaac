import pygame
import os
from game import Game
import styles as st
import ui
import ui_button as ub
import ui_profile as up
import ui_menu as um
import settings_page as sp

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "IMAGES")
def main():
    pygame.init()

    pygame.display.set_caption("Sabaac")
    WIN = pygame.display.set_mode((st.WIDTH,st.HEIGHT))
    
    font = pygame.font.SysFont(st.FONT_NAME, st.FONT_SMALL)
    small_font = pygame.font.SysFont(st.FONT_NAME, st.FONT_SMALL)
    profile_screen = up.ProfileScreen(font, small_font)

    previous_screen = None
    current_screen = "profile"
    selected_profile = None
    
    BG = pygame.transform.scale(pygame.image.load(os.path.join(
                                IMAGE_DIR, "Green_background.jpg")), 
                                (st.WIDTH, st.HEIGHT))

    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if current_screen == "profile":
                selected_profile = profile_screen.handle_event(event)

                if selected_profile is not None:
                    menu = um.MainMenu(
                        selected_profile,
                        font,
                        small_font
                    )
                    current_screen = "menu"

            elif current_screen == "menu":
                menu_action = menu.handle_event(event)

                if menu_action == "play":
                    game = Game(selected_profile)
                    current_screen = "game"

                if menu_action == "settings":
                    settings_page = sp.SettingsPage(
                        selected_profile, font, small_font
                    )
                    previous_screen = "menu"
                    current_screen = "settings"

                elif menu_action == "profile":
                    profile_screen.refresh_profiles()
                    profile_screen.reset()
                    current_screen = "profile"

                elif menu_action == "quit":
                    run = False

            elif current_screen == "settings":
                settings_action = settings_page.handle_event(event)

                if settings_action == "back":
                    current_screen = previous_screen

            elif current_screen == "game":
                game_action = ub.handle_button_clicks(event, game)

                if game_action == "menu":
                    current_screen = "menu"
                elif game_action == "settings":
                    settings_page = sp.SettingsPage(
                        selected_profile,
                        font,
                        small_font
                    )
                    previous_screen = "game"
                    game.menu_open = False
                    current_screen = "settings"

        if current_screen == "game":
            game.update()
        if current_screen == "profile":
            profile_screen.draw(WIN)

        elif current_screen == "menu":
            menu.draw(WIN)
        elif current_screen == "settings":
            settings_page.draw(WIN)

        elif current_screen == "game":
            ui.draw_background(WIN, BG)
            ui.draw_game(WIN, game, font)
        
        pygame.display.flip()
        
    pygame.quit()

if __name__ == "__main__":
    main()